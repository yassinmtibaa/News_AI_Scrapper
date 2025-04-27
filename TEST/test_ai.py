from src.ai.text_processing import NewsProcessor
from src.scrapers.reuters_scraper import ReutersScraper

processor = NewsProcessor()
scraper = ReutersScraper()

# Get first article
article = scraper.get_article_links()[0]
content = scraper.get_article_content(article['url'])

# Process it
summary = processor.summarize(content)
print(f"Original Length: {len(content)} characters")
print(f"Summary Length: {len(summary)} characters")
print("\nSummary:")
print(summary)