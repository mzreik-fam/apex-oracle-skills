---
name: oracle-design
description: Analyse a requirement and design Oracle tables, keys, constraints and settings before anything is built, or review an existing data model. Use whenever the user wants to start a new feature or app, asks how many tables to use, how to map or match records between systems, how to avoid duplicates, how to load and keep raw data, or asks for a schema, key, index or constraint design, even if they do not say "design". Do the analysis before creating objects.
---

# Oracle analysis and design

Cheap mistakes live on paper; expensive ones live in a loaded database. Spend the effort where reversing is costly: keys, what counts as a duplicate, what is stored raw, and who may change what.

## 1. Analyse before you design

1. **Look at real data.** Pull one or two real samples (a small page, a single record) and read them. Design from what the data contains, not from the field names in documentation. Count rows and distinct values; find nulls, zeros used as placeholders, and values that repeat with different meanings.
2. **Ask the owner for what only they know**: what decisions this data feeds, what a duplicate means in their business, which fields they trust. Ask few, specific questions, each with your recommended default.
3. **List what must never be lost.** If a source record can be ignored, say what rule ignores it and make the rule data, not code. When loading from an API, capture every field and every record first; filter later in views.
4. **Write the plan in plain words**: tables, keys, how rows are matched, what is raw and what is derived, and what a person can edit. Get a yes before creating anything.

## 2. Design rules (and why)

- **Normal numeric ids** (`number generated always as identity`), not UUIDs, unless asked: people read, quote and join on them.
- **Name every constraint** (`dpo_row_fk`, `dld_property_uk`) so error messages point at the problem.
- **Natural keys decide duplicates; write them down.** A composite unique key (several columns) beats a hash when people must understand why two rows are the same. Make nullable key parts safe with a virtual column (`nvl(col, 0)`), because NULLs do not collide in a unique key.
- **Keep raw and derived apart.** Store the original payload (JSON column plus hash), then derived columns beside it. Re-deriving later is free; recovering a lost raw record is not.
- **Never silently drop.** Rows that do not become a main record (duplicates, conflicts, no key) go to a side table with a reason, and the load log reconciles: received = stored + side-table copies.
- **Audit columns** on anything editable: `created_by`, `created_at`, `updated_by`, `updated_at`.
- **Soft state, not deletes**: an `is_active` flag and statuses beat deleting; allow real deletion only for rows people created themselves.
- **Rules as data.** Status lists, thresholds, matching limits and similar rules live in small settings tables with a note column, editable from a screen.
- **Matching suggestions are never applied automatically.** Store candidates with a score and a status (suggested, confirmed, rejected); a person confirms.
- **Index for the way you filter and join** (foreign keys, status, area), not everything.
- **Comment tables and columns** so the next person finds what a field means and where it came from.
- **Secrets stay out of tables you export**; keep them in a separate table or environment.

## 3. Hand-offs and checks

PL/SQL: `oracle-plsql`. Screens: `apex-dev` and `apex-ux`. Before release: `apex-audit` (it includes SQL checks for missing keys, audit columns and UUID use, in `skills/apex-audit/scripts/schema_checks.sql`).

## 4. Write the decision down

Keep a short "data model" document next to the code: tables, keys, matching rules, what is editable. When the key or a rule changes, say so there and list what existing data it affects.
