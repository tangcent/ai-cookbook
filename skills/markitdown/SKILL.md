---
name: markitdown
description: Convert various file formats (PDF, DOCX, XLSX, PPTX, HTML, images, etc.) to Markdown via CLI. Invoke when user needs to extract text from documents or convert files to Markdown format.
---

# MarkItDown Skill

## When to Activate

Activate this skill when the user asks to:

- Extract text from PDF documents
- Convert Word documents to Markdown
- Convert Excel spreadsheets to Markdown tables
- Convert PowerPoint presentations to Markdown
- Convert HTML pages to Markdown
- Extract text from images (OCR)
- Convert EPUB e-books to Markdown
- Extract content from email files (.msg, .eml)

## Prerequisites

- `markitdown` must be installed and available in PATH.
- Install with: `pip install 'markitdown[all]'`

## Hard Rule

For document conversion tasks, **always use `markitdown` CLI**.

- Do **not** use the MarkItDown MCP server — it has been replaced by this CLI skill.
- Do **not** use alternative tools unless markitdown cannot handle the format.

## Installation

```bash
pip install 'markitdown[all]'
```

## Command Reference

### Basic Usage

```bash
markitdown <file_path_or_url>
```

### Convert Local Files

```bash
markitdown document.pdf
markitdown presentation.pptx
markitdown spreadsheet.xlsx
markitdown document.docx
markitdown page.html
markitdown ebook.epub
markitdown email.msg
```

### Convert from URL

```bash
markitdown https://example.com/document.pdf
markitdown https://example.com/page.html
```

### Save Output to File

```bash
markitdown document.pdf > output.md
```

### Read from Stdin

```bash
cat document.pdf | markitdown
curl -s https://example.com/doc.pdf | markitdown
```

## Supported Formats

| Format | Extension | Notes |
|--------|-----------|-------|
| PDF | `.pdf` | Extracts text from PDF documents |
| Word | `.docx` | Microsoft Word documents |
| Excel | `.xlsx` | Microsoft Excel spreadsheets |
| PowerPoint | `.pptx` | Microsoft PowerPoint presentations |
| HTML | `.html`, `.htm` | Web pages |
| Images | `.png`, `.jpg`, `.jpeg`, `.gif`, `.bmp` | Uses OCR if enabled |
| Text | `.txt`, `.md`, `.csv`, `.json`, `.xml` | Plain text formats |
| EPUB | `.epub` | E-book format |
| Outlook | `.msg`, `.eml` | Email messages |

## Workflows

### Extract Text from PDF

1. Verify the file exists:
   ```bash
   ls -la document.pdf
   ```
2. Convert to Markdown:
   ```bash
   markitdown document.pdf
   ```

### Convert Excel to Markdown Table

```bash
markitdown data.xlsx
```

### Convert PowerPoint Presentation

```bash
markitdown slides.pptx
```

### Convert Web Page from URL

```bash
markitdown https://example.com/article.html
```

### Process Multiple Files

```bash
for file in *.pdf; do
  echo "=== $file ==="
  markitdown "$file"
done
```

### Batch Convert with Output Files

```bash
for file in *.pdf; do
  markitdown "$file" > "${file%.pdf}.md"
done
```

## Output Handling

### Preview Large Output

For large documents, preview the first part:

```bash
markitdown large-document.pdf | head -100
```

### Count Output Lines

```bash
markitdown document.pdf | wc -l
```

### Search in Output

```bash
markitdown document.pdf | grep -i "keyword"
```

## Error Handling

### SSL Certificate Errors (macOS)

If you encounter SSL errors on macOS:

1. Install OpenSSL:
   ```bash
   brew install openssl@3
   ```

2. Set the environment variable:
   ```bash
   export SSL_CERT_FILE=/opt/homebrew/etc/openssl@3/cert.pem
   markitdown https://example.com/document.pdf
   ```

### File Not Found

Always verify the file exists before conversion:

```bash
if [ -f "document.pdf" ]; then
  markitdown document.pdf
else
  echo "File not found: document.pdf"
fi
```

### URL Not Accessible

For URLs requiring authentication, download first:

```bash
curl -H "Authorization: Bearer token" -o doc.pdf "https://api.example.com/doc.pdf"
markitdown doc.pdf
```

## Tips

1. **Large Files**: Very large files may produce extensive output. Consider piping to `head` or saving to a file.

2. **URLs with Special Characters**: Quote URLs properly:
   ```bash
   markitdown "https://example.com/doc with spaces.pdf"
   ```

3. **Combine with Other Tools**: Use pipes for powerful workflows:
   ```bash
   markitdown document.pdf | grep -A5 "Chapter 1"
   ```

4. **Check Installation**: Verify markitdown is installed:
   ```bash
   which markitdown && markitdown --help
   ```

## Troubleshooting

- **"markitdown: command not found"** → Install with `pip install 'markitdown[all]'`
- **SSL certificate errors** → Set `SSL_CERT_FILE` environment variable (macOS)
- **Empty output** → The file may be empty, corrupted, or in an unsupported format
- **Permission denied** → Check file permissions with `ls -la <file>`
