#!/usr/bin/env python3
"""Static checks on an APEXlang export folder (from `apex export -exptype APEXLANG`).
  python3 audit_apex_export.py <export folder>
Prints findings as: severity | page | region/component | message. Exit code 1 if any MUST finding.
It reads text only; it cannot judge whether a heading is understandable, so pair it with the UX checklist."""
import glob, os, re, sys, collections

root = sys.argv[1] if len(sys.argv) > 1 else "."
files = sorted(glob.glob(os.path.join(root, "**", "pages", "p*.apx"), recursive=True)) or sorted(glob.glob(os.path.join(root, "pages", "p*.apx")))
if not files: sys.exit(f"no page files under {root}")
findings = []
def add(sev, page, where, msg): findings.append((sev, page, where, msg))

def regions(text):
    parts = re.split(r"\n    region ([\w-]+) \(", text)
    return [(parts[i], parts[i + 1]) for i in range(1, len(parts), 2)]

for f in files:
    page = os.path.basename(f)[:-4]; s = open(f).read()
    # 1. item names in conditions written with @ (stored as literal text, so the condition never matches)
    for m in re.finditer(r"\n\s+item: @(\w+)", s):
        add("MUST", page, m.group(1), "condition/readOnly item is written with '@'; it is stored as the literal text, so it never matches. Write the item name without '@'.")
    if "pageAccessProtection: unrestricted" in s:
        add("INFO", page, "page", "page access protection is 'unrestricted'; fine for internal tools, check it for pages that take URL arguments.")
    procs = re.findall(r"editableRegion: @([\w-]+)", s)
    for rid, body in regions(s):
        where = f"region {rid}"
        # 2. grids with editing but nothing saves them
        if "type: interactiveGrid" in body:
            if re.search(r"\n        edit \{\s*\n\s*enabled: true", body) and rid not in procs:
                add("MUST", page, where, "editing is enabled but no process has this region as editableRegion, so Save does nothing.")
            if "searchField" not in body:
                add("SHOULD", page, where, "grid toolbar has no search field.")
        # 3. duplicate end-user aliases in a region
        aliases = re.findall(r"endUserAlias: (\w+)", body)
        for a, n in collections.Counter(aliases).items():
            if n > 1: add("MUST", page, where, f"end-user alias '{a}' is used {n} times; the import fails with DUPLICATED_COMPONENT.")
        # 4. headings
        for cm in re.finditer(r"\n        column (\w+) \((.*?)(?=\n        column |\n        savedReport|\Z)", body, re.S):
            col, cb = cm.group(1), cm.group(2)
            h = re.search(r"heading:\s*(.*)", cb)
            if not h: continue
            head = h.group(1).strip()
            if re.fullmatch(r"[A-Z0-9_]+", head) and ("_" in head or head == col):
                add("SHOULD", page, f"{rid}.{col}", f"heading '{head}' looks like a database name; use plain words.")
            elif head.lower() in ("id", "name") and col not in ("ID", "NAME"):
                add("NICE", page, f"{rid}.{col}", f"heading '{head}' is very short; is it clear what it is the id or name of?")
        # 5. select *
        for q in re.findall(r"sqlQuery:\s*(?:```sql)?\s*(select\s+\*[^`\n]*)", body, re.I):
            add("INFO", page, where, "source is 'select *'; new columns of the table or view are not shown until added to the region.")
        # 6. LOV-style heading shows id
        for cm in re.finditer(r"\n        column (\w+_ID) \(", body):
            if "popupLov" not in body[cm.end():cm.end() + 200] and "selectList" not in body[cm.end():cm.end() + 200]:
                pass

order = {"MUST": 0, "SHOULD": 1, "NICE": 2, "INFO": 3}
for sev, page, where, msg in sorted(findings, key=lambda x: (order[x[0]], x[1], x[2])):
    print(f"{sev:6} | {page} | {where} | {msg}")
c = collections.Counter(x[0] for x in findings)
print(f"\n{len(files)} pages checked. MUST {c['MUST']}, SHOULD {c['SHOULD']}, NICE {c['NICE']}, INFO {c['INFO']}")
sys.exit(1 if c["MUST"] else 0)
