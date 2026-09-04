import os, re

VAULT = r"D:/The Memory/The Memory"
EXCLUDE_DIRS = {".git", ".workbuddy", ".obsidian", ".claudian", ".trash", "tmp", "_归档", "scripts", "Excalidraw", "attachments"}
USER_PAT = re.compile(r"用户(确认|口述|确证|说明|裁定|裁决|提供|回答|指出|明确|订正|授权)|经用户|用户20[12][0-9]|用户口供")
MARK_PAT = re.compile(r"待核|待补|待采|未确认|存疑|未核|待确认|待定|待验证|待裁决")

hits = []
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
        for i, ln in enumerate(lines, 1):
            if USER_PAT.search(ln) and MARK_PAT.search(ln):
                hits.append((rel, i, ln.strip()[:260]))

with open(os.path.join(VAULT, "tmp", "user_answered_but_marked_20260904.txt"), "w", encoding="utf-8") as f:
    cur = None
    for rel, i, txt in hits:
        if rel != cur:
            f.write(f"\n===== {rel} =====\n")
            cur = rel
        f.write(f"L{i}: {txt}\n")
print(f"co-occurrence lines: {len(hits)}")
