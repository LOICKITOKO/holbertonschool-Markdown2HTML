
# Markdown2HTML
## 📌 Features

✅ Converts Markdown to HTML with customizable options

✅ Supports standard Markdown syntax

✅ Easy to integrate into build processes or workflows

✅ Command-line interface for easy use


## 🚀 Installation


Markdown2HTML requires Node.js and npm installed on your system. Install the tool globally using:
```bash
  npm install -g markdown2html
```
## 🛠️ Usage
To convert a Markdown file to HTML, use the following command:
```bash
  markdown2html input.md -o output.html
```
## 🔧 Available Options:

-o, --output <file> → Specify the output file

-t, --template <file> → Use a custom HTML template.

-h, --help → Display help information.
## 💡 Examples
Convert a Markdown file to HTML:
```bash
  markdown2html README.md -o README.html
```
Convert a Markdown file using a custom template:
```bash
  markdown2html input.md -t custom-template.html -o output.html
```
## 📦 API
You can also use Markdown2HTML in your Node.js scripts:
```bash
const markdown2html = require('markdown2html');

markdown2html.renderFile('input.md', 'output.html', (err) => {
  if (err) {
    console.error('Error converting Markdown to HTML:', err);
  } else {
    console.log('Markdown converted to HTML successfully!');
  }
});
```
























