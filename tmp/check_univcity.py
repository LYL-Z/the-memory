import os, re
ROOT = r"D:/The Memory/The Memory"
students_dir = os.path.join(ROOT, "高中", "2025届", "人物", "学生")
city_by_name = {"卞俊豪":"南京","尹晶馨":"苏州","张睿":"湘潭","彭栩怡":"昆明",
"曾畅":"大连","李嘉乐":"重庆","李茹冰":"北京","潘敏行":"石家庄","胡筱乐":"太原",
"苏渝斐":"大连","董佳好":"南京","蔡云霓":"长沙","邓紫昂":"长沙","邹雨恬":"南京",
"郑森":"徐州","陈亭妤":"杭州","鞠子洲":"威海","马沿楚":"广州","黄杰林":"威海"}

all_ok = True
for name, city in city_by_name.items():
    path = os.path.join(students_dir, f"{name}.md")
    text = open(path, encoding="utf-8").read()
    mc = re.search(r"^大学城市:\s*(.*)$", text, re.M)
    cur = mc.group(1).strip() if mc else "(MISSING)"
    # extract city from 地域范围: ...（city）
    mr = re.search(r"^地域范围:.*?（([^）]+)）", text, re.M)
    region_city = mr.group(1) if mr else "(no region city)"
    ok = (cur == city) and (region_city == city)
    if not ok:
        all_ok = False
    print(f"{name:<6} | 大学城市={cur:<6} | 应为={city:<4} | 地域范围城市={region_city:<6} | {'OK' if ok else 'MISMATCH'}")
print("\nALL CONSISTENT:" , all_ok)
