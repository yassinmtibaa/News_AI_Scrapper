# 📰 News Data Scraper

_A scalable, ethical web scraper for collecting and analyzing news articles from multiple sources._

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://python.org)
[![Scrapy](https://img.shields.io/badge/Scrapy-2.11%2B-orange?logo=scrapy)](https://scrapy.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## 🚀 Features
- **Multi-source support**: BBC, Reuters, AP News, and more
- **Structured output**: CSV, JSON, SQLite, or direct API integration
- **Resilient scraping**: Auto-retry, proxy rotation, and user-agent spoofing
- **Custom pipelines**: NLP processing, sentiment analysis, and deduplication
- **Compliance-focused**: Built-in rate limiting and `robots.txt` validation

## 📦 Installation

### Prerequisites
- Python 3.10+
- Git

### Setup
``bash
# Clone with submodules (if using pre-built spiders)
git clone --recurse-submodules https://github.com/yourusername/news-scraper.git
cd news-scraper

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Install with pip
pip install -r requirements.txt


⚙️ Configuration
Edit config/settings.toml (recommended over YAML for type safety):

toml
[sources]  
enabled = ["bbc", "reuters", "ap_news"]  
user_agents_file = "config/user_agents.txt"  

[storage]  
format = "parquet"  # Options: csv, json, ndjson, parquet, sqlite  
path = "data/raw"  
partition_cols = ["source", "year_month"]  # For Parquet/Hive-style partitioning  

[scraping]  
request_delay = 1.5  # Seconds between requests  
timeout = 10.0       # Request timeout in seconds  
max_retries = 3      # Per request  
robots_txt_obey = true  
autothrottle = true  # Adaptive delay based on server response  

[proxies]  
rotation_enabled = false  
list_file = "config/proxies.txt"  # Format: protocol://ip:port  
🖥️ Usage
1. Running the Scraper
bash
# Run with default config (all enabled sources)
python -m scraper --config config/settings.toml

# Override specific parameters
python -m scraper \
  --sources bbc reuters \
  --output-format ndjson \
  --output-path data/custom_dir
2. Output Structure
text
data/
├── raw/                  # Raw scraped articles
│   ├── bbc/
│   │   ├── year_month=2024-05/
│   │   │   └── part-00000.parquet  # Partitioned output
│   └── reuters_20240501.ndjson     
├── processed/            # Post-processed data (cleaned/NLP)
│   ├── sentiment_scores.parquet
│   └── entity_recognition/
└── logs/
    ├── scraping_errors.log
    └── performance_metrics.json
3. Advanced Features
python
# Custom pipeline example (add to pipelines.py)
class SentimentAnalysisPipeline:
    def process_item(self, item, spider):
        item["sentiment"] = analyze_sentiment(item["text"])
        return item

# Enable in settings.toml:
[pipelines]
enabled = ["scraper.pipelines.SentimentAnalysisPipeline"]
⚖️ Legal & Best Practices
Compliance Checklist:
✅ robots.txt Validation: Automatically checked via Scrapy middleware

✅ Rate Limiting: 1500ms default delay (adjust per source requirements)

✅ Data Retention: Raw data auto-deleted after 30 days (configurable)

Ethical Guidelines:
text
1. Never scrape copyrighted content behind paywalls  
2. Attribute sources when republishing processed data  
3. Set User-Agent to identify your bot (e.g., "NewsResearchBot/1.0 (+https://yourdomain.com)")  
4. Prefer official APIs (e.g., NewsAPI, Reuters OpenMedia) when available  
📊 Post-Processing
Jupyter Notebook Integration
python
# Example analysis (notebooks/analysis.ipynb)
import pandas as pd
df = pd.read_parquet("data/raw/bbc/year_month=2024-05/")
df["sentiment"].plot(kind="hist")  
Data Validation
bash
# Run checks (via Great Expectations)
python -m pytest tests/data_validation/
Deployment Options
Method	Command	Use Case
Docker	docker compose up scraper	Production deployment
Airflow	airflow tasks run scraper	Scheduled scraping
Serverless	scrapy deploy aws_lambda	Ephemeral workloads
Key Changes from Previous Version:
Switched to TOML for type-safe configuration (with comments)

Added partitioning for Parquet outputs (optimized for analytics)

Explicit pipeline configuration with code examples

Deployment matrix for different production scenarios

Need additions for a specific use case (e.g., academic research vs. commercial)? Let me know!


