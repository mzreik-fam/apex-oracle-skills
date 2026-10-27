---
name: apex-audit
description: Audit an Oracle APEX application, PL/SQL code or schema before release: checks the live app export for broken conditions, duplicate aliases, unclear headings and unsafe settings, and checks the database for missing keys, audit columns, bad error handling and hardcoded values. Use when the user asks to review, audit, check, QA or "make sure everything is built properly", before telling anyone a screen or package is finished, and before a release, even if they do not say "audit".
---

# Audit before release

## Company conventions (read first)

Look for `apex-oracle-conventions.md` in the project root (also `docs/` and `.claude/`). If it exists, read the sections relevant to the task and follow them: where it differs from a default below, **the company file wins**. If it does not exist, use the defaults in this skill and mention once that the `conventions-setup` skill can create the file.

Review what actually exists, not what you remember writing. A page that looks right in the source can behave wrongly once imported (conditions stored as literal text, a column that never shows). So audit the live app and database, with evidence.

## Steps

1. **Export the live app** (see `apex-dev`) to a folder, for example `backups/audit-<date>`.
2. **Run the scripted checks**
   - `python3 scripts/audit_apex_export.py <export folder>`: flags item names written with `@` in conditions, duplicate end-user aliases, raw database names used as headings, `select *` sources, pages with no access protection, grids with edit on but no save process, and regions with no search.
   - Run `scripts/schema_checks.sql` in SQLcl against the schema: tables without a primary key, editable tables without audit columns, UUID columns, `when others then null`, hardcoded literals that look like ids, objects that are invalid.
2b. **Check against the company conventions file** (`apex-oracle-conventions.md`): turn each rule it states (naming, audit columns, error code ranges, commit policy, glossary) into a check and report breaches. No file: audit against the defaults and say so.
3. **Read the page as a user** with `apex-ux` and its checklist (`../apex-ux/references/ux-checklist.md`). Scripts catch syntax; only a person notices that a heading is confusing.
4. **Check the logic** with `oracle-plsql` and `oracle-design`: keys, error handling, commits, rules stored as data, one runnable test.
5. **Verify deployed behaviour against the dictionary**, for example `apex_application_page_regions` for conditions and `apex_application_page_proc` for processes.
6. **Report**: use the format below.

## Report format

```
Audit of <app / package / schema> on <date>, APEX <version>, DB <version>

Must fix (breaks or loses data)
1. <finding> | where: <page/object> | evidence: <query result or line> | fix: <one line>

Should fix (confusing or risky)
1. ...

Nice to have
1. ...

Checked and fine: <short list, so the reader knows what was covered>
Not checked: <what you could not reach>
```
Order by impact. Give each finding its evidence and a one-line fix. If something is only a guess, say so; do not present a suspicion as a finding.

## Principles

- **Evidence over opinion.** Quote the line, the query result or the screenshot.
- **Do not fix during the audit** unless asked: report first, because some "problems" are decisions the owner already made.
- **Say what you did not check.** An audit that hides its gaps gives false comfort.
