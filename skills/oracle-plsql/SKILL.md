---
name: oracle-plsql
description: Write, review and test Oracle PL/SQL: packages, procedures, functions, triggers, views and SQL scripts (including scripts run through SQLcl or deployed with an APEX app). Use whenever the user asks for database logic, a package or procedure, a data load or merge, an API wrapper with UTL_HTTP, generated HTML in PL/SQL, JSON handling with JSON_TABLE, a migration or DDL script, or when an ORA- or PLS- error appears, even if they only describe the behaviour they want.
---

# Oracle PL/SQL

## Company conventions (read first)

Look for `apex-oracle-conventions.md` in the project root (also `docs/` and `.claude/`). If it exists, read the sections relevant to the task and follow them: where it differs from a default below, **the company file wins**. If it does not exist, use the defaults in this skill and mention once that the `conventions-setup` skill can create the file.

Code behind a screen is read, changed and debugged by other people later. Write it so the next person can trust it: small, named for what it does, safe to run twice, and failing loudly with a message that says what to do.

## How to work

1. **Understand the task and the data first.** Look at the real tables and a few real rows; do not design from the table names. Count before you pull (`select count(*)`), filter, and page. Never read a whole large table to inspect it.
2. **State what will change before you change it.** Say which objects you will create or alter.
3. **Develop on dev.** Do not run against production without the owner's explicit OK in the conversation.
4. **Leave one runnable check.** A small anonymous block with assertions, or a test script, that fails if the logic breaks.

## Style

- **Package for anything with more than one routine.** Spec = the public contract (document it in comments); body = the details. A function called from SQL must be in the spec (PLS-00231 otherwise).
- **Names say what happens:** `save_row`, `add_custom`, `remove_row`, `refresh_paths`. Parameters start with `p_`, locals with `l_`.
- **No hardcoded configuration** (ids, thresholds, rule lists, prompts): store them in a settings table people can edit. Code reads the table.
- **Idempotent scripts.** `create or replace` for code; guard DDL; a MERGE for data so reruns do not duplicate. Put `set define off` at the top of SQLcl scripts that contain `&`.
- **Audit columns** on tables people edit: `created_by`, `created_at`, `updated_by`, `updated_at`, filled by defaults and a before-update trigger; use `coalesce(sys_context('APEX$SESSION','APP_USER'), sys_context('USERENV','PROXY_USER'), user)` for the user.
- **Bind variables in dynamic SQL**; never concatenate user input. Escape output you put in HTML with `apex_escape.html`.
- **Errors:** `raise_application_error(-20xxx, 'what is wrong and what to do')` for rules a person can break (loop in a tree, deleting a protected row). Do not write `when others then null`. If you catch an error, log it and re-raise or return a clear status.
- **Commits:** the caller owns the transaction. A low-level routine that commits cannot be reused or tested safely. If a routine must commit (batch loads, scheduler jobs), say so in its header comment and name it accordingly.
- **Set-based over row-by-row.** One MERGE beats a loop of inserts. Use bulk operations when a loop is unavoidable.
- **Generated long text** (HTML, JSON): append to a CLOB with `dbms_lob.writeappend` through a small helper, never one big concatenation (breaks past 32 KB).
- **JSON:** `JSON_TABLE` cannot be chained on its own output (ORA-40556); stage the JSON in a work table first.
- **Never put secrets in code, scripts or chat.** Read them from a secure table or environment.

## Template: an editable-row save procedure

```sql
create or replace package body loc_edit as
    procedure save_row(p_location_id in number, p_parent_id in number, p_name in varchar2) is
        l_old locations%rowtype;
    begin
        select * into l_old from locations where location_id = p_location_id;       -- raises NO_DATA_FOUND for a bad id
        if p_parent_id = p_location_id then
            raise_application_error(-20001, 'A location cannot be its own parent');
        end if;
        update locations
           set parent_id = p_parent_id, name_en = p_name,
               updated_by = coalesce(sys_context('APEX$SESSION','APP_USER'), user), updated_at = systimestamp
         where location_id = p_location_id;
    end save_row;
end loc_edit;
/
```

## Test pattern

```sql
set serveroutput on
declare l_n number;
begin
    my_pkg.save_row(1, null, 'X');
    select count(*) into l_n from locations where location_id = 1 and name_en = 'X';
    if l_n <> 1 then raise_application_error(-20999, 'save_row did not store the name'); end if;
    dbms_output.put_line('save_row ok');
end;
/
```
If anything the test calls commits, the test cannot be rolled back: clean up explicitly.

## Hand-offs

Table design: `oracle-design`. The APEX side: `apex-dev` and `apex-ux`. Review before release: `apex-audit`. Known ORA/PLS traps with their fixes: `references/plsql-gotchas.md`.
