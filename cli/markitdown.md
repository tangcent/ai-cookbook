# MarkItDown CLI

- GitHub: [microsoft/markitdown](https://github.com/microsoft/markitdown)

MarkItDown is a CLI tool that converts various file formats (PDF, Word, Excel, PowerPoint, images, HTML, etc.) into Markdown text. It's useful for extracting readable content from documents directly within your AI workflow.

## Key Features

- Convert PDF, DOCX, XLSX, PPTX, HTML, images, and more to Markdown
- Simple command-line interface
- Support for local files and URLs
- Pipe support for integration with other tools

## Installation

```bash
pip install 'markitdown[all]'
```

## Common Commands

| Command | Description |
|---------|-------------|
| `markitdown <file>` | Convert a local file to Markdown |
| `markitdown <url>` | Convert from URL to Markdown |
| `markitdown <file> > output.md` | Save output to file |
| `cat <file> \| markitdown` | Read from stdin |

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

## Usage Examples

```bash
# Convert a PDF document
markitdown report.pdf

# Convert a Word document
markitdown document.docx

# Convert an Excel spreadsheet
markitdown data.xlsx

# Convert a PowerPoint presentation
markitdown slides.pptx

# Convert from a URL
markitdown https://example.com/document.pdf

# Save output to a file
markitdown document.pdf > output.md

# Read from stdin
cat document.pdf | markitdown

# Download and convert in one step
curl -s https://example.com/doc.pdf | markitdown
```

## macOS SSL Setup

On macOS, MarkItDown may fail with SSL certificate errors if the Homebrew OpenSSL cert bundle is missing:

```bash
# Check if cert file exists
if [ -f /opt/homebrew/etc/openssl@3/cert.pem ]; then
  echo "✅ OpenSSL cert found"
else
  echo "❌ Install with: brew install openssl@3"
fi
```

If needed, set the SSL_CERT_FILE environment variable:

```bash
export SSL_CERT_FILE=/opt/homebrew/etc/openssl@3/cert.pem
markitdown https://example.com/document.pdf
```
