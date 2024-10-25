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

# Configure logging for better error tracking and debugging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class DynamicSiteScraper:
    def __init__(self, url, is_product_page=True):
        self.url = url
        self.is_product_page = is_product_page
        self.driver = None

    def setup_driver(self):
        """Sets up Selenium WebDriver for handling JavaScript-driven content."""
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode (no UI)
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            logging.info("Web driver successfully initialized.")
        except Exception as e:
            logging.error(f"Error initializing webdriver: {e}")
            raise

    def extract_data(self):
        """Extracts either product or blog data based on the page type."""
        try:
            self.driver.get(self.url)
            time.sleep(3)  # Adjust or use WebDriverWait if needed

            if self.is_product_page:
                return self._extract_product_data()
            else:
                return self._extract_blog_data()
        except Exception as e:
            logging.error(f"Error accessing {self.url}: {e}")
            return None

    def _extract_product_data(self):
        """Extracts product data if the page is an e-commerce site."""
        try:
            product_elements = self.driver.find_elements(By.CSS_SELECTOR, ".product-item")
            logging.info(f"Found {len(product_elements)} product elements.")
            product_data = [
                {
                    "Name": product.find_element(By.CSS_SELECTOR, ".product-title").text,
                    "Price": product.find_element(By.CSS_SELECTOR, ".price").text,
                    "Link": product.find_element(By.CSS_SELECTOR, ".product-link").get_attribute('href')
                }
                for product in product_elements
            ]
            return pd.DataFrame(product_data) if product_data else None
        except Exception as e:
            logging.error(f"Error extracting product data: {e}")
            return None

    def _extract_blog_data(self):
        """Extracts blog data if the page is a blog site."""
        try:
            article_elements = self.driver.find_elements(By.CSS_SELECTOR, ".article-item")
            logging.info(f"Found {len(article_elements)} article elements.")
            article_data = [
                {
                    "Title": article.find_element(By.CSS_SELECTOR, ".article-title").text,
                    "Content": article.find_element(By.CSS_SELECTOR, ".article-content").text,
                    "Link": article.find_element(By.CSS_SELECTOR, ".article-link").get_attribute('href')
                }
                for article in article_elements
            ]
            return pd.DataFrame(article_data) if article_data else None
        except Exception as e:
            logging.error(f"Error extracting blog data: {e}")
            return None

    def save_to_csv(self, data, filename):
        """Saves the extracted data to a CSV file."""
        try:
            data.to_csv(filename, index=False)
            logging.info(f"Scraped data saved to '{filename}'.")
        except Exception as e:
            logging.error(f"Error saving data to CSV: {e}")
            raise

    def scrape_and_save(self, filename):
        """Main function to execute scraping and save data."""
        self.setup_driver()
        data = self.extract_data()
        
        if data is not None:
            self.save_to_csv(data, filename)
        else:
            logging.warning("No data was scraped.")
        
        # Clean up by quitting the driver
        if self.driver:
            self.driver.quit()
            logging.info("WebDriver closed.")


if __name__ == "__main__":
    # Instantiate and scrape product page
    product_scraper = DynamicSiteScraper("https://example-ecommerce.com/products", is_product_page=True)
    product_scraper.scrape_and_save("products_data.csv")

    # Instantiate and scrape blog page
    blog_scraper = DynamicSiteScraper("https://example-blog.com/articles", is_product_page=False)
    blog_scraper.scrape_and_save("articles_data.csv")
