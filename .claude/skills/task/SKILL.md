---
name: task
description: Execute a work request from a folder of materials, save a checked result and a continuation README. Use when the owner asks to solve, analyze or continue a folder task.
argument-hint: "<folder or task name>"
---

# Execute or continue a folder task

1. Read the root AGENTS/CLAUDE contract. Resolve the workspace using `.yar-root`
   or an explicit YAR_ROOT; stay inside the selected workspace for outputs.
2. Find the folder named in the request or its existing project pointer. Read its
   README and linked current result before loading relevant sources. If creating
   a task folder, use `tasks/<owner's name for the task>/`. Don't copy material
   from another project merely to fit this layout. No task form is required.
3. Determine the requested deliverable, audience, conditions and completion
   criteria from the conversation and materials. Ask only for information that
   changes the outcome. Don't execute an arbitrary task just because files exist.
4. Inventory related inputs recursively. Open each necessary primary source;
   preserve filenames, subfolders and original contents. If a format is unreadable,
   report that gap and complete independent work using the readable sources.
5. Work through the request to a concrete artifact. Check facts and calculations
   against sources with units, time periods and conditions. Distinguish proposals
   from decisions; do not invent personal episodes or missing evidence.
6. Save a dated Markdown working result in this folder. Produce any other
   requested formats using available tools and check the artifact. Keep previous
   versions. Name the result `YY-MM-DD_HHMM_Topic.md` using current local time.
7. Create/update README: goal, criteria, actual status/date, current result link,
   missing information, next step, and a link to a relevant open action if needed.
   Don't claim that a prepared artifact was sent or accepted.
8. Link ongoing actions to `ops/tasks/todo.md` without semantic duplicates. Record
   only the owner's actual commitments and confirmed dates. A finished one-turn
   request does not require an open item. Put meeting-derived memory/closure
   candidates into the queues declared in `ops/tasks/review/queues.json`.
9. Return the result and clickable file link. When asked to continue later, begin
   from this README and necessary sources. Internal tool setup belongs in the
   work record, not the audience-facing deliverable.

Optional helper to create a folder and initial pointer (agent can do this itself):
`python3 scripts/yar_workspace.py task "<name>" --goal "<request>"`.
Resolve this script from the workspace root; never from a guessed home path.
