import requests
from bs4 import BeautifulSoup

def request_page():
    url = 'https://sports.ndtv.com/english-premier-league/epl-table/2023-24'        
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    return soup
