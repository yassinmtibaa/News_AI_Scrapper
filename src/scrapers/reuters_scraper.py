import requests
from bs4 import BeautifulSoup
import time
from urllib.robotparser import RobotFileParser

class ReutersScraper:
    def __init__(self):
        self.base_url = "https://www.reuters.com"
        self.session = requests.Session()  # Initialize session here
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.google.com/'
        })
        
    def get_article_links(self):
        """Get links to recent news articles with debug info"""
        try:
            print(f"Attempting to fetch: {self.base_url}/news/archive")
            response = self.session.get(
                f"{self.base_url}/news/archive",
                timeout=10
            )
            print(f"HTTP Status: {response.status_code}")
            
            if response.status_code == 403:
                print("Received 403 Forbidden - Trying alternative approach...")
                return self._fallback_scrape()
                
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Try multiple selector patterns
            selectors = [
                'a[href*="/article/"]',  # New Reuters pattern
                'a[data-testid="Heading"]',  # Old pattern
                'a[class*="heading"]'  # Alternative
            ]
            
            articles = []
            for selector in selectors:
                links = soup.select(selector)
                for link in links:
                    if link.has_attr('href'):
                        url = link['href']
                        if not url.startswith('http'):
                            url = self.base_url + url
                        articles.append({
                            'title': link.text.strip(),
                            'url': url
                        })
                if articles:  # Stop if we found some
                    break
                    
            print(f"Found {len(articles)} articles")
            return articles[:10]  # Return first 10
            
        except Exception as e:
            print(f"Scraping error: {str(e)}")
            return []
    
    def _fallback_scrape(self):
        """Alternative scraping method when blocked"""
        try:
            # Try the business section instead
            response = self.session.get(
                f"{self.base_url}/business",
                timeout=10
            )
            soup = BeautifulSoup(response.text, 'html.parser')
            
            articles = []
            for card in soup.select('[class*="card"]'):
                if card.find('a'):
                    link = card.find('a')
                    url = link['href']
                    if not url.startswith('http'):
                        url = self.base_url + url
                    articles.append({
                        'title': link.text.strip(),
                        'url': url
                    })
            return articles[:10]
        except:
            return []