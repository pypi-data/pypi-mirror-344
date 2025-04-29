# Guidewd Sitemap SEO Tool

**Guidewd** is a command-line tool that analyzes XML sitemaps for SEO optimization.  
It extracts titles, descriptions, keywords, and suggests improvements based on standard SEO best practices.

---

## Features

- Analyze sitemap URLs for SEO metadata
- Check if title and description lengths are SEO-friendly
- Get improvement suggestions for each page
- Output results to a CSV file
- Lightweight and easy to use from the command line

---

## Installation

You can install the package using pip:

```bash
pip install guidewd-sitemap-tool
```

---

## Usage
After installation, you can run the guidewd command directly from your terminal.

- Command-Line Interface:
```bash
guidewd-analyze "path/to/your_sitemap.xml" --output output.csv
```

- `path/to/your_sitemap.xml`: Path to your local sitemap XML file.
- `--output output.csv` (optional): Path to save the output as a CSV file. If not provided, the tool will print the analysis directly to the terminal.

---

## Example
```bash
guidewd-analyze "C:\Users\purva\Downloads\sitemap_final.xml" --output seo_report.csv
```

This will save the SEO analysis in a file called seo_report.csv.

---

## Input
- A valid XML sitemap file containing website URLs.

## Output
- A table containing:
    - URL
    - Title
    - Description
    - Keywords
    - SEO Suggestions
