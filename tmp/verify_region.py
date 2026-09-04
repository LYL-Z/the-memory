import os, re

VAULT = r"D:/The Memory/The Memory"
BACKUP = r"D:/The Memory/The Memory/.workbuddy/.tools/backup_before_region_20260902"

def get_region(path):
    if not os.path.exists(path):
        return "(缺失)"
    with open(path, encoding="utf-8") as f:
        text = f.read()
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not m: return "(无fm)"
    for ln in m.group(1).splitlines():
        if ln.startswith("地域范围:"):
            return ln[len("地域范围:"):].strip()
    return "(空)"

has_infer = []
no_infer = []
for root, _, files in os.walk(BACKUP):
    for fn in files:
        if not fn.endswith(".md"): continue
        rel = os.path.relpath(os.path.join(root, fn), BACKUP).replace("\\","/")
        val = get_region(os.path.join(VAULT, rel))
        (no_infer if "【推断】" not in val else has_infer).append((rel, val))

print(f"带【推断】共 {len(has_infer)} 处：")
for r, v in has_infer: print("   ", v, "|", r)
print(f"\n无【推断】共 {len(no_infer)} 处：")
for r, v in no_infer: print("   ", v, "|", r)
