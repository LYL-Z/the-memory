import os, re
from collections import Counter
ROOT = r"D:/The Memory/The Memory"
PERSON_DIRS = [
    os.path.join(ROOT, "高中", "G2204", "人物"),
    os.path.join(ROOT, "高中", "2025届", "人物"),
    os.path.join(ROOT, "初中", "2022届", "人物"),
    os.path.join(ROOT, "小学", "人物"),
    os.path.join(ROOT, "大学", "四川大学", "强基班", "人物"),
    os.path.join(ROOT, "家庭", "人物"),
]
# index all notes: by full rel path (no ext) and by basename (no ext)
by_path = set(); by_base = {}
for dp,_,fns in os.walk(ROOT):
    if any(x in dp for x in (".git",".obsidian",".workbuddy",".claudian","Excalidraw")): continue
    for fn in fns:
        if not fn.lower().endswith(".md"): continue
        rel = os.path.relpath(os.path.join(dp,fn), ROOT).replace("\\","/")[:-3]
        by_path.add(rel)
        base = fn[:-3]
        by_base.setdefault(base, []).append(rel)

def resolve(target):
    # strip alias and #heading anchor to get the note path
    t = target.split("|")[0].strip()
    note = t.split("#")[0].strip()
    if note == "": return True  # same-note anchor
    if note in by_path: return True
    if note + ".md" in by_path: return True
    base = note.split("/")[-1]
    if base in by_base: return True
    return False

truly_missing = Counter()
files_with_missing = set()
for d in PERSON_DIRS:
    for dp,_,fns in os.walk(d):
        for fn in fns:
            if not fn.lower().endswith(".md"): continue
            path = os.path.join(dp, fn)
            rel = os.path.relpath(path, ROOT).replace("\\","/")
            text = open(path, encoding="utf-8").read()
            m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
            body = text[m.end():] if m else text
            for lt in re.findall(r"\[\[([^\]]+)\]\]", body):
                tgt = lt.split("|")[0].strip()
                if tgt.startswith("#"): continue
                if not resolve(tgt):
                    truly_missing[lt]+=1
                    files_with_missing.add(rel)

print("TRULY MISSING link targets (basename not found anywhere):", len(truly_missing))
for tgt,cnt in truly_missing.most_common(60):
    print(f"  {cnt:>3}  {tgt}")
print("\nFiles containing truly-missing links:", len(files_with_missing))
