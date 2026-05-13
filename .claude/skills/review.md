---
name: review
description: Interactive weekly review — process, archive, plan next week
user_invocable: true
---

# /review — Weekly Review

Run an interactive weekly review following the Getting Things Done (GTD) methodology by David Allen.

## Checklist

Walk the user through each step interactively:

### 1. Get Clear
- Process global `inbox/` to zero (use /inbox logic)
- Ask: "Anything else on your mind that's not captured?"

### 2. Get Current
- Show Next Actions — ask which are still relevant
- Show Waiting For — ask which to follow up on
- Show Projects — update statuses
- Check calendar for next week (if available)

### 3. Promise Audit
- List all `**[PROMISE]**` items
- Flag overdue (>deadline or >14 days)
- For each: Done / Redate / Follow-up / Drop

### 4. Zombie Detection
- Find tasks with `[added:]` older than 14 days
- For each: **K**(ill) / **S**(omeday) / **R**(edate)

### 5. Someday Rotation
- Pick 5 random items from Someday/Maybe
- For each: **P**(romote to Next Actions) / **K**(eep) / **D**(rop)

### 6. Ideas Review
- Show recent items from `context/me/ideas.md`
- For each: **A**(ctionable → create task) / **K**(eep) / **D**(rop)

### 7. Archive
- Move Done items to `tasks/archive/YYYY-WXX.md`
- Clear Done section in todo.md
- Commit: `git add -A && git commit -m "weekly review WXX"`

### 8. Plan Next Week
- Ask: "What are your top 3 priorities for next week?"
- Update `context/goals/weekly.md`

## Format

Present each section as a batch — show items with checkboxes, let the user confirm/modify in bulk. Don't go one-by-one unless the user prefers it.

Show summary at the end:
```
Weekly Review Complete:
- Processed: [N] inbox items
- Archived: [N] done tasks
- Killed: [N] zombies
- Promoted: [N] from someday
- Ideas reviewed: [N]
- Promises: [N] active, [X] overdue
- Next week focus: [goals]
```
