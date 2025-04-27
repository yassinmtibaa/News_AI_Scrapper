# Python libraries for RSS feed parsing, caching, and handling HTTP requests
import feedparser as ET
import pytz
import pickle
import time
import urllib.request
import socket
import logging


from pathlib import Path  # For handling file paths
from datetime import datetime, timedelta  # For date and time manipulation

# Configure socket timeout for better reliability in network requests
socket.setdefaulttimeout(10)

class ReutersRSSScraper:
    """
    A scraper for fetching and processing articles from Reuters RSS feeds.
    """

    def __init__(self, theme="general", cache_file="cache.pkl"):
        """
        Initialize the ReutersRSSScraper with a specific theme and cache file.
        :param theme: The theme or category of news to scrape (default is 'general').
        :param cache_file: Path to the cache file (default is 'cache.pkl').
        """
        self.theme = theme
        self.cache_file = Path(cache_file)
        self.feed_url = f"https://www.reutersagency.com/feed/?best-topics={theme}&post_type=best"

    def _fetch_articles(self, max_age_hours=24, max_articles=10):
        """
        Fetch articles from the Reuters RSS feed.
        :param max_age_hours: Maximum age of articles to fetch in hours.
        :param max_articles: Maximum number of articles to fetch.
        :return: A list of articles with title, link, and publication date.
        """
        try:
            # Reuters RSS feed URL
            url = "https://www.reutersagency.com/feed/?best-topics=tech&post_type=best"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            req = urllib.request.Request(url, headers=headers)

            # Fetch the RSS feed data
            with urllib.request.urlopen(req) as response:
                data = response.read()

            # Parse the RSS feed XML
            root = ET.fromstring(data)
            articles = []
            now = datetime.utcnow()
            max_age = now - timedelta(hours=max_age_hours)

            # Iterate through each item in the RSS feed
            for item in root.findall(".//item"):
                title = item.find("title").text
                link = item.find("link").text
                pub_date = item.find("pubDate").text

                # Convert pubDate to a datetime object
                pub_date_dt = datetime.strptime(pub_date, "%a, %d %b %Y %H:%M:%S %z").replace(tzinfo=None)

                # Filter articles by age
                if pub_date_dt >= max_age:
                    articles.append({
                        "title": title,
                        "link": link,
                        "pub_date": pub_date_dt
                    })

                # Stop if the maximum number of articles is reached
                if len(articles) >= max_articles:
                    break

            return articles

        except Exception as e:
            logging.error(f"Error fetching {url}: {str(e)}")
            return []

    def load_cache(self):
        """
        Load cached data from the cache file.
        :return: Cached data or an empty dictionary if the cache file doesn't exist.
        """
        try:
            if self.cache_file.exists():
                with open(self.cache_file, "rb") as f:
                    return pickle.load(f)
            return {}
        except Exception as e:
            logging.error(f"Cache error: {str(e)}")
            return {}

    def save_cache(self, data):
        """
        Save data to the cache file.
        :param data: Data to be cached.
        """
        try:
            with open(self.cache_file, "wb") as f:
                pickle.dump(data, f)
        except Exception as e:
            logging.error(f"Cache error: {str(e)}")

    def get_articles(self, max_articles=10, max_age_hours=24):
        """
        Get articles from the RSS feed, handling errors and caching.
        :param max_articles: Maximum number of articles to fetch.
        :param max_age_hours: Maximum age of articles to fetch in hours.
        :return: A list of articles.
        """
        try:
            # Fetch articles from the RSS feed
            articles = self._fetch_articles(max_age_hours=max_age_hours, max_articles=max_articles)
            return articles
        except urllib.error.HTTPError as e:
            logging.error(f"HTTP Error: {e.code} - {e.reason}")
            return []
        except urllib.error.URLError as e:
            logging.error(f"URL Error: {e.reason}")
            return []
        except ET.ParseError as e:
            logging.error(f"XML parsing error: {e}")
            return []
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            return []