---
name: inbox
description: Process global inbox — auto-detect content type and route to appropriate agent
user_invocable: true
---

# /inbox — Process Global Inbox

Processes all files in the `inbox/` folder. Auto-detects content type and routes to the appropriate handler.

## How it works

1. List all files in `inbox/`
2. For each file, determine type:
   - **Yar package/recipe** (`.md` with YAML frontmatter `type: yar-recipe`) → delegate to `/pkg_installer`
   - **Meeting transcript** (long text with speaker labels, dialogue format) → launch `meeting-processor` agent
   - **Task list / notes** (short items, bullet points, to-dos) → process with `todo-processor` logic
   - **Document about a project** (report, analysis, brief) → extract key info → update `context/projects/*.md`
   - **Personal info / brain dump** (thoughts, ideas, preferences) → route to appropriate `context/me/` files
   - **Unknown** → ask the user what it is
3. After processing each file, remove it from `inbox/`
4. Show summary of what was processed

## Implementation

Read all files in `inbox/`:

```bash
ls inbox/ 2>/dev/null
```

If empty → tell the user "Inbox is empty, nothing to process."

For each file:
1. Read the file content (at least the first 20 lines to detect frontmatter)
2. Analyze: is this a Yar recipe? A meeting transcript? A task list? A document? Notes?
3. Process accordingly:

**If `.md` with YAML frontmatter `type: yar-recipe`:**
This is a Yar package. Delegate to `/pkg_installer` skill with the file path. It will parse frontmatter, check prerequisites, guide the owner through installation, and archive the recipe to `.yar/packages/`. DO NOT delete the file yourself — pkg_installer handles it.

**If meeting transcript:**
Launch `meeting-processor` agent with the file path. It will handle the full pipeline and move the file to `context/meetings/processed/`.

**If tasks/notes/brain dump:**
- Extract actionable items → add to `tasks/todo.md` (Next Actions or Inbox section)
- Extract ideas → append to `context/me/ideas.md`
- Extract promises → add as `[PROMISE]` items
- Extract waiting-for ��� add to Waiting For
- Delete the original file from inbox

**If project document:**
- Identify which project it relates to
- Update the project file in `context/projects/`
- If new project → create a new project file
- Move or delete the original

**If people info:**
- Create or update `context/people/*.md` cards
- Delete the original

## After processing

Show summary:
```
Inbox processed: [N] items

- [filename] → meeting transcript → processed (tasks: X, promises: Y)
- [filename] → brain dump → 5 tasks added, 3 ideas captured
- [filename] → project update → "Project Name" updated
```

## Rules

- Process ALL files, don't skip any
- Ask the user if you can't determine the type
- Always show what you did with each file
- Don't leave files in inbox after processing
