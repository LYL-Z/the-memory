import os, re, json
from collections import defaultdict

VAULT = r"D:/The Memory/The Memory"
EXCLUDE_DIRS = {".git", ".workbuddy", ".obsidian", ".claudian", ".trash", "tmp", "_归档", "scripts", "Excalidraw", "attachments"}
MARKS = ["待核", "待补", "待采", "未确认", "存疑", "未核", "待确认", "待定", "待办", "待验证", "待回滚", "待裁决", "待用户"]

results = []  # (file, lineno, mark, line_text)
file_stats = defaultdict(lambda: defaultdict(int))

for root, dirs, files in os.walk(VAULT):
    dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
    for fn in files:
        if not fn.endswith(".md"):
            continue
        path = os.path.join(root, fn)
        rel = os.path.relpath(path, VAULT).replace("\\", "/")
        try:
            with open(path, encoding="utf-8") as f:
                lines = f.readlines()
        except Exception:
            continue
        in_callout_replaced = False
        for i, ln in enumerate(lines, 1):
            if i <= 12 and ("已取代" in ln or "已归档" in ln):
                in_callout_replaced = True
            for m in MARKS:
                if m in ln:
                    # 跳过"已取代"文件正文中的标记（仍记录但标旗）
                    results.append((rel, i, m, ln.strip()[:220], in_callout_replaced))
                    file_stats[rel][m] += 1
                    break  # 每行只记最先命中的一个标记

# 输出行级明细
with open(os.path.join(VAULT, "tmp", "marks_linelevel_20260904.txt"), "w", encoding="utf-8") as f:
    cur = None
    for rel, i, m, txt, sup in results:
        if rel != cur:
            f.write(f"\n===== {rel} {'[已取代文件]' if sup else ''} =====\n")
            cur = rel
        f.write(f"L{i} [{m}] {txt}\n")

# 输出统计
total = sum(sum(v.values()) for v in file_stats.values())
out = [f"总标记行数: {total}", f"涉及文件数: {len(file_stats)}", ""]
for rel, st in sorted(file_stats.items(), key=lambda x: -sum(x[1].values())):
    out.append(f"{rel} :: " + " ".join(f"{k}={v}" for k, v in sorted(st.items(), key=lambda x: -x[1])))
with open(os.path.join(VAULT, "tmp", "marks_stats_20260904.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print(f"total_marks={total}, files={len(file_stats)}")
print("written: tmp/marks_linelevel_20260904.txt, tmp/marks_stats_20260904.txt")
