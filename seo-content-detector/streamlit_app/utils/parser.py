import requests
from bs4 import BeautifulSoup
import re

def scrape_url(url, timeout=10):
    """get webpage content"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=timeout)
        
        if response.status_code != 200:
            return None, f"Failed to fetch (status {response.status_code})"
        
        return response.content, None
    except requests.exceptions.Timeout:
        return None, "Request timed out"
    except requests.exceptions.RequestException as e:
        return None, f"Request error: {str(e)}"
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"

def parse_html(html_content):
    """grab title and text from webpage"""
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract title
        title = soup.title.string if soup.title else 'No Title Found'
        
        # Find main content
        main_content = soup.find('main') or soup.find('article') or soup.find('body')
        
        if not main_content:
            return title, "No Body Content Found", 0
        
        # Remove unwanted tags
        for tag in main_content(['script', 'style', 'nav', 'footer', 'header']):
            tag.decompose()
        
        # Get clean text
        body_text = main_content.get_text(separator=' ')
        body_text = re.sub(r'\s+', ' ', body_text).strip()
        
        word_count = len(body_text.split())
        
        return title, body_text, word_count
    
    except Exception as e:
        return "Parsing Error", f"Error: {str(e)}", 0