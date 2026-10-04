---
name: demo
description: Create a separate fictional Yar workspace for demonstration without altering the owner's files.
---

# Isolated demo

Read the root contract. Run `python3 scripts/yar_workspace.py demo` from the selected
workspace. It prints the location of a new workspace under `demos/`. Open that folder
as a separate project, or explicitly set YAR_ROOT to that location for the demonstration.
All reads and writes of profile, todo, queues, meetings and tasks belong to the demo.
Don't process the main inbox, call real integrations or send any messages.

The demo contains `tasks/Compare_proposals/` with two fictional offers and requirements.
Use the task workflow to compare the total first-year cost and requirement coverage,
then save the result and README in the demo folder. Explain that the inputs are synthetic.
Don't copy demo profiles or indexes into the live workspace and don't use git checkout
as a reset. A rerun creates another fresh workspace; removal is a separate owner action.
