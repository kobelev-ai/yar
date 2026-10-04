---
name: review
description: Review current actions and confirmation candidates, preserve history and plan from confirmed priorities.
---

# Review

Read the current todo and the queues located by `ops/tasks/review/queues.json`.
Process requested inbox items, then review a small relevant batch of actions,
promises, waiting-for items and candidates. Verify dated sources and later results.
Let the owner confirm completion, dropping, new dates and memory/decision candidates.
Do not close a task based on an interpretation or an old focus. Apply only specifically
confirmed changes, mark the confirmation source/date in each queue and update the
canonical target. Append confirmed decisions without changing their history.
Archive confirmed Done entries to `ops/tasks/archive/YYYY-WXX.md`, preserving text
and refs. Don't automatically git commit workspace data. Review saved task results
and next steps, then update weekly priorities only from the owner's actual choices.
