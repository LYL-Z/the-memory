import re, pathlib

src = pathlib.Path(r"D:/The Memory/The Memory/tmp/jingtian_pdf_extract.txt").read_text(encoding="utf-8")
src = src.replace("\f", "")
lines = [ln for ln in src.split("\n") if not re.match(r"^\s*\S*码：\s*/\d+\s*15\s*$", ln)]
text = "\n".join(lines)
text = re.sub(r"\n{3,}", "\n\n", text).strip()

header = '''---
分类标签: 审美参考·叙事技法
类型: 第三方文本转录
来源: 孙宇晨 X 账号（https://x.com/justinsuntron/status/2092932777612390850，2026-08-27）；PDF 录入
性质: 第三方第一人称虚构叙事（文末自标"纯属虚构"）
边界: 非景甜本人自述；含代孕/财务/性描写等敏感内容，仅作写作技法参考，不进入事实层
关联: "[[文化与审美/人物审美库/景甜/景甜]]"
tags: [景甜, 孙宇晨, 叙事技法, 第三方文本, 虚构]
---

# 景甜（孙宇晨原文转录·全本）

> 以下为 PDF《孙宇晨：我的女友景甜》全文忠实转录，仅去除 PDF 分页标记与换页符，正文一字未改。
> 原载孙宇晨 X 账号，2026-08-27；文末标注"本文纯属虚构，如果雷同实属巧合"。
> **边界声明**：本文本为第三方单方虚构叙事，不代表景甜本人事实；含代孕、财务往来、性描写等敏感内容，仅限写作技法研究使用，不得作为任何真实人物的事实依据。

'''

out = header + text + "\n"
dst = pathlib.Path(r"D:/The Memory/The Memory/文化与审美/人物审美库/景甜/景甜-孙宇晨原文转录.md")
dst.write_text(out, encoding="utf-8")
print("written:", len(out), "chars ->", dst)
