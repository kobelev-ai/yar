---
name: setup
description: Run the setup wizard to initialize your personalized workspace
user_invocable: true
---

# /setup — Initial Workspace Setup

Launch the setup wizard agent to configure your Yar.

The wizard will:
1. Ask you 5-7 questions about your role, projects, and preferences
2. Generate your personalized configuration files
3. Set up integrations (Plaud transcript fetcher, etc.)
4. Create your task management system with initial tasks

## How to run

Use the Agent tool to launch the `setup-wizard` agent:

```
Launch agent: setup-wizard
Prompt: "Run the full setup wizard. Ask questions one at a time, generate all workspace files from the answers."
```

## When to use

- First time setting up the workspace
- After a clean install
- To reconfigure (will overwrite existing files — confirm with user first)
