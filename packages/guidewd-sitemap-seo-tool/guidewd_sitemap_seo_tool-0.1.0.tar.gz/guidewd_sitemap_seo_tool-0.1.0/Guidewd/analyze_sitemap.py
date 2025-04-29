import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

# Function to analyze the sitemap and return a DataFrame of pages
def analyze_sitemap(sitemap_file):
    # Parse the XML file
    tree = ET.parse(sitemap_file)
    root = tree.getroot()
    urls = []

    # Extract URLs from the sitemap
    for url in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}url"):
        loc = url.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc").text
        urls.append(loc)

    # Analyze each URL to extract meta information
    result = []
    for loc in urls:
        # Fetch the page content
        page_content = fetch_page_content(loc)

        # Parse the HTML
        title, description, keywords = parse_html_meta(page_content)

        # Generate suggestions
        suggestions = generate_suggestions(title, description)

        # Append the result
        result.append([loc, title, description, keywords, suggestions])

    # Convert the list of results to a pandas DataFrame
    df = pd.DataFrame(result, columns=["URL", "Title", "Description", "Keywords", "Suggestions"])

    return df

# Fetch the HTML content of a URL
def fetch_page_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.text
    except requests.exceptions.RequestException as e:
        return ""  # Return empty content if there's an error

# Parse HTML and extract meta information (title, description, keywords)
def parse_html_meta(html_content):
    soup = BeautifulSoup(html_content, "html.parser")

    # Extract title
    title_tag = soup.find("title")
    title = title_tag.text if title_tag else "No Title"

    # Extract meta description
    description_tag = soup.find("meta", attrs={"name": "description"})
    description = description_tag["content"] if description_tag else "No Description"

    # Extract meta keywords
    keywords_tag = soup.find("meta", attrs={"name": "keywords"})
    keywords = keywords_tag["content"] if keywords_tag else "No Keywords"

    return title, description, keywords

# Generate suggestions based on title and description length
def generate_suggestions(title, description):
    suggestions = []

    # Title tag suggestion
    if len(title) < 50 or len(title) > 60:
        suggestions.append("Title tag should be between 50–60 characters.")
    
    # Meta description suggestion
    if len(description) < 120 or len(description) > 160:
        suggestions.append("Meta description should be between 120–160 characters.")

    return "; ".join(suggestions)

# Optional function to generate a CSV file if needed
def generate_csv(df, output_file):
    # Generate the CSV file using pandas
    df.to_csv(output_file, index=False)
