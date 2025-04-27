from src.scrapers.reuters_scraper import ReutersScraper
from ai.text_processing import NewsProcessor

def test_workflow():
    scraper = ReutersScraper()
    processor = NewsProcessor()
    
    print("Testing Reuters scraper...")
    articles = scraper.get_article_links()
    print(f"Found {len(articles)} articles")
    
    print("\nTesting AI summarization...")
    content = scraper.get_article_content(articles[0]['url'])
    summary = processor.summarize(content)
    print(f"Summary: {summary}")

if __name__ == "__main__":
    test_workflow()