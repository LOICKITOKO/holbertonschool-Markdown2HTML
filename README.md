# Markdown to HTML Converter

This project implements a simple **Markdown to HTML** converter written in Python.  
It parses a subset of Markdown syntax (headings, lists, paragraphs, bold/emphasis, special tags, etc.)  
and outputs the corresponding HTML.

The script must be run from the command line and follows strict format rules  
as required by the project instructions.

---

##  Features

The script `markdown2html.py` supports:

### ✔️ Headings
Markdown:

Heading 1
Heading 2
Heading 3

HTML:

```html
<h1>Heading 1</h1>
<h2>Heading 2</h2>
<h3>Heading 3</h3>

Unordered Lists

Markdown:

- Item 1
- Item 2


HTML:

<ul>
<li>Item 1</li>
<li>Item 2</li>
</ul>

Ordered Lists

Markdown:

* Item 1
* Item 2


HTML:

<ol>
<li>Item 1</li>
<li>Item 2</li>
</ol>

Paragraphs with line breaks

Markdown:

Hello

I'm a paragraph
with two lines


HTML:

<p>
Hello
</p>
<p>
I'm a paragraph
<br/>
with two lines
</p>

Bold & Emphasis

Markdown → HTML:

Markdown	HTML
**text**	<b>text</b>
__text__	<em>text</em>
Special Transformations
Markdown	Transformation
[[text]]	Replaced by MD5 hash of text
((text))	Removes all c/C characters from text

Example:

[[Hello]] → 8b1a9953c4611296a827abf8c47804d7  
((Chicago)) → hiago

Usage

Run the script as follows:

./markdown2html.py input.md output.html

Error handling

If fewer than 2 arguments:

Usage: ./markdown2html.py README.md README.html


If the input file does not exist:

Missing <filename>


Exit status codes:

Situation	Exit code
Normal execution	0
Error (missing args/file)	1
Requirements

Ubuntu 18.04 LTS

Python 3.7+

File must start with #!/usr/bin/python3

Follow PEP8

Script must be executable:

chmod +x markdown2html.py


No external Markdown libraries allowed

Code must not execute on import

Project Structure
.
├── markdown2html.py
└── README.md

Exiample

Input file (README.md):

# Title
- Hello
- Bye


Command:

./markdown2html.py README.md output.html


Output:

<h1>Title</h1>
<ul>
<li>Hello</li>
<li>Bye</li>
</ul>
