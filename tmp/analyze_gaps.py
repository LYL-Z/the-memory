import os, re
from collections import Counter, defaultdict
ROOT = r"D:/The Memory/The Memory"
EXCLUDE = (".git",".obsidian",".workbuddy",".claudian","Excalidraw")

rows = []
for dp, dirs, fns in os.walk(ROOT):
    dirs[:] = [d for d in dirs if d not in EXCLUDE]
    for fn in fns:
        if not fn.lower().endswith(".md"): continue
        rel = os.path.relpath(os.path.join(dp,fn), ROOT).replace("\\","/")
        try: lines = open(os.path.join(dp,fn), encoding="utf-8").read().split("\n")
        except Exception: continue
        for i, ln in enumerate(lines,1):
            s = ln.strip()
            if not s: continue
            for m in re.finditer(r"【待核】|【待采】|【待确认】|待核字段|缺口|待采|待确认|待补|待核", s):
                rows.append((rel, i, s, m.group(0)))

print("=== 1. 标记类型计数 ===")
for k,v in Counter(r[3] for r in rows).most_common():
    print(f"  {k:<10} {v}")

print("\n=== 2. 缺口最集中的文件 Top 25 ===")
for rel,c in Counter(r[0] for r in rows).most_common(25):
    print(f"  {c:>4}  {rel}")

print("\n=== 3. 地域范围/字段级【待核】统计 ===")
field_gaps = defaultdict(list)
for rel,i,s,mk in rows:
    if mk == "【待核】":
        # classify
        if s.startswith("-") and "地域范围" in s or "地域范围:" in s:
            field_gaps["frontmatter字段(地域范围等)"].append((rel,s))
print("  frontmatter字段级【待核】:",
      sum(1 for rel,i,s,mk in rows if mk=="【待核】" and re.match(r"^[-*]?\s*\w+范围[:：]", s)))

# Count 地域范围 specific
geo = [ (rel,s) for rel,i,s,mk in rows if mk=="【待核】" and "范围:" in s ]
print("  含'范围:'的【待核】行(多为三范围字段):", len(geo))
for rel,s in geo[:8]:
    print("     ", rel, "|", s[:90])

print("\n=== 4. 结构性'待采清单'段落定位 ===")
for name in ["章节设计-第一卷-童年与底色","章节设计-第二卷-青春与阵痛",
             "章节设计-第三卷-爱与迷失","章节设计-第四卷-困境与重建",
             "章节设计-第五卷-和解与当下"]:
    for dp,dirs,fns in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in EXCLUDE]
        for fn in fns:
            if fn==name+".md":
                p=os.path.join(dp,fn)
                lines=open(p,encoding="utf-8").read().split("\n")
                idx=[i for i,l in enumerate(lines) if "待采清单" in l or "缺口" in l]
                print(f"\n--- {fn}  命中行号: {idx}")
                for i in idx:
                    for j in range(i, min(i+16, len(lines))):
                        if lines[j].strip():
                            print(f"   L{j+1}: {lines[j].strip()[:160]}")
                        if j>i+14: break
