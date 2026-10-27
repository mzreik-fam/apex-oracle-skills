# Gotchas

Each entry is something that cost time. Format: symptom, cause, fix.

## Deploying

- **The app is renamed to the connection name after import.** `apex import -name` sets the application name. Pass the real name (for example `Locations`).
- **ORA-17274 when importing through the SQLcl MCP tool.** That connection forces autocommit on. Use the SQLcl command line with `set autocommit off`.
- **People's browser edits vanish after an import.** The import replaces the whole app. Export the live app first, compare, merge (workflow in SKILL.md).
- **Private saved reports and personal column choices reset on every import.** They are not in the export. Warn users before deploying; for a column choice that must survive, define it in the page's primary saved report (`displayColumn`).
- **ORA-00001 on `WWV_FLOW_INTERACTIVE_GRIDS` (`IG_PK`) during import.** Caused by wrapping toolbar settings in an `attributes ( ... )` child of a grid. Put `toolbar`, `edit` directly in the region. If it persists, rename the region id.
- **`DUPLICATED_COMPONENT ... endUserAlias` on validate.** Interactive report columns need unique end-user aliases; an export taken after a browser edit can contain duplicates. Assign a free alias.

## APEXlang syntax and meaning

- **Single-line `column X ( a b c )`** is a syntax error. Use multiple lines.
- **Condition never matches.** `item: @P7_VIEW` is stored as the literal text "@P7_VIEW" and validates fine. Write item names without `@`. Use `@` only for components (region, column, LOV, template).
- **Interactive report columns** need `type: plainText`, `source { dataType: STRING|NUMBER|DATE|TIMESTAMP }` (uppercase) and a heading. Grid columns use lowercase types.
- **`allowedOperations: add:update:delete` is rejected**; use a multi-line list.
- **A new view column does not appear in a region.** Regions list their columns explicitly; add the column to the region and, for grids, to `displayColumn`.
- **`pagination.type`** for an interactive report must be a valid value such as `rowRangesXToYOfZ` or `rowRangesXToYNoPagination`.
- **`success { message }` on a process** is invalid.
- **A dynamicContent region** needs `source { language: plsql  plsqlFunctionBody: ... }`.
- **Dialog pages**: use `dialogTemplate`, not `pageTemplate`, with `pageMode: modalDialog`; the body slot is `contentBody`.
- **`readOnly` on a `link` column** is invalid. Make the column a link and keep it locked, or use another column type.
- **`number` is a reserved word** and cannot be a column name.

## SQL and PL/SQL

- **SQLcl ends a statement at a blank line, and treats `&` as a substitution variable.** Strip blank lines in generated DDL and use `set define off`.
- **ORA-22998 using LENGTHB on a CLOB**; pass the HTTP body as VARCHAR2 or use `dbms_lob.getlength`.
- **ORA-40556: chained JSON_TABLE.** Stage the JSON in a work table first, then read it with a second statement.
- **ORA-06502 building long HTML.** One concatenation breaks past 32 KB. Append to a CLOB with `dbms_lob.writeappend` in a helper procedure.
- **ORA-54017 updating a virtual column** (`level_code` computed from `level_no`). Update the source column only.
- **PLS-00231: function may not be used in SQL.** A function called from SQL must be declared in the package specification.
- **PLS-00204: EXISTS or DECODE inside PL/SQL.** They are SQL-only; use `select count(*) into ...` or `case`.
- **A view created with `select t.*` freezes its column list.** After adding columns to the table, recreate the view.
- **Procedures that commit cannot be rolled back by a test.** Any helper that commits (a "refresh paths" procedure, for example) makes the whole test permanent. Assume test data stays and clean it up explicitly.
- **ORA-00001 on a unique key when the same content arrives twice in one batch.** De-duplicate the merge source before merging.
- **Do not put secrets in code or chat.** Read them from an environment variable or an env file listed in `.gitignore`.
