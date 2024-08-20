import requests
from bs4 import BeautifulSoup

def check_scraping_allowed(url):  
    response = requests.get(f'{url}/robots.txt')
    page_contents = BeautifulSoup(response.text, 'html.parser')
    print(page_contents)

url = 'https://sports.ndtv.com/'
check_scraping_allowed(url)