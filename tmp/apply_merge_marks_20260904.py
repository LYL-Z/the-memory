import os, io
VAULT = r"D:/The Memory/The Memory"
NEW = "项目管理/全库缺口与审计总台账-2026-09-04"
LINK = f"[[{NEW}|全库缺口与审计总台账（2026-09-04 · 全库唯一现行）]]"

WARN = f"""> [!warning] 已取代 · 并入唯一台账（2026-09-04 全库审计合并）
> 本文件的全部开放项已并入并重定向至 {LINK}。本文件仅作历史档案留存，**不再作为采集依据**；"还缺什么"以唯一台账为唯一来源。
"""

INFO = f"""> [!info] 已并入唯一台账（2026-09-04）
> 本页保留作档案/底册；其全部待核、待办类开放项已并入 {LINK}，后续状态以该唯一台账为准，本页不再单独维护。
"""

def insert_after_fm(rel, block):
    p = os.path.join(VAULT, rel)
    t = io.open(p, encoding="utf-8").read()
    if "全库缺口与审计总台账-2026-09-04" in t:
        print("SKIP(已有指向)", rel); return
    lines = t.split("\n")
    if lines[0].strip() != "---":
        out = block + "\n" + t
    else:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
        lines.insert(end + 1, "\n" + block.rstrip("\n"))
        out = "\n".join(lines)
    io.open(p, "w", encoding="utf-8").write(out)
    print("OK 插入", rel)

def rep(rel, old, new, expect=1):
    p = os.path.join(VAULT, rel)
    t = io.open(p, encoding="utf-8").read()
    n = t.count(old)
    if n != expect:
        print(f"FAIL {rel} | {old[:30]} | count={n}"); return
    io.open(p, "w", encoding="utf-8").write(t.replace(old, new))
    print("OK 替换", rel, "|", old[:24])

# A. 插入标注
insert_after_fm("项目管理/全库缺口与审计总台账-2026-09-02.md", WARN)
insert_after_fm("项目管理/全库整理记录-2026-08-31.md", INFO)
insert_after_fm("项目管理/内容问题检测清单-2026-08-31.md", WARN)
insert_after_fm("项目管理/用户订正-2026-08-28-证据口径与姓名校勘.md", INFO)
insert_after_fm("知识库总收录审计-2026-08-09.md", INFO)
insert_after_fm("长篇创作/第一卷素材缺口台账.md", WARN)
insert_after_fm("项目管理/收录审计/收录审计总索引.md", INFO)
insert_after_fm("项目管理/待核事项/待核事项索引.md", INFO)
insert_after_fm("项目管理/待核事项/母亲QQ相册待核事项-2026-08-29.md", INFO)

# B. 指向更新
rep("项目管理/全库缺口总清单.md",
    "[[项目管理/全库缺口与审计总台账-2026-09-02|全库缺口与审计总台账（2026-09-02 · 现行）]]",
    LINK)
p = os.path.join(VAULT, "长篇创作/素材缺口与待采清单-2026-08-28.md")
t = io.open(p, encoding="utf-8").read()
n = t.count("全库缺口总清单")
t = t.replace("全库缺口总清单", LINK)
io.open(p, "w", encoding="utf-8").write(t)
print("OK 素材清单指向", n, "处")

rep("项目管理/项目管理索引.md",
    "- [[项目管理/全库缺口与审计总台账-2026-09-02|★ 全库缺口与审计总台账（2026-09-02 · 唯一现行）]] — 已取代《全库缺口总清单》及全部历史审计快照",
    f"- [[{NEW}|★ 全库缺口与审计总台账（2026-09-04 · 全库唯一现行）]] — 已合并取代《全库缺口总清单》《总台账-09-02》及**全部**历史审计/审查/缺口/整理文件（2026-09-04 全库审计合并）")

rep("知识库总索引.md",
    "| 两处「吴筱丹待确认」表述滞后 | 待更新 | 用户已于 2026-08-28 确认规范名为伍筱丹，但两处旧文仍写「待确认」 |",
    "| ~~两处「吴筱丹待确认」表述滞后~~ | **已闭合（2026-08-31 审查已按订正更新）** | 规范名＝伍筱丹（「吴筱丹」系刘佑林误记）；2026-09-04 复核销账 |")
