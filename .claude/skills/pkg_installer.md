---
name: pkg_installer
description: Install Yar packages (recipes) from .md files with frontmatter type yar-recipe. Guides the owner through setup, tracks installation in .yar/installed.md.
user_invocable: true
---

# /pkg_installer — Install Yar Package

Installs a Yar package (recipe) delivered as a `.md` file with YAML frontmatter `type: yar-recipe`.

Usually called automatically by `/inbox` when it detects a recipe file. Can also be invoked directly with a file path.

## When to use

- `/inbox` detected a file with frontmatter `type: yar-recipe`
- Owner says "install this package" / "install this recipe" / "обработай рецепт"
- Owner drops a recipe file and explicitly asks to install it

## Input

A `.md` file with frontmatter like:

```yaml
---
type: yar-recipe
recipe_id: email-calendar
version: 2.0
client: Vladimir
created: 2026-04-16
prerequisites: [node.js, google-account]
---
```

## Installation flow

### Step 1: Parse frontmatter

Read the file, extract:
- `recipe_id` (required) — unique identifier
- `version` (required) — semantic version
- `prerequisites` (optional) — list of system requirements
- `client` (optional) — who this recipe is for
- `created` (optional) — generation date

If frontmatter missing or `type != yar-recipe` → abort, tell the owner this is not a valid package.

### Step 2: Check if already installed

Read `.yar/installed.md`. If `recipe_id` already present:
- Same version → "Package {id} v{ver} already installed on {date}. Reinstall? (y/n)"
- Older version → "Package {id} v{old} installed, upgrading to v{new}. Continue?"
- Newer version → warn "You have v{new} installed, this file is v{old}. Downgrade?"

### Step 3: Check prerequisites

For each item in `prerequisites`:
- `node.js` → run `node --version`, if missing tell owner to install from nodejs.org
- `python3` → run `python3 --version`
- `google-account` → just confirmation, no check
- `imap-access` → confirmation
- Custom strings → present to owner, ask "Do you have {X}? (y/n)"

If any prerequisite missing → **stop installation** and show what needs to be set up first. Tell the owner: "Install these prerequisites, then run /pkg_installer again."

### Step 4: Run the recipe

The body of the recipe file after frontmatter contains the actual instructions. These are written in Russian/English as conversational steps for the owner.

**Your job as pkg_installer:**
- Read the body section by section
- Guide the owner step by step — ask questions as they appear in the recipe
- Execute commands from the "Техническая часть / Technical section" automatically (scripts, file creation, permissions)
- When the recipe says "Скажи Яру: X" — that's what the owner would normally say; since we're already in the install flow, interpret it as "the owner is asking you to do X now"
- Follow the recipe's "Настройка поведения / Behavior setup" section — ask those questions, record answers to `context/me/preferences.md`

### Step 5: Record installation

After successful install, update `.yar/installed.md`:

```markdown
## {recipe_id} v{version}
- **Installed:** YYYY-MM-DD
- **Source:** {client field or "manual"}
- **Prerequisites:** {list, all ✓}
- **Behavior config:** see context/me/preferences.md section "{recipe_id}"
- **Files changed:** list of files created/modified
- **MCP servers added:** {list if any}
- **Scripts added:** {list if any}
```

Also update the summary table at the top of `.yar/installed.md`:

```markdown
| ID | Version | Installed | Status |
|----|---------|-----------|--------|
| email-calendar | 2.0 | 2026-04-16 | active |
```

### Step 6: Archive the recipe

Move the recipe file:
- From: `inbox/<filename>.md`
- To: `.yar/packages/{recipe_id}_v{version}.md`

This preserves the full recipe text for future reference (audit, reinstall, uninstall).

### Step 7: Report to owner

Show a clear summary:

```
Package installed: {recipe_id} v{version}

What's working now:
- [capability 1]
- [capability 2]

Files added/changed:
- file1
- file2

To use: say "{trigger phrase from recipe}"

Next recommended step: {if recipe has one}
```

## Rules

1. **Never skip prerequisite checks** — if something is missing, stop and tell the owner
2. **Never silently overwrite** — always confirm reinstall/upgrade/downgrade
3. **Ask when unsure** — recipes have conversational sections; don't auto-fill answers
4. **Record everything** — installation must leave a clean trail in `.yar/installed.md`
5. **Preserve the recipe** — always archive to `.yar/packages/`, never delete
6. **Keep preferences separate** — behavior answers go to `context/me/preferences.md` under a section named `{recipe_id}`, NOT to `.yar/` (that's for system state, not personal settings)

## Errors & Recovery

- **Frontmatter missing/invalid** → abort, explain what a valid recipe looks like
- **Prerequisite fails** → stop, show what to install, don't roll back partial state
- **Mid-install error** → record partial install in `.yar/installed.md` with status `failed` and list of completed steps, so reinstall can resume
- **Owner cancels** → record in `.yar/installed.md` with status `cancelled`

## Uninstall (future)

Not yet implemented. Placeholder: `/pkg_uninstall <recipe_id>` would:
- Read `.yar/packages/{recipe_id}_v{version}.md`
- Read the "Files added/changed" section from `.yar/installed.md`
- Remove those files (with confirmation)
- Remove MCP server entries from `.claude/settings.json`
- Update `.yar/installed.md` status to `uninstalled`
