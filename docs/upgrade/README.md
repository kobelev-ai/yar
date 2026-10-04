# Upgrade an existing Yar workspace to 3.0

User data is separate from the Git distribution. Ignored files aren't backed up
by Git. Make and verify a separate backup of the **whole workspace**, including
ignored sources, tasks, indexes, memory and custom instructions, before updating.
Keep your original copy until the upgraded workspace has been checked.

## Update distribution files

Check `git status` before fetching. Preserve local changes to instructions and
integrations. Fetch and merge distribution updates normally; resolve conflicting
customizations deliberately. Don't use git reset/checkout to discard owner files
and don't stage everything into the public repository. If you don't use Git,
copy updated distribution files into a separate copy of the workspace first.

## Preview and migrate data paths

From the selected workspace root:

```bash
python3 scripts/yar_workspace.py migrate
python3 scripts/yar_workspace.py migrate --apply
```

The first command previews moves. Applying them changes:

- `tasks/todo.md` → `ops/tasks/todo.md`
- files under `tasks/archive/` → `ops/tasks/archive/`
- files under `context/meetings/` → `ops/meetings/`

Before moves, all affected originals are copied to a verified local backup under
`.yar/backups/`. If source and destination conflict, the entire migration stops
before moving anything. Symlink inputs are refused. Relative meeting paths in the
JSON index and speaker map are updated; original bytes are kept in the backup.
A manifest records old/new paths and SHA-256. Initialization creates only missing
operational files, queues and instance state; existing contents stay intact.
Repeated runs do not create another action list or reset current data.

The helper doesn't rewrite arbitrary historical documents, customized integration
scripts or paths in external services. After migration, inspect references to
`tasks/todo.md` and `context/meetings/` in your customized files and update their
technical links as needed. Update any configured transcript fetcher's
`MEETINGS_PROCESSED` path to `ops/meetings/processed/` (and restart your scheduler
only after checking its actual configuration). If the index contains absolute
paths or an unusual schema, open its records and check migrated links before use.

## Check the result

Open todo and compare its items/statuses with your backup. Check original
transcripts and indexed paths, queues and a real task folder. Open a new session
in a task folder and confirm it finds the workspace, current result and sources.
Owner data should not appear in `git status` for a publication commit. Existing
tracked owner files may require explicitly removing them from the Git index after
backing them up; an ignore rule alone doesn't untrack a file.

## Restore if necessary

The migration manifest and verified originals are in the printed backup directory.
On an ordinary error the helper restores the files it moved. After interruption,
compare current files with the manifest and restore only the necessary originals
into a separate recovery copy. Don't overwrite newer work with a whole old snapshot.
Demo workspaces can be opened independently and never serve as a data backup.
