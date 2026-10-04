"""Transcript directories, resolved without opening mail or creating files."""
from pathlib import Path


def transcript_paths(environment):
    configured = environment.get("MEETINGS_INBOX", "").strip()
    if not configured:
        raise ValueError("MEETINGS_INBOX must be set to an absolute directory in .env")
    inbox = Path(configured).expanduser()
    if not inbox.is_absolute():
        raise ValueError("MEETINGS_INBOX must be an absolute directory")
    inbox = inbox.resolve()
    processed = environment.get("MEETINGS_PROCESSED", "").strip()
    if processed:
        result = Path(processed).expanduser()
        if not result.is_absolute():
            raise ValueError("MEETINGS_PROCESSED must be an absolute directory")
        return inbox, result.resolve()
    explicit = environment.get("YAR_ROOT", "").strip()
    if explicit:
        root = Path(explicit).expanduser()
        if not root.is_absolute():
            raise ValueError("YAR_ROOT must be an absolute directory")
    else:
        root = next((p for p in (inbox, *inbox.parents) if (p / ".yar-root").is_file()), inbox.parent)
    return inbox, (root / "ops/meetings/processed").resolve()
