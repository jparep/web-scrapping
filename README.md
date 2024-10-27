# Dynamic Site Scraper

This project is a web scraper designed to handle JavaScript-driven content using Selenium and BeautifulSoup. It can scrape data from both e-commerce product pages and blog article pages, saving the extracted information to CSV files.

## Features

- **JavaScript Rendering**: Uses Selenium WebDriver to handle JavaScript-driven content.
- **Versatile Scraping**: Can scrape product data from e-commerce pages and article data from blog pages.
- **Data Storage**: Saves extracted data to CSV files for easy analysis and access.
- **Logging**: Provides detailed logs for error tracking and debugging.

## Requirements

- **Python 3.8+**
- **Libraries**:
  - `requests`
  - `pandas`
  - `bs4` (BeautifulSoup)
  - `selenium`
  - `webdriver_manager`

To install the required packages, you can use:

```bash
pip install -r requirements.txt
```


## Project Structure

.
├── DynamicSiteScraper.py       # Main script with scraper class
├── requirements.txt            # Required packages
├── .gitignore                  # Git ignore file
└── README.md                   # Project documentation


## Setup

Install Dependencies

Ensure you have Python 3.8 or newer installed. Install the necessary packages:
 ```bash
 pip install -r requirements.txt
```

## Configure WebDriver

This project uses Chrome WebDriver. webdriver_manager will automatically download and manage the Chrome driver for you.

## Usage

To run the scraper, you can instantiate the DynamicSiteScraper class with the target URL and specify if it is a product or blog page.

## Methods

* `setup_driver()`: Initializes the Selenium WebDriver in headless mode.
* `extract_data()`: Extracts data based on the page type (product or blog).
* `_extract_product_data()`: Extracts product information for e-commerce pages.
* `_extract_blog_data()`: Extracts article information for blog pages.
* `save_to_csv(data, filename)`: Saves extracted data to a CSV file.
* `scrape_and_save(filename)`: Combines all steps to scrape data and save to CSV.

## CLI Execution

To run the scraper directly, navigate to the project directory and execute:

```bash
python DynamicSiteScraper.py
```

This will:

    Scrape the specified product page and save data to products_data.csv.
    Scrape the specified blog page and save data to articles_data.csv.


## Logging

Logging is configured to display messages to the console. You can adjust the log level in the script to control the verbosity.

## Notes

    Ensure Chrome is installed, as webdriver_manager downloads the Chrome driver by default.
    Modify sleep durations or use WebDriverWait if loading times differ significantly across pages.

## License

This project is licensed under the MIT License.
