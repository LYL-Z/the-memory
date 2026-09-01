import os, re, glob

ROOT = r"D:/The Memory/The Memory"
# 6 canonical person directories (recursively scanned)
PERSON_DIRS = [
    os.path.join(ROOT, "高中", "G2204", "人物"),
    os.path.join(ROOT, "高中", "2025届", "人物"),
    os.path.join(ROOT, "初中", "2022届", "人物"),
    os.path.join(ROOT, "小学", "人物"),
    os.path.join(ROOT, "大学", "四川大学", "强基班", "人物"),
    os.path.join(ROOT, "家庭", "人物"),
]

ALLOWED_TIER = {"主人公","核心重点","核心","其他核心","普通"}

# Build set of all note paths (relative, no ext) for wikilink resolution
all_md = set()
for dp,_,fns in os.walk(ROOT):
    if any(x in dp for x in (".git",".obsidian",".workbuddy",".claudian","Excalidraw")):
        continue
    for fn in fns:
        if fn.lower().endswith(".md"):
            rel = os.path.relpath(os.path.join(dp,fn), ROOT).replace("\\","/")[:-3]
            all_md.add(rel)

def resolve_link(target):
    # target like "高中/G2204/人物/同学/刘佑林" possibly with |alias
    t = target.split("|")[0].strip()
    if t in all_md: return True
    if t + ".md" in all_md: return True
    # try exact file
    p = os.path.join(ROOT, t + ".md")
    if os.path.exists(p): return True
    # maybe target is a bare name; try searching
    return False

issues = {"missing_tier":[], "missing_age":[], "missing_region":[],
          "missing_idrange":[], "bad_tier":[], "wugang_pollution":[],
          "city_todo_leftover":[], "univcity_mismatch":[], "broken_links":[],
          "liu_school_wrong":[], "zeng_school_wrong":[]}

total = 0
for d in PERSON_DIRS:
    for dp,_,fns in os.walk(d):
        for fn in fns:
            if not fn.lower().endswith(".md"): continue
            total += 1
            path = os.path.join(dp, fn)
            rel = os.path.relpath(path, ROOT).replace("\\","/")
            text = open(path, encoding="utf-8").read()
            m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
            fm = m.group(1) if m else ""
            def g(field):
                mm = re.search(r"^"+re.escape(field)+r":\s*(.*)$", fm, re.M)
                return mm.group(1).strip() if mm else None
            tier = g("角色层级"); age = g("年龄范围"); region = g("地域范围"); idr = g("身份范围")
            if tier is None: issues["missing_tier"].append(rel)
            else:
                if tier not in ALLOWED_TIER: issues["bad_tier"].append((rel,tier))
            if age is None: issues["missing_age"].append(rel)
            if region is None: issues["missing_region"].append(rel)
            else:
                if "武冈" in region and ("G2204" in rel or "2025届" in rel):
                    issues["wugang_pollution"].append(rel)
                if "城市【待核】" in region or "【待核】" in region and "地域" in rel:
                    pass
                if "【待核】" in region:
                    issues["city_todo_leftover"].append((rel, region))
            if idr is None: issues["missing_idrange"].append(rel)
            # 大学城市 consistency
            uc = g("大学城市")
            if uc is not None:
                mr = re.search(r"求学地：[^（]*（([^）]+)）", region or "")
                rc = mr.group(1) if mr else None
                # normalize 大学城市 vs region (rc may have province/campus prefix)
                if rc and uc not in rc and rc not in uc:
                    issues["univcity_mismatch"].append((rel, uc, rc))
            # High-risk mappings
            if rel.endswith("高中/G2204/人物/同学/刘佑林.md"):
                if not (("麓山" in (g("学校") or "") or "麓山" in (region or "") or "长沙麓山" in text)):
                    issues["liu_school_wrong"].append(rel)
            if "曾子沣.md" in rel:
                if not ("武冈二中" in (g("高中毕业学校") or "") or "武冈" in (region or "")):
                    issues["zeng_school_wrong"].append(rel)
            # broken wikilinks (body only, skip frontmatter)
            body = text[m.end():] if m else text
            for lt in re.findall(r"\[\[([^\]]+)\]\]", body):
                tgt = lt.split("|")[0].strip()
                # skip non-path links (e.g., headings #, or pure aliases)
                if tgt.startswith("#"): continue
                if not resolve_link(tgt):
                    issues["broken_links"].append((rel, lt))

print("TOTAL person pages scanned:", total)
print("\n=== A. 结构完整性 ===")
print("缺角色层级:", len(issues["missing_tier"]), issues["missing_tier"][:10])
print("角色层级非法值:", issues["bad_tier"])
print("缺年龄范围:", len(issues["missing_age"]), issues["missing_age"][:10])
print("缺地域范围:", len(issues["missing_region"]), issues["missing_region"][:10])
print("缺身份范围:", len(issues["missing_idrange"]), issues["missing_idrange"][:10])
print("\n=== B. 污染/残留 ===")
print("武冈污染(G2204/2025届):", issues["wugang_pollution"])
print("地域范围含【待核】:", len(issues["city_todo_leftover"]))
for x in issues["city_todo_leftover"][:20]:
    print("   ", x[0], "->", x[1][:40])
print("\n=== C. 大学城市一致性 ===")
print("大学城市与地域范围求学城市不一致:", issues["univcity_mismatch"])
print("\n=== D. 高风险映射 ===")
print("刘佑林高中非麓山:", issues["liu_school_wrong"])
print("曾子沣高中非武冈:", issues["zeng_school_wrong"])
print("\n=== E. 断链(部分) ===")
print("断链总数:", len(issues["broken_links"]))
# dedupe broken link targets
from collections import Counter
c = Counter(lt for _,lt in issues["broken_links"])
print("断链目标 Top:", c.most_common(30))
