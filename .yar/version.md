# Yar Version

**Distribution version:** 3.1
**Released:** 2026-10-14

## 3.1 — separate task work folders from GTD

- Work materials and results stay in `tasks/<name>/`; action tracking lives in `ops/gtd/`.
- Setup, demos, workflow instructions and data exclusions use `ops/gtd/todo.md`.
- Verified migration moves Yar 3.0 data from `ops/tasks/`, preserving custom queues,
  original files and backups. Yar 2.3 can migrate directly to the same layout.

## 3.0 — folder tasks and durable context

- Work folders under `tasks/`, checked artifacts and README continuation pointers.
- Single operational list at `ops/tasks/todo.md`; separate confirmation queues.
- Preserved originals in inbox/meetings; summaries and normalized transcripts are derivatives.
- Task-first setup, create-if-missing initialization and isolated synthetic demos.
- Generic matching AGENTS/CLAUDE contracts; workflows use standard SKILL.md folders.
- Owner data excluded from distribution; separate data-backup and upgrade instructions.
- Optional tested Python workspace/migration helper with conflict checks and verified backups.

Older distribution: 2.3 (2026-05-13). The [upgrade guide](../docs/upgrade/README.md)
explains preserving owner data and migrating old operational paths. Instance-specific
history and package records are local files, created during setup or migration.
