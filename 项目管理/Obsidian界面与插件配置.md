---
分类标签: 项目运维
类型: Obsidian配置说明
更新日期: 2026-08-21
公开等级: 内部
tags: [项目管理, Obsidian, 插件, 视觉规范]
cssclasses: [longform]
---

> [!meta] 元数据页眉
> **文件编号**：RZ-OM-0028
> **所属分类**：项目运维
> **核心主题**：Obsidian界面与插件配置
> **关联文件**：[[00-知识库首页]] · [[项目管理/备份与恢复运维]]
> **核心出场人物**：刘佑林（叙事者）
> **时间跨度**：项目运维（2026）
# Obsidian界面与插件配置

本页记录 The Memory 的界面层。插件只负责导航、阅读与视觉呈现，不改变人物事实、来源状态、隐私等级或文件路径。

## 已启用的视觉与导航插件

| 插件 | 当前版本 | 用途 | 边界 |
|---|---:|---|---|
| Minimal Theme Settings | 9.0.0 | 控制 Minimal 的配色、行宽、字号、媒体宽度与折叠行为 | 不改 Markdown 内容 |
| Style Settings | 1.0.9 | 在设置页中调整本库 CSS 片段暴露的颜色、圆角与字体选项 | 配置只保存在 `.obsidian` |
| Homepage | 4.4.4 | 启动时以阅读模式打开并固定 [[00-知识库首页]] | 不替代静态索引 |
| File Explorer Note Count | 1.2.4 | 在文件树中显示各目录的 Markdown 笔记数 | 只计 `.md`，不代表素材完整度 |

现有的 Dataview、Excalidraw、Templater、QuickAdd、Advanced Tables 等插件继续保留。它们与本次视觉层相互独立。

维护提示：Style Settings 1.0.9 的上游仓库已归档，但它仍是 Obsidian 官方社区注册表中的稳定插件，本次在 Obsidian 1.13.7 中可加载。自定义 CSS 已写入默认值；即使未来停用 Style Settings，当前视觉方案仍会生效，只会失去图形化调节面板。

`Obsidian Git` 已启用。Vault 根目录是 Git 仓库，`.gitignore` 排除整个 `私人资料/`。插件配置禁止自动推送。没有远端之前，它只提供本机版本记录，不能代替 Sync 或含私密层的 ZIP。详见 [[项目管理/备份与恢复运维|备份与恢复运维]]。

## 视觉方案

- 主题：Minimal 9.0.2。
- 明暗配色：Flexoki Light / Flexoki Dark。
- 正文字体：Source Han Serif SC VF；用于长文阅读。
- 界面字体：Microsoft YaHei UI；用于文件树与设置页。
- 等宽字体：SF Mono；用于代码、路径与字段值。
- 主色：暖棕橙。它只承担链接、选中态和标题标记，不承担证据等级。

## 证据型 Callout

视觉颜色不能替代来源字段。下列 Callout 只帮助阅读，使用时仍须写明来源与核验状态。

```markdown
> [!fact] 已确认事实
> 只放入已有材料直接支持的内容。

> [!source] 来源说明
> 写明原始文件、页码、说话人与记录时间。

> [!analysis] 回望解释
> 明确这是事后分析，不是当时已知事实。

> [!fiction] 文学化重构
> 不得伪装成真实记忆、逐字原话或第三人内心。

> [!pending] 待核信息
> 保留冲突、缺字与尚未确认的字段。

> [!privacy] 私密材料
> 默认不进入公开导出或普通人物页。
```

## 页面样式类

在 YAML 中使用：

```yaml
cssclasses: [longform]
```

- `the-memory-dashboard`：仅用于首页。隐藏首页自身的属性面板，强化入口、表格与 Dataview 的层级；属性仍保存在 YAML 中。
- `longform`：用于章节、人物专题或长篇分析。正文更适合连续阅读。
- `source-ledger`：用于来源清单、审计和逐条转录。表格更紧凑。

## 调整入口

1. `设置 → Minimal Theme Settings`：切换明暗方案、正文宽度和字号。
2. `设置 → Style Settings → The Memory · 档案视觉系统`：调整本库主色、纸张色、圆角和标题线宽。
3. `设置 → Homepage`：更换启动页或取消固定。
4. `设置 → 外观 → CSS代码片段`：启停 `the-memory-archive`。

## 恢复方式

本次修改前的 Obsidian 配置快照位于工作区外层：

`D:\The Memory\.codex-tmp\obsidian-ui-backup-2026-08-13`

该目录不是知识库内容。恢复前应先退出 Obsidian，再按需复制对应 JSON 文件，避免覆盖正在写入的工作区状态。
