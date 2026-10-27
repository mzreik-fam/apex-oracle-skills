---
name: apex-dev
description: Build, change, validate and deploy Oracle APEX applications from code, including APEXlang (APEX's text-based source format) and SQLcl `apex export`, `apex validate` and `apex import`. Use this whenever the task mentions Oracle APEX, APEXlang, an APEX page, region, interactive grid, interactive report, LOV, page item, process or server-side condition, importing or exporting an APEX app, or changing an APEX app that people also edit in the browser, even if the user does not say "skill". It carries the deploy workflow that avoids overwriting other people's browser edits, the version check, and the list of mistakes that waste hours.
---

# Oracle APEX development

APEX apps are edited by two parties: you in source files, and other people in the browser (headings, columns, inline CSS, saved reports). Importing source replaces the whole app, so anything a person changed in the browser and you did not export is silently lost. Most of this skill exists to prevent that.

## 1. Check versions first

Run both queries on the connected database and compare with `references/versions.md`:

```sql
select banner_full from v$version;
select version_no from apex_release;
```

The notes in `references/` were written for APEX 26.1 and Oracle Database 26ai. If the version differs, read the official documentation for that version (links in `references/docs-links.md`) before relying on them, and tell the user which parts may be out of date.

## 2. The deploy workflow (never skip the export)

1. **Export the live app** to a dated folder: `apex export -applicationid <id> -exptype APEXLANG -dir backups/live-<time>`
2. **Compare** the live export with your source for the pages you will touch (headings, columns, SQL, conditions, inline CSS, region names). Anything that differs is somebody's edit. Take the live file as the base and make your change on top of it.
3. **Validate**: `apex validate -input <source dir> -workspace <workspace>`. Fix every error; warnings about slots usually mean a wrong slot name.
4. **Import**: `set autocommit off`, then `apex import -input <source dir> -workspace <workspace> -name <APPLICATION NAME>`. The `-name` value becomes the application name shown in the header, so pass the real app name, never the SQLcl connection name.
5. **Verify** against the dictionary, not by eye: `select region_name, condition_expression1 from apex_application_page_regions where application_id = <id> and page_id = <n>`.
6. **Tell the user** that private saved reports and personal column choices are not in an export and reset on import.

`scripts/deploy_safe.sh` does steps 1, 3 and 4 with settings from environment variables. Use the SQLcl command line for the import: the SQLcl MCP tool forces autocommit on and fails with ORA-17274.

## 3. Writing APEXlang

- Start from `references/apexlang-quickref.md`: verified patterns for pages, grids, reports, LOVs, items, processes, conditions and dialogs.
- Read `references/gotchas.md` before writing anything new. Each entry is an error someone already paid for.
- For a property you have not used before, do not guess. Generate the full property reference from the local SQLcl install with `python3 scripts/build_apexlang_reference.py` and search it. A wrong value usually makes the validator list the valid values, which is a quick way to learn them.
- The validator accepts text that is not what you meant (for example `item: @P1_X` is stored as the literal text "@P1_X"). After deploying a condition, check what was stored (step 5).

## 4. Hand-offs

- How the screen should look and behave: use `apex-ux`.
- Packages, procedures, triggers and scripts behind the screen: use `oracle-plsql`.
- New tables or a data model: use `oracle-design`.
- Before telling anyone it is finished: use `apex-audit`.

## 5. Rules that keep teams out of trouble

- Develop on the dev environment first. Do not import into production, or push to a shared branch, without the owner's explicit OK in the conversation.
- Change only what was asked. If you notice something else, report it separately.
- State what will change before changing it, especially for imports, which affect every user of the app.
- Keep configuration (ids, thresholds, rules) in tables people can edit, not in code.
