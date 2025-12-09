#!/usr/bin/python3
"""
Markdown to HTML converter

This module contains a script that converts a Markdown file into HTML.
It supports headings, unordered and ordered lists, paragraphs with line breaks,
bold and emphasis, and special transformations for [[text]] and ((text)).

Usage:
    ./markdown2html.py input.md output.html
"""

import sys
import os
import re
import hashlib

def md5_text(text):
    """Return md5 hex digest of text."""
    return hashlib.md5(text.encode()).hexdigest()


def remove_c(text):
    """Remove all 'c' or 'C' characters."""
    return re.sub(r'(?i)c', '', text)


def process_inline(text):
    """Apply inline transformations: bold, emphasis, [[ ]], (( ))."""
    # Bold ** **
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)

    # Emphasis __ __
    text = re.sub(r'__(.+?)__', r'<em>\1</em>', text)

    # [[ ]] → md5
    text = re.sub(
        r'\[\[(.+?)\]\]',
        lambda m: md5_text(m.group(1)),
        text
    )

    # (( )) → remove c/C
    text = re.sub(
        r'\(\((.+?)\)\)',
        lambda m: remove_c(m.group(1)),
        text
    )

    return text


def flush_paragraph(buffer, out):
    """Flush paragraph buffer into <p> block."""
    if not buffer:
        return

    out.append("<p>")
    for i, line in enumerate(buffer):
        line = process_inline(line)
        if i == 0:
            out.append(line)
        else:
            out.append("<br/>")
            out.append(line)
    out.append("</p>")


def main():
    # --- Argument verification ---
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        sys.exit(1)

    md_file = sys.argv[1]
    html_file = sys.argv[2]

    # --- File existence ---
    if not os.path.exists(md_file):
        sys.stderr.write(f"Missing {md_file}\n")
        sys.exit(1)

    # --- Read MD file ---
    with open(md_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Add an empty line at end to simplify closing blocks
    lines.append("\n")

    out = []

    in_ul = False
    in_ol = False
    in_paragraph = False
    paragraph_buffer = []

    for raw in lines:
        line = raw.rstrip("\n")

        # Empty line -> close paragraph if open
        if line.strip() == "":
            if in_paragraph:
                flush_paragraph(paragraph_buffer, out)
                paragraph_buffer = []
                in_paragraph = False

            if in_ul:
                out.append("</ul>")
                in_ul = False

            if in_ol:
                out.append("</ol>")
                in_ol = False

            continue

        # ---------- HEADINGS ----------
        match = re.match(r'^(#{1,6})\s+(.*)', line)
        if match:
            if in_paragraph:
                flush_paragraph(paragraph_buffer, out)
                paragraph_buffer = []
                in_paragraph = False

            if in_ul:
                out.append("</ul>")
                in_ul = False

            if in_ol:
                out.append("</ol>")
                in_ol = False

            level = len(match.group(1))
            content = process_inline(match.group(2))
            out.append(f"<h{level}>{content}</h{level}>")
            continue

        # ---------- UL LIST ----------
        if line.startswith("- "):
            if in_paragraph:
                flush_paragraph(paragraph_buffer, out)
                paragraph_buffer = []
                in_paragraph = False

            if not in_ul:
                if in_ol:
                    out.append("</ol>")
                    in_ol = False
                out.append("<ul>")
                in_ul = True

            content = process_inline(line[2:])
            out.append(f"<li>{content}</li>")
            continue

        # ---------- OL LIST ----------
        if line.startswith("* "):
            if in_paragraph:
                flush_paragraph(paragraph_buffer, out)
                paragraph_buffer = []
                in_paragraph = False

            if not in_ol:
                if in_ul:
                    out.append("</ul>")
                    in_ul = False
                out.append("<ol>")
                in_ol = True

            content = process_inline(line[2:])
            out.append(f"<li>{content}</li>")
            continue

        # ---------- PARAGRAPH ----------
        if in_ul:
            out.append("</ul>")
            in_ul = False

        if in_ol:
            out.append("</ol>")
            in_ol = False

        paragraph_buffer.append(line)
        in_paragraph = True

    # Safety — close paragraph if still open
    if in_paragraph:
        flush_paragraph(paragraph_buffer, out)

    # --- Write output file ---
    with open(html_file, 'w', encoding='utf-8') as f:
        for l in out:
            f.write(l + "\n")

    sys.exit(0)


if __name__ == "__main__":
    main()
