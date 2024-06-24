# Import necessary libraries
from scrapy.linkextractors import LinkExtractor
import scrapy
from datetime import datetime
import re
from bs4 import BeautifulSoup
import concurrent.futures
import requests
from urllib.parse import urlparse
import csv

# Define the number of threads for concurrent scraping
NUM_THREADS = 4

# Create a list of URLs to be scraped
urls_to_scrape = [
    "https://mm.kerala.gov.in",
    "https://www.kerala.gov.in",
]

# Function to remove HTML tags from a given HTML content
def remove_tags(html:str)-> str:
    """
    Removes HTML tags and extracts text content from the provided HTML.
    
    Args:
        html (str): The HTML content to process.
        
    Returns:
        str: The extracted text content without HTML tags.
    """
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    # Remove style and script tags from the parsed content
    for data in soup(["style", "script"]):
        data.decompose()

    # Extract and join the text content from the remaining tags
    return " ".join(re.findall(r'[\u0D00-\u0D7F]+', " ".join(soup.stripped_strings)))

# Define a Scrapy spider to crawl and scrape web pages
class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = urls_to_scrape

    def save_metadata_to_csv(self, metadata):
        with open('metadata.csv', 'a', newline='') as csvfile:
            fieldnames = ['filename', 'domain_name', 'date_time_scraped', 'url']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write header if the file is empty
            if csvfile.tell() == 0:
                writer.writeheader()

            writer.writerow(metadata)

    def parse(self, response):
        """
        Parses the response from a URL and extracts text content from it.
        
        Args:
            response (scrapy.http.Response): The response from the crawled URL.
        """
        # Remove HTML tags and extract text content from the response
        text = remove_tags(response.text)

        # Check if the extracted text is substantial (more than 50 characters)
        if len(text) > 50:

            time = datetime.now()
            filename = f"res/{time}.txt"
            domain_name = urlparse(response.url).netloc
            date_time_scraped = time.strftime('%Y-%m-%d %H:%M:%S')

            # Save the extracted text to a file named with the current timestamp
            with open(filename, "w+") as f:
                f.write(text)
            
            # Extracted metadata to be saved in CSV
            metadata = {
                'filename': filename,
                'domain_name': domain_name,
                'date_time_scraped': date_time_scraped,
                'url': response.url,
            }

            # Save metadata to CSV
            self.save_metadata_to_csv(metadata)

        # Follow links on the page and recursively call the 'parse' method for each link
        for a in LinkExtractor(deny_domains="").extract_links(response):
            x = a.url.split("/", 3)
            if x[2].endswith(".gov.in"):
                yield response.follow(a, callback=self.parse)

# Function to scrape a single page and save its text content to a file
def scrape_page(url:str)->None:
    """
    Scrapes a single web page, extracts text content, and saves it to a file.
    
    Args:
        url (str): The URL of the web page to scrape.
    """
    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url)

        # Check if the response status code is 200 (indicating a successful request)
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup and extract text content
            soup = BeautifulSoup(response.text, "html.parser")
            text = " ".join(re.findall(r'[\u0D00-\u0D7F]+', " ".join(soup.stripped_strings)))

            # Save the extracted text to a file named with the current timestamp
            with open(f"res/{datetime.now()}.txt", "w+") as f:
                f.write(text)
    except Exception as e:
        print('Error', e)

# Use concurrent.futures to scrape the URLs concurrently using multiple threads
with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
    # Map the 'scrape_page' function to each URL for concurrent scraping
    executor.map(scrape_page, urls_to_scrape)
