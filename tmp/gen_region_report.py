import os, re
from collections import OrderedDict

VAULT = r"D:/The Memory/The Memory"
BACKUP = r"D:/The Memory/The Memory/.workbuddy/.tools/backup_before_region_20260902"

def read_region(path):
    if not os.path.exists(path):
        return "(文件缺失)"
    try:
        with open(path, encoding="utf-8") as f:
            text = f.read()
    except Exception as e:
        return f"(读取错误:{e})"
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not m:
        return "(无 frontmatter)"
    fm = m.group(1)
    for ln in fm.splitlines():
        if ln.startswith("地域范围:"):
            return ln[len("地域范围:"):].strip() or "(空值)"
    return "(字段原为空/无)"

rows = []
for root, dirs, files in os.walk(BACKUP):
    for fn in files:
        if not fn.endswith(".md"):
            continue
        bpath = os.path.join(root, fn)
        rel = os.path.relpath(bpath, BACKUP).replace("\\", "/")
        vpath = os.path.join(VAULT, rel)
        before = read_region(bpath)
        after = read_region(vpath)
        rows.append((rel, before, after))

def cat(rel):
    if rel.startswith("家庭/"): return "家庭"
    if rel.startswith("小学/"): return "小学"
    if rel.startswith("初中/"): return "初中"
    if rel.startswith("高中/2025届/人物/学生"): return "高中-同学(2025届)"
    if rel.startswith("高中/2025届/人物/教师"): return "高中-教师(2025届)"
    return "其他"

groups = OrderedDict()
for r in rows:
    groups.setdefault(cat(r[0]), []).append(r)
for k in groups:
    groups[k].sort(key=lambda x: x[0])

out = []
out.append("# 43 处地域回填对照清单（2026-09-02）\n")
out.append("> 比对来源：`.workbuddy/.tools/backup_before_region_20260902/`（回填前备份） vs 当前工作树。\n")
out.append("> 说明：43 处 `地域范围` 为阶段七按【推断】回填；经 2026-09-02 22:57 用户复核，**10 处已确认为确切（无【推断】）**——向睿馨/夏恺宪/李霞/李顺贤（小学·益阳）、杨铨/莫莫阿姨（家庭·益阳）、颜子杰/上官青雨（高中同学·长沙）沿用回填城市仅去标记；洋洋（杨朝辉之女）/杨朝辉 更正为长沙。其余 33 处维持【推断】。\n")
out.append("")
out.append(f"**总计：{len(rows)} 处**（家庭 4 / 小学 4 / 初中 4 / 高中同学 5 / 高中教师 26）\n")

for g, items in groups.items():
    out.append(f"## {g}（{len(items)} 处）\n")
    out.append("| # | 文件（相对 vault 路径） | 回填前 | 回填后 |")
    out.append("|---|---|---|---|")
    for i, (rel, before, after) in enumerate(items, 1):
        out.append(f"| {i} | `{rel}` | {before} | {after} |")
    out.append("")

dest = os.path.join(VAULT, "tmp", "地域回填43处对照-2026-09-02.md")
with open(dest, "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("written", len(rows), "rows ->", dest)
