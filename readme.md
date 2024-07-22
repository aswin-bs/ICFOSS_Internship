# Malayalam Scrapy 

This is a Scrapy project for web scraping Malayalam Scraper.


## Updations

Updations did on the Malayalam Scraper
1. Scraper With Malayalam Data Extraction
2. Improved Performance by incorporating concurrency into the scraper

## Getting Started

These instructions will help you set up the project and get it running on your local machine.

### Prerequisites

You need to have Python and pip installed on your system. If you don't have them installed, you can download Python from [python.org](https://www.python.org/downloads/) and pip will be installed along with it.

### Setting up a Virtual Environment

It's a good practice to create a virtual environment to isolate your project dependencies. If you haven't already, you can do this using the following commands:

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate
# On macOS and Linux
source venv/bin/activate
```

### Installing Project Dependencies

Once you have your virtual environment set up and activated, you can install the project dependencies listed in the `requirements.txt` file. To do this, run the following command:

```bash
pip install -r requirements.txt
```

This will install all the necessary packages, including Scrapy, in your virtual environment.

### Running the Scrapy Spider

Now that you have the project set up and dependencies installed, you can run the Scrapy spider. To run the spider, use the following command:

```bash
cd corpus1
scrapy crawl quotes
```


