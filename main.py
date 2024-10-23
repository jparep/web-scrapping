# Import Libraries
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import logging

# Setting up logging for better error tracking and debugging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_driver():
    """Sets up Selenium WebDriver for handling JavaScript-driven content."""
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode (no UI)
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        logging.info("Web driver successfully initialized.")
        return driver
    except Exception as e:
        logging.error(f"Error initializing webdriver: {e}")
        raise

def extract_product_data(driver):
    """Extracts product data from a page using the provided Selenium WebDriver."""
    try:
        # Locate the product elements
        product_elements = driver.find_elements(By.CSS_SELECTOR, ".product-item")
        logging.info(f"Found {len(product_elements)} product elements.")

        # Extract data from each product element (e.g., product name, price, etc.)
        product_data = []
        for product in product_elements:
            try:
                name = product.find_element(By.CSS_SELECTOR, ".product-name").text
                price = product.find_element(By.CSS_SELECTOR, ".product-price").text
                product_data.append({"Name": name, "Price": price})
            except Exception as e:
                logging.warning(f"Error extracting product details: {e}")
        
        return pd.DataFrame(product_data) if product_data else None
    except Exception as e:
        logging.error(f"Error extracting product data: {e}")
        raise

def scrape_dynamic_site(url):
    """Scrapes data from a dynamic website."""
    driver = None
    try:
        driver = setup_driver()
        logging.info(f"Accessing {url}...")
        driver.get(url)

        time.sleep(3)  # Giving the page time to load (consider adjusting or using WebDriverWait)
        
        # Extract and return product data from the website
        return extract_product_data(driver)
    
    except Exception as e:
        logging.error(f"Error during scraping: {e}")
        raise
    finally:
        if driver:
            driver.quit()
            logging.info("WebDriver closed.")

def save_data_to_csv(data, filename='scraped_data.csv'):
    """Saves the scraped data to a CSV file."""
    try:
        data.to_csv(filename, index=False)
        logging.info(f"Scraped data saved to '{filename}'.")
    except Exception as e:
        logging.error(f"Error saving data to CSV: {e}")
        raise

def main():
    url = "https://ibm.com"
    try:
        scraped_data = scrape_dynamic_site(url)
        if scraped_data is not None:
            save_data_to_csv(scraped_data)
            print(scraped_data.head())  # Display first few rows of scraped data
        else:
            logging.warning("No data was scraped.")
    except Exception as e:
        logging.error(f"Failed to scrape the website: {e}")

if __name__ == "__main__":
    main()
