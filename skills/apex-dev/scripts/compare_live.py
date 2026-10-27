#!/usr/bin/env python3
"""Shows what people changed in the LIVE app compared with your source, before you import.
  python3 compare_live.py <live export folder> <your source folder>
Both are APEXlang folders (the live one comes from `apex export -exptype APEXLANG`). Differences in formatting are ignored; it compares
what matters to users: regions, column headings and order, queries, inline CSS, conditions, toolbar and pagination settings, items.
Every line it prints is either someone's browser edit to keep, or something you are about to overwrite."""
import glob, os, re, sys

def pages(root):
    files = glob.glob(os.path.join(root, "**", "pages", "p*.apx"), recursive=True) or glob.glob(os.path.join(root, "pages", "p*.apx"))
    return {os.path.basename(f)[:-4]: open(f).read() for f in files}

def norm(t): return re.sub(r"\s+", " ", t or "").strip()

def model(text):
    m = {"css": norm(" ".join(re.findall(r"css \{\s*inline:\s*(?:```css)?(.*?)(?:```)?\s*\}", text, re.S))), "regions": {}, "items": sorted(re.findall(r"\n    pageItem (\w+) \(", text)),
         "processes": sorted(re.findall(r"\n    process ([\w-]+) \(", text))}
    parts = re.split(r"\n    region ([\w-]+) \(", text)
    for i in range(1, len(parts), 2):
        rid, body = parts[i], parts[i + 1]
        body = re.split(r"\n    (?:pageItem|process|button|region) ", body)[0]
        q = re.search(r"sqlQuery:\s*(?:```sql)?(.*?)(?:```|\n\s{8}\w+ \{|\n\s{8}\w+:|\Z)", body, re.S)
        cols = {}
        cparts = re.split(r"\n        column (\w+) \(", body)
        for j in range(1, len(cparts), 2):
            cb = cparts[j + 1]
            h = re.search(r"heading:\s*(.*)", cb); s = re.search(r"sequence:\s*(\d+)", cb); t = re.search(r"\n\s+type:\s*(\w+)", cb)
            cols[cparts[j]] = (h.group(1).strip() if h else None, s.group(1) if s else None, t.group(1) if t else None)
        name = re.search(r"name:\s*(.*)", body)
        cond = re.findall(r"serverSideCondition \{\s*type:\s*(\S+)\s*item:\s*(\S+)\s*value:\s*(\S+)", body)
        ctl = re.search(r"toolbar \{.*?controls: \[(.*?)\]", body, re.S)
        pag = re.search(r"pagination \{(.*?)\}", body, re.S)
        m["regions"][rid] = {"name": name.group(1).strip() if name else None, "sql": norm(q.group(1)) if q else None, "cols": cols, "cond": cond,
                             "toolbar": norm(ctl.group(1)) if ctl else None, "pagination": norm(pag.group(1)) if pag else None}
    return m

live, mine = pages(sys.argv[1]), pages(sys.argv[2])
n = 0
def say(page, msg):
    global n; n += 1; print(f"{page}: {msg}")
for p in sorted(set(live) | set(mine)):
    if p not in live: say(p, "only in your source (not in the live app yet)"); continue
    if p not in mine: say(p, "only in the LIVE app (somebody created it; your import would delete it)"); continue
    a, b = model(live[p]), model(mine[p])
    if a["css"] != b["css"]: say(p, f"inline CSS differs. Live: '{a['css'][:90]}' | yours: '{b['css'][:90]}'")
    if a["items"] != b["items"]: say(p, f"page items differ. live {a['items']} vs yours {b['items']}")
    if a["processes"] != b["processes"]: say(p, f"processes differ. live {a['processes']} vs yours {b['processes']}")
    for rid in sorted(set(a["regions"]) | set(b["regions"])):
        la, lb = a["regions"].get(rid), b["regions"].get(rid)
        if la is None or lb is None: say(p, f"region '{rid}' exists only in the {'live app' if lb is None else 'source'}"); continue
        for k in ("name", "sql", "toolbar", "pagination"):
            if la[k] != lb[k]: say(p, f"region {rid}: {k} differs. live: {str(la[k])[:80]} | yours: {str(lb[k])[:80]}")
        if la["cond"] != lb["cond"]: say(p, f"region {rid}: condition differs. live {la['cond']} vs yours {lb['cond']}")
        for c in sorted(set(la["cols"]) | set(lb["cols"])):
            x, y = la["cols"].get(c), lb["cols"].get(c)
            if x is None: say(p, f"region {rid}: column {c} is in your source but not live (someone removed it, or you added it)")
            elif y is None: say(p, f"region {rid}: column {c} is live but not in your source (someone added it)")
            elif x[0] != y[0]: say(p, f"region {rid}: column {c} heading live '{x[0]}' vs yours '{y[0]}'")
            elif x[1] != y[1]: say(p, f"region {rid}: column {c} position live {x[1]} vs yours {y[1]} (moved)")
print(f"\n{n} difference(s). Merge every one that is a person's edit into your source before importing.")
