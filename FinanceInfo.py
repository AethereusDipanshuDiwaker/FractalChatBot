import requests
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import re
import sys
import io
import multiprocessing

# Wrap sys.stdout with a custom encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

API_KEY = 'a46eec33-475c-4658-970a-09c2ea06051e'

def extract_plain_text(html):
    soup = BeautifulSoup(html, 'html.parser')
    # Remove script and style tags
    for script in soup(["script", "style"]):
        script.extract()
    # Remove all remaining tags and get plain text
    plain_text = soup.get_text(separator=' ')
    # Remove extra whitespaces
    plain_text = re.sub('\s+', ' ', plain_text).strip()
    return plain_text


def get_scrapeops_url(url):
    payload = {'api_key': API_KEY, 'url': url}
    query_string = urlencode(payload)
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + query_string
    return proxy_url


def scrape_url(url):
    r = requests.get(get_scrapeops_url(url))
    return extract_plain_text(r.text)


def finance():
    urls = [
        'https://www.crunchbase.com/organization/fractal-analytics/',
        'https://www.crunchbase.com/organization/fractal-analytics/company_financials',
        'https://www.crunchbase.com/organization/fractal-analytics/org_similarity_overview'
    ]
    
    with multiprocessing.Pool() as pool:
        result_texts = pool.map(scrape_url, urls)
        combined_text = ''.join(result_texts)
        print(combined_text)
    return combined_text


