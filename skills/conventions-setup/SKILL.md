---
name: conventions-setup
description: Create or update the company or team conventions file (`apex-oracle-conventions.md`) that the other skills follow: naming rules, audit columns, environments and approvals, PL/SQL and APEX standards, UX wording, security, release rules. Use when the user says "set up our conventions", "our company rules", "onboard my team", "make the assistant follow our standards", or when another skill finds no conventions file and the user wants one, or when conventions change.
---

# Set up the team's conventions

The other skills ship sensible defaults, but every company names things and approves releases differently. One file in the project, shared through git, makes every developer's assistant follow the same rules. It is faster for people to answer 15 questions once than to correct the assistant every day.

## Steps

1. **Look for an existing file**: `apex-oracle-conventions.md` in the project root (also check `docs/` and `.claude/`). If it exists, show what is filled and what is still `<...>`, and ask what to change instead of starting over.
2. **Learn what already exists before asking.** Where you can query the database or read the repository, infer instead of asking, then confirm:
   ```sql
   select table_name from user_tables order by 1;                       -- naming style, prefixes
   select distinct column_name from user_tab_columns where column_name like 'CREATED%' or column_name like 'UPDATED%';  -- audit columns
   select constraint_name, constraint_type from user_constraints where constraint_name not like 'SYS%' fetch first 30 rows only;  -- constraint naming
   select distinct object_type, substr(object_name,1,instr(object_name||'_','_')) prefix from user_objects;  -- package and procedure prefixes
   ```
   From an APEXlang export: page numbering, item and region naming, templates, authentication. From the repo: folder layout and branch rules.
3. **Interview in short rounds** (3 to 5 questions per round, each with a recommended default; "default" is a valid answer):
   - Round 1, environments: names of dev/test/prod, who approves a release, the SQLcl connection names (never the passwords).
   - Round 2, naming and tables: table and column style, key and constraint names, id style, audit columns, delete policy.
   - Round 3, code: commit policy, error code ranges, logging, tests, formatting.
   - Round 4, screens: glossary of business words, rows per page, who may edit what, language and right-to-left, accessibility level, brand.
   - Round 5, security and release: where secrets live, roles, what blocks a release, who reviews.
   Do not ask about anything you inferred with confidence in step 2; confirm it in one line instead.
4. **Write the file** from `templates/conventions.template.md`, replacing every `<...>` you have an answer for. Keep the headings so the other skills can find sections. Leave `(default)` where the user took the default, and leave `<...>` where they did not know yet; say which sections are still open.
5. **Tell the user** to commit the file to the project repository so the whole team shares it, and that changing a rule later is just editing the file (or asking you to update it).
6. **Check it works**: pick one rule (for example the audit columns) and show how you would apply it to a new table.

## Rules for yourself

- Do not invent company rules. Unknown is better than guessed; leave it open and say so.
- Never write passwords, keys or tokens into the file; store only where they live.
- If the user's answer contradicts a default that protects data (for example "commit inside every procedure"), write what they asked and add a one-line note of the risk.
