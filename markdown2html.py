#!/usr/bin/python3

import sys
import os
import re
import hashlib


def convert_markdown_to_html(markdown_text):
    """Convertit un texte Markdown en HTML."""
    html_lines = []
    in_list = False
    list_type = None

    for line in markdown_text.split('\n'):
        line = line.strip()

        # Convert headings
        heading_match = re.match(r'^(#{1,6})\s+(.*)', line)
        if heading_match:
            level = len(heading_match.group(1))
            content = heading_match.group(2)
            html_lines.append(f'<h{level}>{content}</h{level}>')
            continue

        # Convert unordered lists (- item)
        if line.startswith('- '):
            if not in_list or list_type != 'ul':
                if in_list:
                    html_lines.append(f'</{list_type}>')
                html_lines.append('<ul>')
                in_list = True
                list_type = 'ul'
            html_lines.append(f'    <li>{line[2:]}</li>')
            continue

        # Convert ordered lists (* item)
        if line.startswith('* '):
            if not in_list or list_type != 'ol':
                if in_list:
                    html_lines.append(f'</{list_type}>')
                html_lines.append('<ol>')
                in_list = True
                list_type = 'ol'
            html_lines.append(f'    <li>{line[2:]}</li>')
            continue

        # Close list if needed
        if in_list:
            html_lines.append(f'</{list_type}>')
            in_list = False
            list_type = None

        # Convert bold syntax
        line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
        line = re.sub(r'__(.*?)__', r'<em>\1</em>', line)

        # Convert special syntax [[text]] to MD5
        line = re.sub(r'\[\[(.*?)\]\]', 
                      lambda m: hashlib.md5(m.group(1).encode()).hexdigest(), 
                      line)

        # Convert special syntax ((text)) removing all 'c' (case insensitive)
        line = re.sub(r'\(\((.*?)\)\)', 
                      lambda m: m.group(1).replace('c', '').replace('C', ''), 
                      line)

        # Convert paragraphs
        if line:
            line = line.replace('\n', '<br />')
            html_lines.append(f'<p>\n    {line}\n</p>')

    return '\n'.join(html_lines)


def main():
    """Gère l'entrée et la sortie du programme."""
    # Check arguments
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Check if input file exists
    if not os.path.isfile(input_file):
        sys.stderr.write(f"Missing {input_file}\n")
        sys.exit(1)

    # Read input file
    with open(input_file, 'r', encoding='utf-8') as f:
        markdown_content = f.read()

    # Convert markdown to HTML
    html_content = convert_markdown_to_html(markdown_content)

    # Write to output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    sys.exit(0)


if __name__ == "__main__":
    main()
