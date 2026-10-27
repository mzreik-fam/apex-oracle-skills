# Versions these notes were written for

- Oracle APEX 26.1 (APEXlang compiler from SQLcl 26.3)
- Oracle Database 26ai (23.26), Autonomous Database
- SQLcl 26.3

APEXlang is new and its syntax changes between releases. Treat everything in `apexlang-quickref.md` and `gotchas.md` as verified for the versions above and re-verify on others (validate a small page before building a large one).

## How to check what you have

```sql
select banner_full from v$version;
select version_no from apex_release;
```

In SQLcl: `show version` (client) and `apex version` if available.

## If the versions differ

1. Read the official documentation for your version (see `docs-links.md`).
2. Regenerate the property reference from your own SQLcl install: `python3 ../scripts/build_apexlang_reference.py`.
3. Validate a small test page for every pattern you rely on.
4. Update the "written for" lines above and note what changed in `gotchas.md`.
