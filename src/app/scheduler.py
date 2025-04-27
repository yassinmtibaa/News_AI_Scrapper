import time
import schedule
from src.scrapers.reuters_rss import ReutersRSSScraper

def update_cache():
    print("Updating RSS cache...")
    scraper = ReutersRSSScraper()
    scraper.get_articles()  # This will refresh cache
    print("Cache updated at", time.ctime())

# Schedule every 15 minutes
schedule.every(15).minutes.do(update_cache)

if __name__ == '__main__':
    update_cache()  # Run immediately first
    while True:
        schedule.run_pending()
        time.sleep(60)