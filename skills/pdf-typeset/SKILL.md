---
name: pdf-typeset
description: Typeset structured content into a polished A4 PDF using HTML, CSS, a local HTTP server, and Playwright PDF rendering. Use when the user asks to generate, export, typeset, print, or lay out content as a PDF, including notes, reports, summaries, handouts, course material, and analysis documents.
---

# PDF Typeset

Use this skill to turn structured content into a clean A4 PDF. The reliable path is:

```text
content -> HTML/CSS -> local HTTP server -> Playwright render -> PDF -> cleanup
```

## Inputs

Collect or infer:

- `content`: Markdown, structured notes, report outline, or source text.
- `style`: academic, report, analysis, creative, handout, or neutral.
- `output_filename`: final PDF filename.
- `accent_color`: optional hex color.
- `output_dir`: default `~/Downloads`.

## Style Selection

Read `references/component-library.md` when composing the HTML. Pick only the components needed for the content.

Use these defaults:

- Academic: serif headings, sans-serif body, warm neutral background.
- Report or analysis: sans-serif, clear sectioning, dark table headers.
- Training handout: stronger hierarchy, callout boxes, wide spacing.
- Creative document: restrained accent blocks; avoid decorative clutter.

## HTML Requirements

Create a temporary HTML file in a safe temp directory, for example:

```python
from pathlib import Path
import tempfile, time

work_dir = Path(tempfile.gettempdir()) / "pdf-typeset"
work_dir.mkdir(parents=True, exist_ok=True)
html_path = work_dir / f"pdf-typeset-{int(time.time())}.html"
```

Use this base structure:

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700&family=Noto+Sans+SC:wght@300;400;500;700&display=swap');

  :root {
    --bg: #fafaf8;
    --text: #1a1a1a;
    --text-secondary: #555;
    --accent: #b44a3e;
    --accent-light: #f3e8e6;
    --border: #d4d0c8;
    --table-header: #2c2c2c;
    --table-header-text: #fff;
    --table-stripe: #f5f3ef;
  }

  * { margin: 0; padding: 0; box-sizing: border-box; }
  @page { size: A4; margin: 2.2cm 2cm 2cm 2cm; }
  body {
    font-family: 'Noto Sans SC', 'Segoe UI', sans-serif;
    font-size: 10.5pt;
    line-height: 1.75;
    color: var(--text);
    background: var(--bg);
  }
</style>
</head>
<body>
  <!-- content -->
</body>
</html>
```

## Layout Rules

- Use Noto Sans SC / Noto Serif SC for Chinese documents when web fonts are available.
- Do not use pure black `#000000`; use `#1a1a1a` or softer text colors.
- Avoid purple-blue AI-style gradients.
- Keep cards, tables, and quote blocks inside page boundaries.
- Use at least `12px` vertical spacing between tables, cards, and quote blocks.
- Prevent wide tables and code blocks from overflowing:

```css
table { table-layout: fixed; word-break: break-word; }
pre, code { white-space: pre-wrap; overflow-wrap: anywhere; }
```

## Local Server

Playwright PDF rendering is more reliable through HTTP than direct `file://`.

Start a local server from the temp work directory:

```bash
python -m http.server 8731 --bind 127.0.0.1
```

If the port is busy, use another port in `8700-8799`. Verify the page before rendering:

```bash
curl -s -o /dev/null -w "%{http_code}" "http://127.0.0.1:8731/pdf-typeset-123.html"
```

## Render with Playwright

Use Playwright or the Browser tool to navigate to the local URL, wait for fonts, inspect the layout, then print to PDF.

```javascript
await page.goto("http://127.0.0.1:8731/pdf-typeset-123.html", {
  waitUntil: "networkidle"
});

await page.pdf({
  path: outputPath,
  format: "A4",
  margin: { top: "2.2cm", bottom: "2cm", left: "2cm", right: "2cm" },
  printBackground: true,
  displayHeaderFooter: true,
  headerTemplate: "<div></div>",
  footerTemplate: "<div style=\"font-size:9px;color:#999;text-align:center;width:100%\"><span class=\"pageNumber\"></span></div>"
});
```

Keep CSS `@page` margins and Playwright `margin` values aligned.

## Quality Check

Before returning the PDF:

1. Open or render the PDF preview.
2. Check page breaks: no orphan headings, split cards, broken tables, or cut-off code blocks.
3. Check page use: no final page with only one or two lines unless intentional.
4. Check typography: title hierarchy, body size, line height, and table styles are consistent.
5. Check readability: body text is at least 10pt and line width is not too long.

For documents over one page, revise the HTML and render again if a serious layout problem appears.

## Output

Save the final PDF to:

```text
~/Downloads/{output_filename}.pdf
```

If the user specifies another folder, use that folder. Return the absolute PDF path and file size.

Delete temporary HTML files and stop the local HTTP server when done.

## Common Fixes

- Font not loaded: wait longer or use installed fallback fonts.
- Blank page: verify the HTTP URL with `curl`.
- Content overflow: add `word-break`, reduce table font size, or split the table.
- Bad page break: add `<div class="page-break"></div>` or CSS `page-break-inside: avoid`.

## Boundaries

This skill does PDF layout and rendering. It does not fact-check the source content unless the user asks. If the PDF includes current facts, prices, laws, dates, or model/version claims, verify them before typesetting.
