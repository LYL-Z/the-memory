import os, re

VAULT = r"D:/The Memory/The Memory"

# 用户确认项：绝对路径 -> 确认后的地域范围（无【推断】）
targets = {
    "小学/人物/同学/向睿馨.md": "湖南益阳",
    "小学/人物/同学/夏恺宪.md": "湖南益阳",
    "小学/人物/教师/李霞.md": "湖南益阳",
    "小学/人物/教师/李顺贤.md": "湖南益阳",
    "家庭/人物/杨铨.md": "湖南益阳",
    "家庭/人物/莫莫阿姨（杨铨之母）.md": "湖南益阳",
    "高中/2025届/人物/学生/颜子杰.md": "湖南长沙",
    "高中/2025届/人物/学生/上官青雨.md": "湖南长沙",
    "家庭/人物/洋洋（杨朝辉之女）.md": "湖南长沙",
    "家庭/人物/杨朝辉.md": "湖南长沙",
}

for rel, newval in targets.items():
    p = os.path.join(VAULT, rel)
    if not os.path.exists(p):
        print(f"MISS {rel} 文件不存在")
        continue
    with open(p, encoding="utf-8") as f:
        lines = f.readlines()
    done = False
    for i, ln in enumerate(lines):
        m = re.match(r"^(地域范围:\s*)(.*?)(\r?\n)$", ln)
        if m:
            oldval = m.group(2).strip()
            lines[i] = f"{m.group(1)}{newval}{m.group(3)}"
            print(f"OK  {rel}\n     {oldval!r} -> {newval!r}")
            done = True
            break
    if not done:
        print(f"WARN {rel} 未找到 地域范围 行")
        continue
    with open(p, "w", encoding="utf-8") as f:
        f.writelines(lines)
print("DONE")
