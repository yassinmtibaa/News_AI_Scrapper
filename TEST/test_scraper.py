from src.scrapers.reuters_scraper import ReutersScraper

def test_reuters_scraper():
    print("=== Testing Reuters Scraper ===")
    scraper = ReutersScraper()
    
    # Test article links
    articles = scraper.get_article_links()
    print(f"\nFound {len(articles)} articles:")
    for i, article in enumerate(articles[:3]):  # Print first 3 as sample
        print(f"{i+1}. {article['title']}")
        print(f"   {article['url']}")
    
    # Test article content
    if articles:
        print("\nTesting article content extraction...")
        content = scraper.get_article_content(articles[0]['url'])
        print(f"\nFirst paragraph:\n{content[:500]}...")
    else:
        print("\nNo articles found to test content extraction")

if __name__ == "__main__":
    test_reuters_scraper()