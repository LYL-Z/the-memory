import pathlib

BASE = pathlib.Path(r"D:/The Memory/The Memory/项目管理")

callout_B = (
    "> [!warning] 本文件已取代（历史审计快照）\n"
    "> 本审计快照已被 [[项目管理/全库缺口与审计总台账-2026-09-02|全库缺口与审计总台账（2026-09-02 · 现行）]] 取代，"
    "仅保留作历史溯源。现行缺口与审计信息以该总台账为唯一权威。\n\n"
)
callout_C_stay = (
    "> [!info] 本文件已归档（一次性收录/核对记录）\n"
    "> 本文件为一次性收录/核对记录，已于 2026-09-02 逻辑归档。因仍被多处索引/正文引用（维持图谱完整），"
    "**物理留存原处**；现行权威信息见 [[项目管理/全库缺口与审计总台账-2026-09-02|全库缺口与审计总台账（2026-09-02）]]。\n\n"
)
callout_C_moved = (
    "> [!info] 本文件已归档（2026-09-02 物理归档至 `_归档/`）\n"
    "> 本一次性收录/核对记录已归档至 `项目管理/收录审计/_归档/`。"
    "现行权威信息见 [[项目管理/全库缺口与审计总台账-2026-09-02|全库缺口与审计总台账（2026-09-02）]]。\n\n"
)

tier_b = [
    "全库缺口总清单.md",
    "收录审计/全库结构与完整性审计-2026-08-13.md",
    "收录审计/全库结构与完整性审计-2026-08-21.md",
    "收录审计/全库链接与数据卫生检测-2026-08-31.md",
    "收录审计/全库审计与运维风险报告-2026-08-29.md",
    "收录审计/写作技法库建设与全库复核-2026-08-21.md",
    "内容问题检测清单-2026-08-31.md",
    "全库整理记录-2026-08-31.md",
]
tier_c_stay = [
    "收录审计/知识库收录审计补充-2026-08-12-中考与赵问竹高中回忆.md",
    "收录审计/知识库收录审计补充-2026-08-12-高二上第一次家长大会.md",
    "收录审计/知识库收录审计补充-2026-08-13-G2205毕业去向.md",
    "收录审计/2026-08-28-创作规格与颜子杰材料系统性核对.md",
    "收录审计/2026-08-28-曾子沣QQ动态系统性核对.md",
]
tier_c_moved = [
    "收录审计/_归档/知识库收录审计补充-2026-08-11-赵问竹18份影像.md",
    "收录审计/_归档/知识库收录审计补充-2026-08-11-赵问竹成长资料.md",
    "收录审计/_归档/知识库收录清单-2026-08-11-赵问竹18份资料.md",
    "收录审计/_归档/知识库收录验收-2026-08-11-赵问竹18份影像.md",
]

def insert(path: pathlib.Path, callout: str):
    text = path.read_text(encoding="utf-8")
    if text.startswith("---"):
        idx = text.find("\n---", 3)
        if idx != -1:
            end = text.find("\n", idx + 1)
            # insert after the closing --- line
            new = text[: end + 1] + "\n" + callout + text[end + 1:]
            path.write_text(new, encoding="utf-8")
            return "B-frontmatter"
    # fallback: prepend
    path.write_text(callout + text, encoding="utf-8")
    return "prepended"

results = []
for f in tier_b:
    p = BASE / f
    results.append((f, insert(p, callout_B)))
for f in tier_c_stay:
    p = BASE / f
    results.append((f, insert(p, callout_C_stay)))
for f in tier_c_moved:
    p = BASE / f
    results.append((f, insert(p, callout_C_moved)))

for f, how in results:
    print(f"{how:14} {f}")
print("TOTAL:", len(results))
