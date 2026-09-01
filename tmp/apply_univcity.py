import os, re
ROOT = r"D:/The Memory/The Memory"
students_dir = os.path.join(ROOT, "高中", "2025届", "人物", "学生")
city_by_name = {"卞俊豪":"南京","尹晶馨":"苏州","张睿":"湘潭","彭栩怡":"昆明",
"曾畅":"大连","李嘉乐":"重庆","李茹冰":"北京","潘敏行":"石家庄","胡筱乐":"太原",
"苏渝斐":"大连","董佳好":"南京","蔡云霓":"长沙","邓紫昂":"长沙","邹雨恬":"南京",
"郑森":"徐州","陈亭妤":"杭州","鞠子洲":"威海","马沿楚":"广州","黄杰林":"威海"}

print("=== Insert 大学城市 for the 18 pages missing it ===")
for name, city in city_by_name.items():
    if name == "董佳好":
        continue
    path = os.path.join(students_dir, f"{name}.md")
    if not os.path.exists(path):
        print(f"[MISSING] {name}")
        continue
    text = open(path, encoding="utf-8").read()
    if "大学城市" in text:
        print(f"[SKIP already has] {name}")
        continue
    def repl(m, city=city):
        return m.group(1) + "\n大学城市: " + city
    new_text, n = re.subn(r"^(大学: .*)$", repl, text, count=1, flags=re.M)
    if n != 1:
        print(f"[WARN no 大学: line] {name}")
        continue
    open(path, "w", encoding="utf-8").write(new_text)
    print(f"OK {name}: 大学城市 -> {city}")
