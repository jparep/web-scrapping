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

# Setting up Selenium for hadling JavaScript-driven content
def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless") # Run in headless mode (no UI)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--diasble-dev-shm-usage")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


# Example function to scrape data from a dynamic website
def scrape_dynamic_site(url):
    driver = setup_driver()
    driver.get(url)
    
    time.sleep(3) # Giving the page time to load
    
    # Locate the elements to be scraped, modify based on website struture
    product_elements = driver.find_element(By.CSS_SELECTOR, ".product-item")
    

