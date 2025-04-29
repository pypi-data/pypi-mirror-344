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
python /usr/local/lib/python3.9/site-packages/guidewd/analyze_sitemap.py "/path/to/your/sitemap.xml" --output "/path/to/your/output.csv"

```

- `/path/to/your_sitemap.xml`: Path to your local sitemap XML file.
- `--output "/path/to/your/dir/output.csv": Path to save the output as a CSV file.

---

## Example
```bash
python /usr/local/lib/python3.9/site-packages/guidewd/analyze_sitemap.py "/path/to/your/sitemap.xml" --output "/path/to/your/output.csv"

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
