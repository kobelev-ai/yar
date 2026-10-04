---
name: setup
description: Configure Yar with the owner's language, profile and first real task while preserving existing files. Use for new setup or explicit reconfiguration.
---

# Set up Yar

Read the root contract. Ask only the owner's name, language and first useful task
if unknown. Existing profile and answers in the conversation are sufficient.
Run `python3 scripts/yar_workspace.py init` from the selected workspace, or create
only missing files from templates if Python is unavailable. Never overwrite an
existing todo, memory, index, README, profile or installation registry.
Keep the shared root AGENTS/CLAUDE files generic; store owner details in
`context/me.md` and `context/me/preferences.md`. Reconfiguration changes only
explicitly requested profile fields, preserving everything else. Preserve an
original before editing an existing owner file. Don't run git add/commit on data.

Help the owner put actual materials in `tasks/<name>/`, then use the task workflow
to produce their first result. The owner may name an existing folder instead.
Profile completeness, goals, people cards and a brain dump can follow when useful;
none is a prerequisite for doing the first task. Set up integrations only if asked.
Mention inbox for incoming files and the single action list for ongoing commitments.
Use setup-wizard only if the host supports subagents; otherwise follow this workflow
in the main assistant. Don't replace the owner's chosen model or application.
