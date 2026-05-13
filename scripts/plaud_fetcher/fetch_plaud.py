#!/usr/bin/env python3
"""
Plaud Transcript Fetcher
Fetches meeting transcripts from email (IMAP), saves to meetings/inbox/
Works with Plaud Note, Otter.ai, or any recorder that emails transcripts.
"""

import imaplib
import email
import os
import re
import sys
import time
import socket
import logging
from datetime import datetime
from email.header import decode_header
from pathlib import Path
from dotenv import load_dotenv

# Load environment
load_dotenv(Path(__file__).parent / ".env")

# Config
IMAP_SERVER = os.getenv("IMAP_SERVER", "imap.gmail.com")
IMAP_PORT = int(os.getenv("IMAP_PORT", "993"))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
INBOX_PATH = Path(os.getenv("MEETINGS_INBOX", ""))
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "300"))
PLAUD_SUBJECT_PREFIX = os.getenv("PLAUD_SUBJECT_PREFIX", "[Plaud-AutoFlow]")

if not INBOX_PATH or str(INBOX_PATH) == "":
    print("ERROR: MEETINGS_INBOX must be set in .env")
    sys.exit(1)

PROCESSED_PATH = Path(os.getenv("MEETINGS_PROCESSED", str(INBOX_PATH.parent / "context" / "meetings" / "processed")))

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(Path(__file__).parent / "plaud_fetcher.log"),
    ],
)
log = logging.getLogger(__name__)

# Ensure directories exist
INBOX_PATH.mkdir(parents=True, exist_ok=True)
PROCESSED_PATH.mkdir(parents=True, exist_ok=True)


def decode_mime_header(header_value: str) -> str:
    """Decode MIME encoded header (handles =?UTF-8?B?...?= etc.)"""
    if not header_value:
        return ""
    decoded_parts = decode_header(header_value)
    result = []
    for part, charset in decoded_parts:
        if isinstance(part, bytes):
            result.append(part.decode(charset or "utf-8", errors="replace"))
        else:
            result.append(part)
    return "".join(result)


def sanitize_filename(name: str) -> str:
    """Remove characters unsafe for filenames"""
    name = re.sub(r'^(Fwd|Re|Fw):\s*', '', name, flags=re.IGNORECASE).strip()
    name = name.replace(PLAUD_SUBJECT_PREFIX, "").strip()
    name = re.sub(r'[/\\:*?"<>|]', "_", name)
    name = re.sub(r"[_\s]+", " ", name).strip()
    return name


def format_date(date_str: str) -> str:
    """Parse email date and format as YYYY-MM-DD_HH_MM in local timezone"""
    try:
        parsed = email.utils.parsedate_to_datetime(date_str)
        local = parsed.astimezone()
        return local.strftime("%Y-%m-%d_%H_%M")
    except Exception:
        return datetime.now().strftime("%Y-%m-%d_%H_%M")


def process_message(mail: imaplib.IMAP4_SSL, msg_id: bytes) -> bool:
    """Process a single email message. Returns True if transcript was saved."""
    _, msg_data = mail.fetch(msg_id, "(RFC822)")
    raw_email = msg_data[0][1]
    msg = email.message_from_bytes(raw_email)

    subject = decode_mime_header(msg.get("Subject", ""))
    date_str = msg.get("Date", "")

    if PLAUD_SUBJECT_PREFIX.lower() not in subject.lower():
        return False

    log.info(f"Processing: {subject}")

    date_formatted = format_date(date_str)
    clean_subject = sanitize_filename(subject)
    filename = f"{date_formatted}_{clean_subject}.txt"
    filepath = INBOX_PATH / filename

    # Check if already saved
    processed_filepath = PROCESSED_PATH / filename
    if filepath.exists() or processed_filepath.exists():
        log.info(f"  Already exists: {filename}")
        return False

    # Dedup by meeting date + topic
    meeting_match = re.search(r"(\d{2}-\d{2})\s+(.+)", clean_subject)
    if meeting_match:
        meeting_date = meeting_match.group(1)
        topic_words = meeting_match.group(2)[:50].lower()
        for folder in (INBOX_PATH, PROCESSED_PATH):
            for f in folder.glob(f"*{meeting_date}*"):
                fname_lower = f.name.lower()
                sig_words = [w for w in re.findall(r"[a-zа-яё]+", topic_words) if len(w) > 3][:4]
                if sig_words and all(w in fname_lower for w in sig_words):
                    log.info(f"  Duplicate by meeting date + topic: {f.name}")
                    return False

    # Find .txt attachment
    saved = False
    for part in msg.walk():
        content_disposition = str(part.get("Content-Disposition", ""))
        if "attachment" not in content_disposition:
            continue

        attachment_name = decode_mime_header(part.get_filename() or "")
        if not attachment_name.lower().endswith(".txt"):
            continue

        payload = part.get_payload(decode=True)
        if payload:
            filepath.write_bytes(payload)
            log.info(f"  Saved: {filename} ({len(payload)} bytes)")
            saved = True
            break

    return saved


def fetch_transcripts(once: bool = False):
    """Connect to IMAP and fetch transcripts"""
    if not EMAIL_USER or not EMAIL_PASSWORD:
        log.error("EMAIL_USER and EMAIL_PASSWORD must be set in .env")
        sys.exit(1)

    while True:
        try:
            log.info("Connecting to IMAP...")
            socket.setdefaulttimeout(60)
            mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
            mail.login(EMAIL_USER, EMAIL_PASSWORD)
            mail.select("INBOX")

            search_term = PLAUD_SUBJECT_PREFIX.replace("[", "").replace("]", "")
            _, message_ids = mail.search(None, f'(SUBJECT "{search_term}")')
            ids = message_ids[0].split()

            if ids:
                log.info(f"Found {len(ids)} email(s), checking for new...")
                new_count = sum(1 for msg_id in ids if process_message(mail, msg_id))
                if new_count:
                    log.info(f"Saved {new_count} new transcript(s)")
                else:
                    log.info("All emails already processed")
            else:
                log.info("No matching emails found")

            mail.logout()

        except imaplib.IMAP4.error as e:
            log.error(f"IMAP error: {e}")
        except Exception as e:
            log.error(f"Unexpected error: {e}")

        if once:
            break

        log.info(f"Next check in {CHECK_INTERVAL}s...")
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    once = "--once" in sys.argv
    fetch_transcripts(once=once)
