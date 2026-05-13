---
name: brief
description: Prepare a quick 1-page brief on a project
user_invocable: true
---

# /brief — Project Brief

Prepare a 1-page brief on the specified project.

## Usage

User calls: `/brief <project name>`

If no name given — ask "Which project should I brief?"

## Data Sources

1. **Project:** `context/projects/<project>.md`
2. **People:** `context/people/*.md` — people involved in the project
3. **Meetings:** `context/meetings/index.json` — last 3-5 meetings on this project
4. **Tasks:** `tasks/todo.md` — open tasks related to the project
5. **Promises:** tasks with `[PROMISE]` in the todo list

## Output Format

```markdown
# Brief: [Project Name]

**Status:** active/paused/...
**Last activity:** DD.MM.YYYY
**Key people:** [names]

## Summary
[2-3 sentences on what this project is about]

## Recent Activity
- [Last 3 meetings/events with dates]

## Open Tasks
- [List of open tasks from todo list]

## Promises
- [Any PROMISE items related to this project]

## Next Steps
- [Recommended next actions]
```
