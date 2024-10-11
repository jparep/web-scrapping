# Import Libraries
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Set up Chrome options for Selenium
chrome_options = Options()
chrome_options.add_argument("--headless") # Run in headless mode (no UI)
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--diasble-dev-shm-usage")