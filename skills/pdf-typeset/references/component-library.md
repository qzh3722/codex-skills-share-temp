# PDF 排版组件库

> 从本库中选取组件拼装 HTML，不需要全部使用——按内容需要选取。

## 目录

1. [基础排版](#基础排版) — 字体、颜色变量、页面结构
2. [页眉区](#页眉区) — 标题、标签栏、副标题、作者
3. [正文组件](#正文组件) — 段落、标题、引用、列表
4. [表格](#表格) — 深色表头、斑马纹
5. [卡片系统](#卡片系统) — 概念框、警告框、编号漏洞卡、判决框
6. [可视化](#可视化) — 流程图行、时间线、对比图
7. [页脚区](#页脚区) — 来源链接、日期
8. [分页控制](#分页控制)
9. [配色方案参考](#配色方案参考)

---

## 基础排版

### 字体加载

```css
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700&family=Noto+Sans+SC:wght@300;400;500;700&display=swap');
```

用途：
- `Noto Serif SC` → 标题、概念名称（有文化感）
- `Noto Sans SC` → 正文、表格、标签（清晰易读）

### CSS 变量模板

```css
:root {
  /* 底色 */
  --bg: #fafaf8;
  --text: #1a1a1a;
  --text-secondary: #555;

  /* 强调色 —— 按主题替换这一组即可换肤 */
  --accent: #b44a3e;          /* 主强调 */
  --accent-light: #f3e8e6;    /* 标签/浅底 */

  /* 结构色 */
  --border: #d4d0c8;
  --table-header: #2c2c2c;
  --table-header-text: #fff;
  --table-stripe: #f5f3ef;
  --blockquote-bg: #f0eeea;
}
```

### 全局重置

```css
* { margin: 0; padding: 0; box-sizing: border-box; }
@page { size: A4; margin: 2.2cm 2cm 2cm 2cm; }
body {
  font-family: 'Noto Sans SC', 'Segoe UI', sans-serif;
  font-size: 10.5pt;
  line-height: 1.75;
  color: var(--text);
  background: var(--bg);
}
```

---

## 页眉区

### 居中标题头（适合论文、报告）

```css
.header {
  text-align: center;
  padding-bottom: 24px;
  margin-bottom: 24px;
  border-bottom: 2px solid var(--accent);
}
h1 {
  font-family: 'Noto Serif SC', serif;
  font-size: 20pt;
  font-weight: 700;
  line-height: 1.3;
  margin-bottom: 8px;
}
.subtitle {
  font-size: 10pt;
  color: var(--text-secondary);
  margin-bottom: 10px;
}
.authors {
  font-size: 8.5pt;
  color: #777;
  line-height: 1.6;
}
```

```html
<div class="header">
  <div class="tag-bar">
    <span class="tag">标签1</span>
    <span class="tag">标签2</span>
  </div>
  <h1>主标题<br>副标题</h1>
  <p class="subtitle">机构 · 来源 · 日期</p>
  <p class="authors">作者1 · 作者2 · 作者3</p>
</div>
```

### 标签栏

```css
.tag-bar {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-bottom: 14px;
}
.tag {
  font-size: 8pt;
  padding: 2px 10px;
  border-radius: 3px;
  background: var(--accent-light);
  color: var(--accent);
  font-weight: 500;
}
/* 警告标签变体 */
.tag.warn {
  background: #fdf6ed;
  color: #c9760c;
}
```

---

## 正文组件

### 二级标题

```css
h2 {
  font-family: 'Noto Serif SC', serif;
  font-size: 13pt;
  font-weight: 600;
  color: var(--accent);
  margin-top: 24px;
  margin-bottom: 10px;
  padding-bottom: 3px;
  border-bottom: 1px solid var(--border);
}
```

### 三级标题

```css
h3 {
  font-size: 11pt;
  font-weight: 700;
  color: var(--text);
  margin-top: 16px;
  margin-bottom: 6px;
}
```

### 段落和加粗

```css
p { margin-bottom: 8px; }
strong { font-weight: 700; }
```

### 引用块

```css
blockquote {
  background: var(--blockquote-bg);
  border-left: 3px solid var(--accent);
  padding: 10px 14px;
  margin: 12px 0;
  border-radius: 0 4px 4px 0;
  font-size: 10pt;
  color: var(--text-secondary);
}
```

### 列表

```css
ul, ol { margin: 8px 0 8px 18px; }
li { margin-bottom: 5px; line-height: 1.65; font-size: 10pt; }
```

---

## 表格

```css
table {
  width: 100%;
  border-collapse: collapse;
  margin: 12px 0;
  font-size: 9.5pt;
}
thead th {
  background: var(--table-header);
  color: var(--table-header-text);
  font-weight: 500;
  padding: 7px 10px;
  text-align: left;
}
thead th:first-child { border-radius: 4px 0 0 0; }
thead th:last-child { border-radius: 0 4px 0 0; }
tbody td {
  padding: 7px 10px;
  border-bottom: 1px solid #e5e2dc;
}
tbody tr:nth-child(even) { background: var(--table-stripe); }
```

**注意**：宽表格加 `table { table-layout: fixed; word-break: break-all; }` 防溢出。

---

## 卡片系统

### 概念框（强调核心概念）

```css
.concept-box {
  background: linear-gradient(135deg, #fdf6f4 0%, #f9f0ed 100%);
  border: 1px solid #e8cfc9;
  border-radius: 6px;
  padding: 14px 16px;
  margin: 14px 0;
}
.concept-box .label {
  font-family: 'Noto Serif SC', serif;
  font-size: 10.5pt;
  font-weight: 700;
  color: var(--accent);
  margin-bottom: 4px;
}
```

```html
<div class="concept-box">
  <div class="label">概念名称</div>
  <p>概念解释内容。</p>
</div>
```

### 警告框

```css
.warn-box {
  background: #fdf6ed;
  border: 1px solid #e8c88a;
  border-radius: 6px;
  padding: 14px 16px;
  margin: 14px 0;
}
.warn-box .label {
  font-weight: 700;
  color: #c9760c;
  font-size: 10pt;
  margin-bottom: 4px;
}
```

### 编号卡片（漏洞分析、步骤列表）

```css
.flaw-card {
  background: #fff;
  border: 1px solid #e0ddd6;
  border-radius: 6px;
  padding: 14px 16px;
  margin: 12px 0;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.flaw-card .num {
  display: inline-block;
  width: 22px; height: 22px;
  line-height: 22px;
  text-align: center;
  border-radius: 50%;
  background: var(--accent);
  color: #fff;
  font-size: 9pt;
  font-weight: 700;
  margin-right: 8px;
}
.flaw-card .title {
  font-weight: 700;
  font-size: 10.5pt;
}
.flaw-card .body {
  margin-top: 6px;
  font-size: 10pt;
  color: var(--text-secondary);
}
```

```html
<div class="flaw-card">
  <span class="num">1</span>
  <span class="title">卡片标题</span>
  <div class="body">卡片正文内容。</div>
</div>
```

### 判决框 / 深色总结框

```css
.verdict {
  background: #2c2c2c;
  color: #fff;
  border-radius: 6px;
  padding: 16px 18px;
  margin: 18px 0;
}
.verdict .label {
  font-family: 'Noto Serif SC', serif;
  font-size: 11pt;
  font-weight: 700;
  color: #c9760c;
  margin-bottom: 6px;
}
.verdict p { color: #ddd; font-size: 10pt; margin-bottom: 6px; }
.verdict strong { color: #fff; }
```

### 带左边框的价值条目

```css
.value-item {
  margin-bottom: 12px;
  padding-left: 14px;
  border-left: 2px solid var(--accent);
}
.value-item .project {
  font-weight: 700;
  font-size: 10pt;
  color: var(--accent);
}
.value-item p {
  font-size: 10pt;
  margin-bottom: 0;
}
```

### 浅灰背景框（局限性等次要信息）

```css
.muted-box {
  background: #f8f7f5;
  border-radius: 4px;
  padding: 14px 18px;
  margin: 14px 0;
}
.muted-box li {
  font-size: 10pt;
  color: var(--text-secondary);
}
```

---

## 可视化

### 流程图行（横向色块 + 箭头）

```css
.diagram { text-align: center; margin: 20px 0; }
.diagram-row {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0;
}
.diagram-box {
  padding: 10px 16px;
  border-radius: 5px;
  font-size: 10pt;
  font-weight: 500;
  text-align: center;
  min-width: 100px;
  color: #fff;
}
.diagram-arrow {
  font-size: 16pt;
  color: #999;
  padding: 0 6px;
}
.diagram-label {
  font-size: 8.5pt;
  color: var(--text-secondary);
  margin-top: 8px;
}
```

```html
<div class="diagram">
  <div class="diagram-row">
    <div class="diagram-box" style="background:#2c5f3f;">步骤A</div>
    <span class="diagram-arrow">▸</span>
    <div class="diagram-box" style="background:#c9a84c;">步骤B</div>
    <span class="diagram-arrow">▸</span>
    <div class="diagram-box" style="background:#b44a3e;">步骤C</div>
  </div>
  <p class="diagram-label">说明文字</p>
</div>
```

### 时间线

```css
.timeline { margin: 12px 0; }
.timeline-item {
  display: flex;
  gap: 12px;
  margin-bottom: 8px;
  font-size: 9.5pt;
}
.timeline-item .date {
  min-width: 90px;
  font-weight: 700;
  color: var(--accent);
  text-align: right;
}
.timeline-item .event {
  color: var(--text-secondary);
}
```

```html
<div class="timeline">
  <div class="timeline-item">
    <div class="date">2025-06-10</div>
    <div class="event">事件描述</div>
  </div>
</div>
```

---

## 页脚区

```css
.footer {
  margin-top: 28px;
  padding-top: 14px;
  border-top: 1px solid var(--border);
  font-size: 8.5pt;
  color: #999;
}
.footer a {
  color: var(--accent);
  text-decoration: none;
}
```

---

## 分页控制

```css
.page-break { page-break-before: always; }
```

在需要分页的位置插入 `<div class="page-break"></div>`。

**自动分页建议**：
- 每个主要 h2 章节前考虑分页
- 表格尽量不要跨页（短表格加 `page-break-inside: avoid`）
- 图表和其说明文字放在同一页

---

## 配色方案参考

按内容主题选择强调色，替换 `--accent` 和 `--accent-light`：

| 主题 | --accent | --accent-light | 适合 |
|------|----------|----------------|------|
| 暖红（默认） | `#b44a3e` | `#f3e8e6` | 论文、分析、批评 |
| 深蓝 | `#2b5ea7` | `#e8eef6` | 技术报告、数据 |
| 墨绿 | `#2c5f3f` | `#e6f0ea` | 环保、健康、自然 |
| 琥珀 | `#9a6b2f` | `#f5f0e5` | 商业、金融 |
| 石板灰 | `#4a5568` | `#edf0f4` | 中性、通用 |
| 紫檀 | `#6b3a6b` | `#f3e8f3` | 文化、艺术 |

**禁止**：`#6c5ce7`-`#a29bfe` 范围的紫蓝渐变（AI slop 标志色）。
