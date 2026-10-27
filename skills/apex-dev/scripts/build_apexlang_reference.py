#!/usr/bin/env python3
"""Builds a searchable APEXlang property reference from YOUR OWN SQLcl install.

SQLcl ships the APEXlang compiler (apexlang-compiler.jar), which contains the compiler's metadata: every component type, its
properties, groups and the valid values of list properties. This script reads that file and writes Markdown. Nothing from the
jar is copied into this repository; each developer generates the file for the SQLcl/APEX version they actually have.

  python3 build_apexlang_reference.py [--sqlcl <sqlcl dir or jar>] [--out ../references/apexlang-reference.md]
"""
import argparse, glob, json, os, sys, zipfile

ap = argparse.ArgumentParser()
ap.add_argument("--sqlcl", help="SQLcl install folder, or the apexlang-compiler.jar itself")
ap.add_argument("--out", default=os.path.join(os.path.dirname(__file__), "..", "references", "apexlang-reference.md"))
a = ap.parse_args()

def find_jar():
    if a.sqlcl and a.sqlcl.endswith(".jar"): return a.sqlcl
    roots = [a.sqlcl] if a.sqlcl else []
    roots += ["/opt/homebrew/Caskroom/sqlcl/*/sqlcl", "/usr/local/Caskroom/sqlcl/*/sqlcl", os.path.expanduser("~/sqlcl"),
              "/opt/oracle/sqlcl", "C:/sqlcl", os.environ.get("SQLCL_HOME", "")]
    for r in roots:
        for hit in glob.glob(os.path.join(r, "lib", "ext", "apexlang-compiler.jar")) if r else []:
            return hit
    sys.exit("apexlang-compiler.jar not found. Pass --sqlcl <your SQLcl folder> (it is in lib/ext).")

jar = find_jar()
d = json.loads(zipfile.ZipFile(jar).read("apexlang_meta_data.json"))
props, types = d["properties"], d["componentTypes"]
name = lambda t: t["name"]["singular"] if isinstance(t["name"], dict) else t["name"]
out = [f"# APEXlang property reference\n\nGenerated from `{os.path.basename(jar)}` (build id {d.get('buildID')}). Do not edit; regenerate after upgrading SQLcl.\n"]
out.append("Component types are listed with their parent, the file they live in, and each property as `group.property` with its type, whether it is required, and the valid values of list properties.\n")
out.append("## Index\n" + "\n".join(f"- {name(t)} (parent: {name(types[str(t['parent']['componentTypeId'])]) if t.get('parent') and str(t['parent'].get('componentTypeId')) in types else 'page/app'})" for _, t in sorted(types.items(), key=lambda kv: name(kv[1]))) + "\n")
for tid, t in sorted(types.items(), key=lambda kv: name(kv[1])):
    par = t.get("parent") or {}
    pname = name(types[str(par["componentTypeId"])]) if str(par.get("componentTypeId")) in types else "-"
    out.append(f"\n## {name(t)}\nParent: {pname}. File: `{t.get('filePath', '-')}`\n")
    rows = []
    for pid, pp in (t.get("properties") or {}).items():
        p = props.get(pid, {})
        lov = p.get("lov") or {}
        vals = ", ".join(v["name"] for v in lov.get("values", [])) if lov.get("type") == "STATIC" else (f"(list from {lov.get('type', '').lower()})" if lov else "")
        req = "required" if pp.get("isRequired") is True else ""
        rows.append((pp.get("groupName", ""), p.get("name", pid), p.get("type", ""), req, vals))
    for g, n, ty, req, vals in sorted(rows):
        out.append(f"- `{g}.{n}` {ty} {req} {('values: ' + vals) if vals else ''}".rstrip())
os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
open(a.out, "w").write("\n".join(out) + "\n")
print(f"wrote {a.out} ({len(types)} component types)")
