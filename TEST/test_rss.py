import feedparser

# Test with Reuters RSS feed
feed_url = "https://www.reutersagency.com/feed/?best-topics=tech&post_type=best"
feed = feedparser.parse(feed_url)

# Proper way to check feed status
if feed.get('bozo', 0) == 1:
    print(f"Error parsing feed: {feed.bozo_exception}")
else:
    print(f"Successfully parsed feed")
    print(f"Feed version: {feed.version}")
    print(f"Found {len(feed.entries)} articles")
    
    for i, entry in enumerate(feed.entries[:3], 1):
        print(f"\nArticle {i}:")
        print(f"Title: {entry.get('title', 'No title')}")
        print(f"Link: {entry.get('link', 'No link')}")
        print(f"Published: {entry.get('published', 'No date')}")
        print(f"Summary: {entry.get('summary', 'No summary')[:100]}...")