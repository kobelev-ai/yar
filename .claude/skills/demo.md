---
name: demo
description: Load demo workspace with sample data (for demonstrations and testing)
user_invocable: true
---

# /demo — Load Demo Workspace

Populates the workspace with realistic demo data to showcase the system's capabilities.

## What it does

Copies pre-built demo data from `templates/demo/` into the workspace:
- `context/me.md` — sample CEO profile (Alexei Petrov, TechVentures)
- `tasks/todo.md` — 15+ tasks with promises, priorities, waiting-for
- `context/me/decisions.md` — decision log from 4 meetings
- `context/meetings/index.json` — 3 indexed meetings
- `context/meetings/speaker_mappings.json` — speaker IDs
- `context/projects/datapulse-acquisition.md` — M&A project
- `context/projects/ai-pilot-program.md` — AI transformation project

## How to run

Copy demo files to workspace locations:

```bash
cp templates/demo/me.md context/me.md
cp templates/demo/todo.md tasks/todo.md
cp templates/demo/decisions.md context/me/decisions.md
cp templates/demo/index.json context/meetings/index.json
cp templates/demo/speaker_mappings.json context/meetings/speaker_mappings.json
cp templates/demo/project_datapulse.md context/projects/datapulse-acquisition.md
cp templates/demo/project_ai_pilot.md context/projects/ai-pilot-program.md
```

Then run `session-starter` to show a realistic morning briefing with:
- Overdue promises
- Upcoming deadlines
- Active projects
- Waiting-for items

## When to use

- Demonstrating the system to potential clients
- Testing agents and workflows
- Onboarding new team members

## To reset

```bash
git checkout -- context/ tasks/
```
