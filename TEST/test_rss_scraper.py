from src.scrapers.reuters_rss import ReutersRSSScraper

def test_scraper():
    scraper = ReutersRSSScraper()
    articles = scraper.get_articles(max_articles=5)
    
    print(f"Found {len(articles)} articles:")
    for i, article in enumerate(articles, 1):
        print(f"\n{i}. {article['title']}")
        print(f"Category: {article['category']}")
        print(f"Published: {article['published']}")
        print(f"URL: {article['url']}")

if __name__ == "__main__":
    test_scraper()