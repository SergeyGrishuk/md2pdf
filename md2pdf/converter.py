"""Main conversion pipeline for md2pdf.

Pipeline:
1. Parse frontmatter — extract configuration
2. Pre-process custom syntax — convert extensions to HTML
3. Convert Markdown to HTML — using markdown library
4. Apply stylesheet — wrap HTML with CSS
5. Render PDF — via WeasyPrint
"""

import sys
from pathlib import Path
from typing import Optional

import frontmatter
import markdown
from weasyprint import HTML, CSS

from .extensions import preprocess, postprocess


# Path to default stylesheet (handles PyInstaller bundled resources)
def _get_styles_dir() -> Path:
    if getattr(sys, 'frozen', False):
        # Running as PyInstaller bundle
        return Path(sys._MEIPASS) / "md2pdf" / "styles"
    else:
        # Running as normal Python
        return Path(__file__).parent / "styles"

STYLES_DIR = _get_styles_dir()
DEFAULT_CSS = STYLES_DIR / "default.css"


def parse_document(md_content: str) -> tuple[dict, str]:
    """Parse frontmatter and return config dict and content.
    
    Args:
        md_content: Raw markdown file content
        
    Returns:
        Tuple of (config dict, markdown content without frontmatter)
    """
    post = frontmatter.loads(md_content)
    
    config = {
        "page_numbers": post.get("page-numbers", True),  # Enabled by default
    }
    
    return config, post.content


def markdown_to_html(md_text: str) -> str:
    """Convert markdown text to HTML.
    
    Uses standard markdown extensions for tables, code highlighting, etc.
    """
    extensions = [
        "extra",        # Abbreviations, attribute lists, definition lists, fenced code, footnotes, tables
        "codehilite",   # Syntax highlighting via Pygments
        "fenced_code",  # Fenced code blocks (```)
        "tables",       # Table support
        "toc",          # Table of contents
    ]
    
    extension_configs = {
        "codehilite": {
            "css_class": "highlight",
            "guess_lang": False,
        }
    }
    
    md = markdown.Markdown(extensions=extensions, extension_configs=extension_configs)
    return md.convert(md_text)


def wrap_html(body_html: str, config: dict, custom_css: Optional[Path] = None) -> str:
    """Wrap HTML body with full document structure.
    
    Args:
        body_html: Converted HTML content
        config: Document configuration from frontmatter
        custom_css: Optional path to custom stylesheet
        
    Returns:
        Complete HTML document
    """
    css_path = custom_css if custom_css else DEFAULT_CSS
    css_content = css_path.read_text()
    
    # Add page number CSS if enabled
    if config.get("page_numbers", True):
        page_number_css = """
        @page {
            @bottom-center {
                content: "Page " counter(page) " of " counter(pages);
                font-size: 10pt;
                color: #666;
            }
        }
        """
        css_content += page_number_css
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
{css_content}
    </style>
</head>
<body>
{body_html}
</body>
</html>"""
    
    return html


def convert(
    input_path: Path,
    output_path: Optional[Path] = None,
    custom_css: Optional[Path] = None,
) -> Path:
    """Convert a Markdown file to PDF.
    
    Args:
        input_path: Path to input .md file
        output_path: Optional output path (defaults to input with .pdf extension)
        custom_css: Optional path to custom CSS stylesheet
        
    Returns:
        Path to the generated PDF file
    """
    # Determine output path
    if output_path is None:
        output_path = input_path.with_suffix(".pdf")
    
    # Read input file
    md_content = input_path.read_text()
    
    # Step 1: Parse frontmatter
    config, content = parse_document(md_content)
    
    # Step 2: Pre-process custom syntax
    processed = preprocess(content)
    
    # Step 3: Convert Markdown to HTML
    body_html = markdown_to_html(processed)
    
    # Step 4: Post-process (wrap centered content)
    body_html = postprocess(body_html)
    
    # Step 5: Wrap with full HTML document and CSS
    full_html = wrap_html(body_html, config, custom_css)
    
    # Step 6: Render PDF with WeasyPrint
    html_doc = HTML(string=full_html, base_url=str(input_path.parent))
    html_doc.write_pdf(output_path)
    
    return output_path
