# Oracle APEX and database conventions for <COMPANY / TEAM>

Fill this in once, commit it to your project repository, and every developer's AI assistant will follow it. Anything you leave
as `(default)` uses the default written in the skills. Delete lines that do not apply. Where this file and a skill disagree, **this file wins**.

Last reviewed: <date>   Owner: <name or role>   APEX version: <e.g. 26.1>   Database version: <e.g. 26ai>

## 1. Environments and approvals
- Environments (in order): <dev> -> <test> -> <prod>
- Who may deploy to each, and who must approve a release to prod: <names or roles>   (default: nothing goes to prod without the owner's explicit OK)
- Changes allowed directly on prod: <none / hotfix with approval>

## 2. Naming
- Tables: <singular|plural>, prefix/suffix rules: <e.g. no prefix; staging tables start with STG_>
- Columns: <e.g. snake_case; booleans as Y/N varchar2(1)>
- Primary key: <e.g. <table>_id>   Foreign key: <e.g. same name as the parent key>
- Constraints: <e.g. <table_abbrev>_pk, _uk, _fk, _ck>   Indexes: <e.g. <table_abbrev>_<cols>_ix>
- Packages / procedures / functions: <e.g. package per domain; verbs for procedures, nouns for functions>
- Parameters and local variables: <default: p_ and l_>
- APEX: page numbering ranges: <e.g. 1-99 admin, 100-199 customers>; region/item/static ids: <e.g. P<page>_NAME>

## 3. Table standards
- Id style: <default: number generated always as identity; no UUIDs unless asked>
- Audit columns: <default: created_by, created_at, updated_by, updated_at>
- Deleting rows: <default: Active flag; real delete only for rows users created>
- Comments on tables and columns: <required / optional>
- Where reference data and rules live: <default: settings tables editable from a screen>

## 4. PL/SQL
- Commit policy: <default: the caller owns the transaction; routines that commit say so in their header>
- Error handling: <default: raise_application_error(-20xxx, 'message'); no when others then null>   Error code ranges: <e.g. -20001..-20099 per package>
- Logging framework: <none / logger / custom table>
- Test approach: <default: one runnable check per routine; or utPLSQL>
- Formatting: <e.g. keywords lower case, 4 spaces, line length 140>

## 5. APEX standards
- Workspace and application id per environment: <...>
- Application name (used for import): <...>
- Authentication and authorization schemes: <...>
- Theme and templates: <...>
- Date, number and currency formats: <...>   Languages / right-to-left: <...>
- Source control: export format <APEXlang / SQL>, folder <...>, backups before deploy: <default: yes, export the live app first>

## 6. UX standards
- Business glossary (words users use -> words on screen): <e.g. "Property" not "Unit record">
- Default rows per page: <default: 50>   Default search and filters: <...>
- Locked versus editable rules: <default: only what users are meant to change is editable, and looks editable>
- Wording for empty states, errors, confirmations: <...>
- Accessibility level required: <e.g. WCAG 2.1 AA>   Brand colours and fonts: <...>

## 7. Security
- Where secrets live: <e.g. vault / secure table / environment>   Never in code, scripts or chat.
- Roles and who can see which data: <...>
- Escaping and input rules: <default: apex_escape.html for output, bind variables for dynamic SQL>

## 8. Release and review
- What blocks a release: <default: any MUST finding from the apex-audit skill>
- Code review needed for: <PL/SQL, APEX pages, DDL>   Reviewer: <...>
- Documentation required: <data model note, release note, none>

## 9. Notes for the assistant
Anything else a new developer should know (legacy tables not to touch, known problem areas, who to ask):
- <...>
