import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import argparse

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
    print(f"\nThe analysis has been saved to {output_file}")

# Main entry function for command-line execution
def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Analyze a sitemap XML file for SEO optimization.")
    parser.add_argument('sitemap', metavar='sitemap', type=str, help='Path to the sitemap XML file')
    parser.add_argument('--output', type=str, help='Path to save the output CSV file (optional)')
    
    # Parse the arguments
    args = parser.parse_args()

    # Print start message with details
    print("############################################################################################")
    print("# Guidewd Sitemap SEO Tool: Analyzing your Sitemap for SEO Optimization")
    print("# Please ensure your sitemap is a valid XML file containing URLs.")
    print("############################################################################################\n")
    print(f"Input Sitemap File: {args.sitemap}")
    if args.output:
        print(f"Output CSV File: {args.output}")
    else:
        print("No output file specified. Analysis will be printed in the terminal.\n")
    
    print("======Initiating SEO Analysis Using Guidewd. Please Wait.......================\n")

    # Run the analysis
    df = analyze_sitemap(args.sitemap)
    
    # If output file path is provided, save the CSV
    if args.output:
        generate_csv(df, args.output)
    else:
        # Print the DataFrame result in the terminal
        print(df)

if __name__ == '__main__':
    main()
