# Yar Version

**Current version:** 2.3
**Installed:** 2026-04-16
**Last updated:** 2026-05-13

## Update history

### v2.3 (2026-05-13)
- Renamed `tasks/gtd.md` → `tasks/todo.md` (no data loss — file hadn't been created yet in this install)
- Renamed agent `gtd-processor` → `todo-processor`
- Renamed `templates/gtd.md.template` → `templates/todo.md.template`
- Renamed `templates/demo/gtd.md` → `templates/demo/todo.md`
- Removed "GTD" jargon from user-facing headings (README, CLAUDE.md, skills) — kept one methodology reference in `/review` skill
- README: removed 4 dead agents (`speaker-identifier`, `promise-extractor`, `daily-planner`, `self-memory`) that were already killed in v2.2 but still listed
- CLAUDE.md version bumped 2.0 → 2.3
- Migration plan: `.yar/migrations/003-v2.3-gtd-to-todo.md`
- **Still deferred to v2.4+:** Step 3.5 cross-check (closure signal), permission allowlist template in setup-wizard, channels setup guide for TG-based clients

### v2.2 (2026-05-13)
- Killed 4 standalone subagents (duplicate logic, already inline in meeting-processor): `daily-planner`, `promise-extractor`, `self-memory`, `speaker-identifier`
- `.gitignore` hardening: added `*.log`, `*.lock`, `.mcp.json`, `node_modules/`, `.venv/`, `venv/`, `.next/`, `dist/`, `build/`, `*.swp`, `Thumbs.db`
- Hygiene: removed tracked `.DS_Store`
- Migration plan: `.yar/migrations/002-v2.2-agent-cleanup.md`

### v2.1 (2026-04-16)
- Added package system (recipes with frontmatter `type: yar-recipe`)
- New skill: `/pkg_installer` — installs packages, records to `.yar/installed.md`
- Updated `/inbox` to detect recipes and delegate to `/pkg_installer`
- New system folder `.yar/` for installation state

### v2.0 (2026-04-16)
- Renamed from Helm to Yar
- Folder `helm/` → `yar/`

### v1.0 (2026-03-29)
- Initial release as Helm
- 8 agents, 6 skills (setup, demo, inbox, brief, status, review)
- Single inbox, collector behavior, boundaries

---

## Update commands (future)

```bash
# Check for updates (when distribution is on GitHub)
git fetch origin
git log HEAD..origin/main --oneline

# Apply updates (runs any new migrations from .yar/migrations/)
/update
```
