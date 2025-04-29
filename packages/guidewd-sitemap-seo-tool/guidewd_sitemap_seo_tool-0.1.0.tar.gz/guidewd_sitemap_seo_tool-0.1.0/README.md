# Guidewd Sitemap SEO Tool

**Guidewd** is a Sitemap SEO Analysis tool that helps you analyze XML sitemaps for SEO optimization.  
It extracts titles, descriptions, keywords, and suggests improvements.

---

## Features

- Analyze sitemap URLs for SEO metadata
- Check title and description lengths
- Suggest improvements for SEO
- Streamlit web interface
- Command-line usage support

---

## Installation

```bash
pip install guidewd-sitemap-seo-tool
Usage

1. Command Line
To analyze your sitemap directly:

```bash
guidewd-analyze --file uploaded_sitemap.xml
This will output a CSV file with SEO analysis.

2. Streamlit Web App
To launch the Streamlit interface locally:

```bash
streamlit run guidewd/streamlit_app.py
Then open the given localhost URL in your browser.

Input
Upload a .xml sitemap file that contains URLs.

Output
* Table of SEO metadata: Title, Description, Keywords

* SEO improvement suggestions

* Downloadable report (CSV)