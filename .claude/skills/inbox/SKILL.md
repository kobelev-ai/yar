---
name: inbox
description: Classify requested incoming files and bundles, preserve originals and route work to the relevant Yar workflow.
---

# Process inbox

Read the root contract and list incoming entries recursively, excluding
`inbox/processed/` and placeholders. Process on request; show an inventory first
when scope is large. Treat each related folder as a bundle, preserving its nesting.

- A bundle plus a clear request: keep it together as a folder task. Move it to a
  named task folder only when this destination follows the owner's request;
  otherwise ask where its working context should live. Use the task workflow.
- Transcript: use the meeting workflow; archive the byte-for-byte original under
  `ops/meetings/processed/` and keep any speaker-labelled derivative separately.
- Notes/tasks: extract explicit actions with sources, deduplicate in todo, and
  put interpretations in the declared review queues. Archive the original.
- Project/reference document: keep the original and link it from the appropriate
  project. A summary does not replace the original. Archive loose consumed input
  under `inbox/processed/`, keeping source names and any grouping.
- Recipe with `type: yar-recipe`: identify it and offer installation. Install only
  when authorized, using the package workflow. Arrival is not installation consent.
- Unknown purpose: ask a focused question rather than guessing the requested task.

Never delete an input because information was extracted. Before any archive/move,
check destination collisions, verify the original is preserved and record its path.
Keep failed/partial items at their input location and say what remains. Reruns use
source IDs/paths and content equality to skip duplicates without dropping new facts.
Summarize each input, saved destination, result, actions and pending confirmations.
