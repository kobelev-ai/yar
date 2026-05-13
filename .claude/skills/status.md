---
name: status
description: Quick overview of your workspace — tasks, promises, projects, meetings
user_invocable: true
---

# /status — System Overview

Show a quick dashboard of the workspace state.

## What to show

Read `tasks/todo.md`, `context/meetings/index.json`, and `context/projects/*.md`, then display:

```
SYSTEM STATUS
=============

Tasks:       [N] total | [X] Priority 1 | [Y] Priority 2
Promises:    [N] active | [X] overdue
Waiting For: [N] items | [X] older than 7 days
Projects:    [N] active | [X] without activity >7 days
Meetings:    [N] processed | [X] in inbox
People:      [N] cards

OVERDUE
-------
- [PROMISE] task (was due DD.MM)
- Waiting: Person — action (since DD.MM, [X] days ago)

UPCOMING DEADLINES (next 7 days)
---------------------------------
- task (due DD.MM)

STALE PROJECTS
--------------
- project (last activity: DD.MM)

INBOX
-----
[N] items waiting to be processed
```

## Rules
- Keep it concise — pure data, no commentary
- Highlight problems (overdue, stale) at the top
- Check `inbox/` for unprocessed items
- If everything is healthy — say "All systems healthy"
