import requests
from bs4 import BeautifulSoup

# URL of the webpage you want to scrape
url = "https://example-news-website.com"

# Send a GET request to the webpage
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the webpage content with BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Find all article titles (assuming they are in <h2> tags with class 'article-title')
    article_titles = soup.find_all('h2', class_='article-title')
    
    # Loop through the titles and print them
    for idx, title in enumerate(article_titles, 1):
        print(f"{idx}. {title.get_text()}")
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
