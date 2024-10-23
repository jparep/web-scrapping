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
        # Locate the product elements (commonly used CSS classes for scraping e-commerce data)
        product_elements = driver.find_elements(By.CSS_SELECTOR, ".product-item")
        logging.info(f"Found {len(product_elements)} product elements.")

        # Extract data from each product element (e.g., product name, price, etc.)
        product_data = []
        for product in product_elements:
            try:
                name = product.find_element(By.CSS_SELECTOR, ".product-title").text  # Common CSS class for product titles
                price = product.find_element(By.CSS_SELECTOR, ".price").text  # Common CSS class for price
                link = product.find_element(By.CSS_SELECTOR, ".product-link").get_attribute('href')  # Common attribute for links
                product_data.append({"Name": name, "Price": price, "Link": link})
            except Exception as e:
                logging.warning(f"Error extracting product details: {e}")
        
        return pd.DataFrame(product_data) if product_data else None
    except Exception as e:
        logging.error(f"Error extracting product data: {e}")
        raise

def extract_blog_data(driver):
    """Extracts blog article data from a page."""
    try:
        # Locate the article elements (commonly used for blog sites)
        article_elements = driver.find_elements(By.CSS_SELECTOR, ".article-item")
        logging.info(f"Found {len(article_elements)} article elements.")

        # Extract data from each article (e.g., title, content, etc.)
        article_data = []
        for article in article_elements:
            try:
                title = article.find_element(By.CSS_SELECTOR, ".article-title").text  # Common class for article title
                content = article.find_element(By.CSS_SELECTOR, ".article-content").text  # Common class for article content
                link = article.find_element(By.CSS_SELECTOR, ".article-link").get_attribute('href')  # Common class for article link
                article_data.append({"Title": title, "Content": content, "Link": link})
            except Exception as e:
                logging.warning(f"Error extracting article details: {e}")
        
        return pd.DataFrame(article_data) if article_data else None
    except Exception as e:
        logging.error(f"Error extracting article data: {e}")
        raise

def scrape_dynamic_site(url, is_product_page=True):
    """Scrapes data from a dynamic website."""
    driver = None
    try:
        driver = setup_driver()
        logging.info(f"Accessing {url}...")
        driver.get(url)

        time.sleep(3)  # Giving the page time to load (consider adjusting or using WebDriverWait)
        
        # Choose the correct extraction method based on the page type
        if is_product_page:
            return extract_product_data(driver)
        else:
            return extract_blog_data(driver)
    
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
    # Example URL (e-commerce site)
    product_url = "https://example-ecommerce.com/products"  # Replace with actual e-commerce URL
    # Example URL (blog site)
    blog_url = "https://example-blog.com/articles"  # Replace with actual blog URL

    # Scrape products
    try:
        scraped_data = scrape_dynamic_site(product_url, is_product_page=True)
        if scraped_data is not None:
            save_data_to_csv(scraped_data, filename='products_data.csv')
            print(scraped_data.head())  # Display first few rows of scraped product data
        else:
            logging.warning("No product data was scraped.")
    except Exception as e:
        logging.error(f"Failed to scrape the product page: {e}")
    
    # Scrape blog articles
    try:
        scraped_articles = scrape_dynamic_site(blog_url, is_product_page=False)
        if scraped_articles is not None:
            save_data_to_csv(scraped_articles, filename='articles_data.csv')
            print(scraped_articles.head())  # Display first few rows of scraped article data
        else:
            logging.warning("No article data was scraped.")
    except Exception as e:
        logging.error(f"Failed to scrape the blog page: {e}")

if __name__ == "__main__":
    main()
