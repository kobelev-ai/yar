# Yar — a folder that helps you get work done

Put materials in a folder, ask your assistant for a result, and continue from the
saved work next time. Yar adds rules, a simple work structure and source-based
memory to your own files. The reasoning model and the application can change;
your materials and results remain yours.

## Start with one real task

Clone this repository and open the folder in your agent application:

```bash
git clone https://github.com/kobelev-ai/yar.git my-assistant
cd my-assistant
```

Create a folder in `tasks/` and drop in the materials:

```text
tasks/
  Compare_proposals/
    Proposal A.pdf
    Proposal B.xlsx
    Requirements.txt
```

Tell the assistant: **“Read the Yar rules. Compare the proposals in
`tasks/Compare_proposals`: cost, scope and deadlines. Save a comparison and
recommendation in that folder, and list what we still need to know.”**

No task form is required. The assistant preserves the inputs, saves the result
and maintains a short README with the current status and where to continue.
Nested folders are welcome. Other folders can also be selected as work contexts.
File formats depend on the tools available in your agent application.

## Applications and setup

- **Claude Code:** reads `CLAUDE.md`; workflows are in `.claude/skills/<name>/SKILL.md`.
  Start `claude` and say `/setup`, or simply ask to configure Yar and do your task.
- **Codex:** reads `AGENTS.md`. Ask it to set up Yar or solve a folder task in
  plain language. This distribution doesn't require Claude-specific subagents.
- **Other folder-enabled assistants:** give access to the folder and explicitly
  ask them to read `AGENTS.md`. Check file/tool support and permissions first.
  Native commands and automatic instruction loading vary by application.

Setup asks your name, preferred language and first task. You can fill in the
rest of your profile, projects and goals as you work. It creates only missing
workspace files and preserves existing tasks, memory and source materials.
Python 3.10+ is needed for the optional setup, demo and upgrade helper:

```bash
python3 scripts/yar_workspace.py init
```

## Three things to remember

- `tasks/` — **“Here are the materials; help me produce this result.”**
- `inbox/` — **“This arrived; help me figure out where it belongs.”**
- `ops/tasks/todo.md` — your single list of actions, promises and things awaited.

After a work session, the current result is linked from its task or project
README. Say “continue the proposal comparison” to resume. A requested briefing
checks dated records instead of treating an old focus or plan as today's.

## Try a demo

Ask `/demo` in Claude Code or “create an isolated Yar demo” in another assistant:

```bash
python3 scripts/yar_workspace.py demo
```

The helper creates a separate workspace under `demos/` and prints its path.
Open that folder to compare two fictional supplier proposals. Your real profile,
tasks and meeting files remain in your main workspace. Demo data is synthetic;
the assistant still has to perform the comparison.

## Workflows

| Request | What happens |
|---|---|
| “Solve this folder task” / `/task <folder>` | Read sources, produce a checked artifact, save a continuation pointer |
| “Process inbox” / `/inbox` | Route loose inputs and bundles; preserve originals |
| “Process this meeting” | Index the source, produce a summary, extract actions and confirmation candidates |
| “Give me a briefing” | Review relevant tasks, dates, goals and waiting-for items |
| `/status`, `/brief <project>`, `/review` | Overview, project brief and confirmed review of open work |
| “Install this recipe” / `/pkg-installer <file>` | Authorized installation, prerequisites and package record |

Slash commands above are Claude Code workflows. Other assistants can follow the
same workflow files through a plain-language request and available tools.

## Structure

```text
tasks/                    Work folders: inputs, results, current README
inbox/                    Incoming files and bundles
ops/
  tasks/todo.md           Actions and commitments
  tasks/review/           Candidates awaiting owner confirmation
  meetings/               Transcript originals, summaries and index
context/                  Profile, confirmed memory, projects, people and goals
.yar/                     Distribution version and local instance state
.claude/                  Claude Code workflows and agents
AGENTS.md                 Shared work contract for folder-enabled agents
scripts/                  Optional workspace helper and integrations
templates/                Empty templates and fictional demo inputs
```

## Memory with sources

Yar keeps original transcripts and documents alongside derived summaries. It
uses indexes and current pointers to find relevant evidence. Decisions about
personal memory and possible completion signals extracted from meetings are
kept in separate queues until you confirm them. Direct explicit instructions
in a conversation can be recorded immediately.

A larger archive can improve answers when the assistant finds the right source
and checks its date. Keeping files alone doesn't guarantee recall or accuracy.

## Data, backups and updates

The repository contains the distribution and synthetic examples. Workspace data
is excluded from Git by default. Git history does **not** back up ignored files;
make a separate backup of the whole working folder. The helper makes a verified
local backup of files it moves during an upgrade. See [upgrade instructions](docs/upgrade/README.md).

Files are stored in your folder. When using a cloud model, the application may
send relevant file contents to that provider. Sync, storage and model processing
are separate choices. Define processing boundaries in `context/me/boundaries.md`.

Switching models keeps the files. Switching applications also requires checking
instruction loading, tools, supported formats and access to the workspace.

## Extending Yar

Add a task, a project or an authorized recipe. Workflows are plain Markdown;
adapt them to your role. [Folder-task workflow](.claude/skills/task/SKILL.md) and
[upgrade guide](docs/upgrade/README.md) describe the working rules. Optional
transcript fetching uses `scripts/plaud_fetcher/` and is configured separately.

## License

MIT
