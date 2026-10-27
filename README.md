# apex-oracle-skills

Skills that make an AI coding assistant a careful Oracle APEX and Oracle Database developer. They work with Claude Code, and the same Markdown files work in other assistants (Codex, Cursor, Copilot and others) that read `AGENTS.md` or a skills folder.

> **Using an AI assistant? Just tell it:** *"Install https://github.com/mzreik-fam/apex-oracle-skills following INSTALL.md"*. The steps in `INSTALL.md` are written for the assistant, and it will report what it installed.

## What you get

| Skill | Use it when |
|---|---|
| **apex-dev** | Building, changing and deploying an APEX app, APEXlang, SQLcl `apex export / validate / import`. Contains the safe deploy workflow, a verified syntax quick reference, and a list of mistakes that cost hours. |
| **apex-ux** | Making screens clear for end users: headings, filters, locked versus editable fields, grid versus report, dialogs. Includes a checklist. |
| **oracle-plsql** | Packages, procedures, triggers, scripts, JSON and HTML in PL/SQL, ORA- and PLS- errors. |
| **oracle-design** | Analysis and data model before building: keys, duplicates, raw data, rules as data. |
| **conventions-setup** | Setting up your own company rules once (naming, audit columns, environments, approvals, wording). All other skills then follow them. |
| **apex-audit** | Review before release: scripted checks on the live APEX export and the schema, plus a report format. |

The assistant picks the right skill from what you ask. You can also name one: "use apex-audit on this app".

## Make it follow your company rules (do this once per team)

Every company names things and approves releases differently. The skills ship with sensible defaults; your own rules live in one file in **your** project repository, so the whole team shares them.

1. After installing, ask your assistant: **"set up our conventions"** (it uses the `conventions-setup` skill). It reads your database and project to guess your naming, then asks a few short questions with a default for each.
2. It writes `apex-oracle-conventions.md` in your project root. Commit it.
3. From then on every skill looks for that file first and follows it. Where it differs from a default, your file wins. `apex-audit` checks your work against it.

Prefer to fill it by hand? Copy `skills/conventions-setup/templates/conventions.template.md` to `apex-oracle-conventions.md` in your project and edit it. To change a rule later, edit the file (or ask the assistant to).

You can also fork this repository and edit the defaults in the skills if you want your company-wide changes to apply to every project.

## Install (Claude Code), 2 commands

```
claude plugin marketplace add mzreik-fam/apex-oracle-skills
claude plugin install apex-oracle-skills@apex-oracle-skills
```
Or inside a Claude Code session: `/plugin marketplace add mzreik-fam/apex-oracle-skills`, then `/plugin install apex-oracle-skills@apex-oracle-skills`.

Update later: `claude plugin marketplace update apex-oracle-skills`, then reinstall or update the plugin.

## Install in other assistants

The skills are plain Markdown, so any tool can use them.
1. Clone: `git clone https://github.com/mzreik-fam/apex-oracle-skills`
2. Either
   - copy the folders in `skills/` into your tool's skills folder (for Codex this is `~/.codex/skills/`; check your tool's documentation for the exact location and format), or
   - put `AGENTS.md` at the root of your project. It tells any assistant that reads `AGENTS.md` which `SKILL.md` to open for which task. Keep the `skills/` folder next to it.

These instructions for non-Claude tools are not tested by the author. If your tool needs a different layout, the content of each skill is the same.

## What you need on your machine

- **SQLcl 26.x** (includes the APEX commands and the APEXlang compiler). Check with `sql -V`.
- A saved connection to your dev database: in SQLcl, `conn -save <name> <user>/<password>@<tns or wallet>` (use your own secure way of keeping the password; never paste it into chat).
- An APEX workspace on the database. The notes are written for **APEX 26.1** and **Oracle Database 26ai**; the skills tell the assistant to check your versions and read the official documentation if they differ.
- Optional: the SQLcl MCP server, so the assistant can query the database directly (`sql -mcp`, see the SQLcl documentation).
- Optional but recommended: generate the full property reference for your own SQLcl version:
  ```
  python3 skills/apex-dev/scripts/build_apexlang_reference.py
  ```
  It reads the APEXlang compiler that ships with your SQLcl and writes `skills/apex-dev/references/apexlang-reference.md`. That file is not stored in this repository.

## How it works

Each skill has a short `SKILL.md` (when to use it and the steps) and a `references/` folder the assistant opens only when needed, so it stays fast and focused. Scripts do the repeatable checks:
- `skills/apex-dev/scripts/deploy_safe.sh` exports the live app, asks you to compare, validates, then imports.
- `skills/apex-audit/scripts/audit_apex_export.py <export folder>` checks an APEXlang export.
- `skills/apex-audit/scripts/schema_checks.sql` checks the schema.

## Try it

Prompts to test the skills are in `evals/evals.json`. Ask your assistant the prompt, with and without the plugin installed, and compare the answers with the listed expectations.

## Rules baked into the skills

- Export the live app before every deploy; people edit in the browser.
- Develop on dev first; do not release or push to a shared branch without the owner's OK.
- Change only what was asked, and say what will change before changing it.
- Keep configuration in tables people can edit, not in code.
- Never put passwords or keys in code, scripts or chat.

## Contributing

Found a new mistake or a better pattern? Add it to `skills/apex-dev/references/gotchas.md` (symptom, cause, fix) and open a pull request. Note the APEX and database version it was verified on.

## License

MIT. See `LICENSE`.
