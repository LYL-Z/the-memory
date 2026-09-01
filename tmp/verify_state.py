import os, re
ROOT = r"D:/The Memory/The Memory"
students_dir = os.path.join(ROOT, "高中", "2025届", "人物", "学生")
city_by_name = {"卞俊豪":"南京","尹晶馨":"苏州","张睿":"湘潭","彭栩怡":"昆明",
"曾畅":"大连","李嘉乐":"重庆","李茹冰":"北京","潘敏行":"石家庄","胡筱乐":"太原",
"苏渝斐":"大连","董佳好":"南京","蔡云霓":"长沙","邓紫昂":"长沙","邹雨恬":"南京",
"郑森":"徐州","陈亭妤":"杭州","鞠子洲":"威海","马沿楚":"广州","黄杰林":"威海"}

print("=== 19 person pages: frontmatter (between --- and ---) ===")
for name, city in city_by_name.items():
    path = os.path.join(students_dir, f"{name}.md")
    if not os.path.exists(path):
        print(f"\n##### [MISSING FILE] {name}\n")
        continue
    text = open(path, encoding="utf-8").read()
    # extract frontmatter
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    fm = m.group(1) if m else "(no frontmatter)"
    has_field = "大学城市" in text
    mc = re.search(r"^大学城市:\s*(.*)$", text, re.M)
    cur = mc.group(1) if mc else "(none)"
    # find 大学: line
    mu = re.search(r"^大学:.*$", text, re.M)
    univ_line = mu.group(0) if mu else "(NO 大学: LINE)"
    print(f"\n##### {name} (应为城市={city}, 现有大学城市={cur})")
    print(fm)
    print(f"--- 大学: line -> {univ_line}")
