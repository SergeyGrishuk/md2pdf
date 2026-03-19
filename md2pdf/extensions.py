"""Custom syntax pre-processor for md2pdf extensions.

Handles three custom syntax extensions:
1. Page breaks: ---break---
2. Centering: -> text <- (single or multi-line)
3. Page numbers: via frontmatter (page-numbers: true/false)
"""

import re

# Unique markers that won't appear in normal content
CENTER_START = "<!--CENTER_START-->"
CENTER_END = "<!--CENTER_END-->"


def process_page_breaks(text: str) -> str:
    """Convert ---break--- to page break div."""
    pattern = r'^---break---$'
    replacement = '<div class="page-break"></div>'
    return re.sub(pattern, replacement, text, flags=re.MULTILINE)


def mark_centering(text: str) -> str:
    """Mark centered content with placeholders (pre-Markdown processing).
    
    Replaces -> and <- with HTML comment markers that survive Markdown.
    The actual wrapping happens in postprocess() after Markdown conversion.
    """
    # Multi-line centering: -> on its own line, content, <- on its own line
    multiline_pattern = r'^->\s*$\n(.*?)\n^<-\s*$'
    
    def multiline_replacer(match: re.Match) -> str:
        content = match.group(1)
        return f'{CENTER_START}\n{content}\n{CENTER_END}'
    
    text = re.sub(multiline_pattern, multiline_replacer, text, flags=re.MULTILINE | re.DOTALL)
    
    # Single-line centering: -> text <-
    singleline_pattern = r'^->\s*(.+?)\s*<-$'
    
    def singleline_replacer(match: re.Match) -> str:
        content = match.group(1).strip()
        return f'{CENTER_START}\n{content}\n{CENTER_END}'
    
    text = re.sub(singleline_pattern, singleline_replacer, text, flags=re.MULTILINE)
    
    return text


def preprocess(text: str) -> str:
    """Apply pre-Markdown syntax extensions.
    
    Args:
        text: Raw markdown content (frontmatter should already be stripped)
        
    Returns:
        Markdown with markers for post-processing
    """
    text = process_page_breaks(text)
    text = mark_centering(text)
    return text


def postprocess(html: str) -> str:
    """Apply post-Markdown processing to wrap centered content.
    
    Args:
        html: HTML output from Markdown conversion
        
    Returns:
        HTML with centered content wrapped in divs
    """
    # Replace the comment markers with actual centered divs
    # The markers may have been wrapped in <p> tags by Markdown
    
    # Pattern to find CENTER_START...CENTER_END blocks
    pattern = re.compile(
        r'(?:<p>)?' + re.escape(CENTER_START) + r'(?:</p>)?\s*'
        r'(.*?)'
        r'\s*(?:<p>)?' + re.escape(CENTER_END) + r'(?:</p>)?',
        re.DOTALL
    )
    
    def replacer(match: re.Match) -> str:
        content = match.group(1).strip()
        return f'<div class="centered">{content}</div>'
    
    return pattern.sub(replacer, html)

