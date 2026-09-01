import os, re
from collections import Counter, defaultdict
ROOT = r"D:/The Memory/The Memory"
EXCLUDE = (".git",".obsidian",".workbuddy",".claudian","Excalidraw")
PERSON_DIRS = ("高中/G2204/人物","高中/2025届/人物","初中/2022届/人物",
               "小学/人物","大学/四川大学/强基班/人物","家庭/人物")

cnt = Counter()
geo_names, age_names = [], []
for dp, dirs, fns in os.walk(ROOT):
    dirs[:] = [d for d in dirs if d not in EXCLUDE]
    for fn in fns:
        if not fn.lower().endswith(".md"): continue
        rel = os.path.relpath(os.path.join(dp,fn), ROOT).replace("\\","/")
        if not any(rel.startswith(p) for p in PERSON_DIRS): continue
        text = open(os.path.join(dp,fn), encoding="utf-8").read()
        for line in text.split("\n"):
            m = re.match(r"^(年龄范围|地域范围|身份范围|籍贯|大学|学校|高中毕业学校|birth_date):\s*(.*)$", line)
            if m and "【待核】" in m.group(2):
                fld = m.group(1); cnt[fld]+=1
                name = os.path.basename(rel)[:-3]
                if fld=="地域范围": geo_names.append(name)
                if fld=="年龄范围": age_names.append(name)

print("=== 规范人物页 frontmatter 字段级【待核】构成 ===")
tot=0
for k,v in cnt.most_common():
    print(f"  {k:<12} {v}")
    tot+=v
print("  合计:", tot)
print("\n=== 地域范围【待核】明细（共 %d）===" % len(geo_names))
print("  " + "、".join(sorted(set(geo_names))))
print("\n=== 年龄范围【待核】人数（唯一）===", len(set(age_names)))
