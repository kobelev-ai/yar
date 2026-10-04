---
name: brief
description: Produce a saved project brief from its current pointer and primary sources.
argument-hint: "<project>"
---

# Project brief

Resolve the root; locate the named project via `context/projects/` or its actual
folder. Read its current README/pointer, relevant dated source documents, meeting
index and related actions in `ops/tasks/todo.md`. Open cited primary sources.
Don't read all projects and personal memory. Show goal, checked status/date,
current result, actual recent developments, open actions and next decision.
Distinguish proposal, decision and commitment. Save a dated brief in the project's
working folder (or `tasks/<project>/` when no folder exists), update its pointer,
and return the link. An indexed meeting alone doesn't prove current project status.
