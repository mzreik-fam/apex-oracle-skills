# Oracle APEX and database work in this repository

This repository holds six skills. Each is a folder in `skills/` with a `SKILL.md` and, where needed, `references/` and `scripts/`.
If your tool does not load skills by itself, read the matching `SKILL.md` before starting that kind of work:

| When the task is about | Read |
|---|---|
| Building, changing or deploying an Oracle APEX app, APEXlang, SQLcl `apex` commands | `skills/apex-dev/SKILL.md` |
| How an APEX screen should look and behave for end users | `skills/apex-ux/SKILL.md` |
| PL/SQL packages, procedures, functions, triggers, SQL scripts | `skills/oracle-plsql/SKILL.md` |
| New tables, keys, constraints, data analysis before building | `skills/oracle-design/SKILL.md` |
| Reviewing finished work before release | `skills/apex-audit/SKILL.md` |

| Setting up or changing the team's own rules (naming, audit columns, approvals) | `skills/conventions-setup/SKILL.md` |

Before any task, look for `apex-oracle-conventions.md` in the project root. If it exists, follow it; it overrides the defaults in the skills.

Two rules apply everywhere:
1. Check the database and APEX version first (queries are in `skills/apex-dev/references/versions.md`). The notes were written for APEX 26.1 and Oracle Database 26ai. If your versions differ, read the official documentation for your version and say what may be out of date.
2. People edit APEX apps in the browser. Export the live app and merge before every deploy, otherwise their work is overwritten.
