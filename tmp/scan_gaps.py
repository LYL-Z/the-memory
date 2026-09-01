import os, re
ROOT = r"D:/The Memory/The Memory"
EXCLUDE = (".git", ".obsidian", ".workbuddy", ".claudian", "Excalidraw")
PAT = re.compile(r"【待核】|【待采】|【待确认】|待核字段|缺口|待采|待确认|待补|待核")

rows = []
for dp, dirs, fns in os.walk(ROOT):
    dirs[:] = [d for d in dirs if d not in EXCLUDE]
    for fn in fns:
        if not fn.lower().endswith(".md"): continue
        path = os.path.join(dp, fn)
        rel = os.path.relpath(path, ROOT).replace("\\", "/")
        try:
            lines = open(path, encoding="utf-8").read().split("\n")
        except Exception:
            continue
        for i, ln in enumerate(lines, 1):
            if PAT.search(ln):
                rows.append((rel, i, ln.strip()))

out = os.path.join(ROOT, "tmp", "gap_raw_inventory.txt")
with open(out, "w", encoding="utf-8") as f:
    f.write(f"TOTAL gap-flagged lines: {len(rows)}\n")
    f.write(f"Files with >=1 flag: {len(set(r[0] for r in rows))}\n\n")
    cur = None
    for rel, i, ln in rows:
        if rel != cur:
            cur = rel
            f.write("\n" + "="*100 + f"\n## {rel}\n" + "="*100 + "\n")
        f.write(f"L{i:>4}: {ln[:400]}\n")

print("TOTAL gap-flagged lines:", len(rows))
print("Files with >=1 flag:", len(set(r[0] for r in rows)))
print("Written to:", out)

# summary by top folder
from collections import Counter
c = Counter(r[0].split("/")[0] for r in rows)
print("\nBy top folder:")
for k,v in c.most_common():
    print(f"  {k:<20} {v}")
