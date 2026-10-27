# Install instructions (written for an AI assistant)

If a user gave you this repository's link and asked you to install it, follow these steps in order. The skills are Markdown and a few scripts; installing them does not change any database.

## 0. Before you start
- Tell the user in one or two lines what you are about to install and where (a user-wide plugin or a copy in this project). If they did not say, use the default for their tool below.
- Do not ask for, print or store passwords or keys. Do not change settings other than the installation itself.

## 1. Detect which tool you are running in, then install

**Claude Code** (default: user-wide plugin)
```
claude plugin marketplace add mzreik-fam/apex-oracle-skills
claude plugin install apex-oracle-skills@apex-oracle-skills
```
If you cannot run `claude` commands from your shell, tell the user to type these two lines inside Claude Code instead: `/plugin marketplace add mzreik-fam/apex-oracle-skills` and `/plugin install apex-oracle-skills@apex-oracle-skills`. A new session may be needed before the skills appear.

**Codex or another tool with a skills folder**
1. `git clone --depth 1 https://github.com/mzreik-fam/apex-oracle-skills /tmp/apex-oracle-skills`
2. Copy every folder inside `skills/` into the tool's skills folder (Codex: `~/.codex/skills/`; check the tool's documentation if you are unsure). Keep each skill folder whole, including `references/` and `scripts/`.
3. Put `AGENTS.md` in the project root only if the project has none. If one exists, add a short section that points to the skills; never overwrite the user's file.

**Any other assistant**
1. Clone the repository into the project, for example into `.apex-oracle-skills/`.
2. Add `AGENTS.md` to the project root (or merge its table into the existing one) so that the assistant opens the right `SKILL.md` per task. Adjust the paths to where you cloned.

## 2. Check it worked
List the installed skills. You should see: `apex-dev`, `apex-ux`, `oracle-plsql`, `oracle-design`, `apex-audit`, `conventions-setup`. Each folder must contain a `SKILL.md`.

## 3. Check what the user still needs (report it, do not install it silently)
- SQLcl 26.x: run `sql -V`. If it is missing, point the user to Oracle's SQLcl download page.
- A saved database connection: the user creates it themselves with `conn -save <name> <user>/<password>@<service>` in SQLcl. Never ask them to paste the password to you.
- An APEX workspace on that database, and which APEX and database versions it runs (the `apex-dev` skill checks this itself).

## 4. Offer the next step
Tell the user: "To make me follow your company's rules, say **set up our conventions**." That runs the `conventions-setup` skill and writes `apex-oracle-conventions.md` in the project, which the whole team should commit.

## 5. Report back
Say plainly what you installed, where, and what you could not do. If a step failed, show the error and stop instead of trying unrelated workarounds.
