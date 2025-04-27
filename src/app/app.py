from flask import Flask, render_template
from src.scrapers.reuters_rss import ReutersRSSScraper
from src.ai.text_processing import NewsProcessor
import logging
from .filters import datetimeformat

app = Flask(__name__)
scraper = ReutersRSSScraper()
processor = NewsProcessor()
app.jinja_env.filters['datetimeformat'] = datetimeformat

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def home():
    try:
        articles = scraper.get_articles(max_age_hours=12, max_articles=10)
    except Exception as e:
        logger.error(f"Error fetching articles: {e}")
        articles = []
    
    # Add AI summaries
    for article in articles:
        if article.get("summary") and len(article["summary"]) > 200:
            article["ai_summary"] = processor.summarize(article["summary"])
    
    return render_template('index.html', articles=articles)

if __name__ == '__main__':
    app.run(debug=True)