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

# Setting up loggin for better error tracking and debugging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def setup_driver():
    """Setting up Selenium for hadling JavaScript-driven content"""
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless") # Run in headless mode (no UI)
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--diasble-dev-shm-usage")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        logging.info("Web driver successfully initialized.")
        return driver
    except Exception as e:
        logging.error(f"Error Initializing webdriver: {e}")
        raise


def scrape_dynamic_site(url):
    """Scrape data from a dynamic website."""
    driver = None
    try:
        driver = setup_driver()
        logging.info(f"Accessing {url}...")
        driver.get(url)
        
        time.sleep(3) # Giving the page time to load
        
        # Locate the elements to be scraped, modify based on website struture
        product_elements = driver.find_element(By.CSS_SELECTOR, ".product-item")
        logging.info(f"Found {len(product_elements)} product elements.")
        
        # Extract data from the elements (e.g., product name, price, etc.)
        product_data = []
        for product in product_elements:
            name = product.find_elment(By.CSS_SELECTOR, ".product-name").text
            price = product.find_element(By.CSS_SELECTOR, ".product-price").text
            product_data.append({"Name": name, "Price": price})
        return pd.DataFrame(product_data)
    
    except Exception as e:
        logging.error(f"Error during scrapping {e}")
        raise
    finally:
        if driver:
            driver.quit()
            logging.info("WebDriver closed.")

def main():
    url = "https://ibm.com"
    