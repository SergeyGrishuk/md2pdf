# md2pdf

A small CLI tool that converts Markdown files into clean, professional-looking PDFs. Built for people who write in Markdown but occasionally need to hand someone a PDF that doesn't look like a raw text dump.

Uses WeasyPrint under the hood. Supports syntax-highlighted code blocks, tables, and a few simple extensions for things Markdown doesn't handle natively (page breaks, page numbers, centered text) — without polluting your source files with HTML.

## Install

Requires Python 3.10+.

```bash
pip install .
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv pip install .
```

> **Note:** WeasyPrint has system-level dependencies (Pango, GDK-Pixbuf, etc.). See the [WeasyPrint docs](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#installation) if you run into issues.

## Usage

```bash
md2pdf document.md                    # Creates document.pdf
md2pdf document.md -o report.pdf      # Custom output path
md2pdf document.md --css custom.css   # Use your own stylesheet
md2pdf document.md --open             # Open the PDF after conversion
```

## Syntax Extensions

Three extensions on top of standard Markdown. Your source files stay clean and readable.

### Page Breaks

```
---break---
```

A standalone line that forces a page break in the PDF.

### Page Numbers

Controlled via YAML frontmatter:

```yaml
---
page-numbers: true
---
```

Renders "Page 1 of 5" in the footer. Enabled by default — set to `false` to disable.

### Centered Text

Single line:

```
-> This text will be centered <-
```

Multi-line:

```
->
Line one
Line two
<-
```

## Defaults

- A4 page size with 2.5cm/2cm margins
- Serif body text (Georgia), sans-serif headings (Helvetica Neue)
- Dark-themed syntax highlighting for code blocks
- Justified text with automatic hyphenation
- Alternating row colors on tables

Override everything with `--css custom.css`.
