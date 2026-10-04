---
name: meeting-processor
description: Process a transcript into preserved evidence, a saved summary, deduplicated actions and separate confirmation candidates.
---

Read the selected root contract and review paths from `ops/tasks/review/queues.json`.
Read the original transcript, identify date/participants and distinguish what each
speaker said, proposed and agreed. Use speaker maps and owner signals where useful;
uncertain identification remains explicitly uncertain. Check `ops/meetings/index.json`
for duplicate sources/content before processing. Preserve the byte-for-byte source
under `ops/meetings/processed/` with its original name; resolve collisions safely.
Speaker label normalization goes into a separately named derivative, never the only
original. Index both paths where present, plus date, participants, topics, source and
summary path; keep the index's established structure. Don't initialize over an index.

Open the relevant project's pointer; match the destination from confirmed facts.
Save a self-contained dated summary with primary-source coordinates in that project
or task folder, otherwise in `ops/meetings/docs/`. Link it from the project pointer.
Record explicit commitments/actions in `ops/tasks/todo.md` after deduplication,
with source and only confirmed deadlines. Statements that may indicate an existing
action is completed go to the closures queue. Interpretations of the owner's
positions/preferences and suggested strategic decisions go to the insights queue.
Don't apply those candidates to memory, decisions or task status without explicit
owner confirmation. Update factual project activity and confirmed person facts with
sources. Preserve owner processing boundaries. Return original/summary links, added
actions, candidates and unresolved identification or attribution gaps.
