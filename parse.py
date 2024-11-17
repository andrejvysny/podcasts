
from bs4 import BeautifulSoup
import requests


def get_content(url):   
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }   

    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code != 200:
        return None
    soup = BeautifulSoup(response.text, 'html.parser')
    for tag in soup(['nav', 'footer', 'script', 'style']):
        tag.decompose()

    if soup.find('body') is None:
        return None

    return soup.find('body').get_text().strip().replace('\n\n\n', '\n').replace('\n\n', '\n').replace('    ', ' ')
    
