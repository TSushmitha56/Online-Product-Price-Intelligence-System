import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from scrapers.amazon_scraper import AmazonScraper
from comparison.matcher import normalize_name, is_match

query = "mailbag"
print(f"Testing amazon scraper for '{query}'...")
scraper = AmazonScraper()
results = scraper.search_products(query)

print(f"\nScraped {len(results)} items:")
normalized_query = normalize_name(query)
print(f"Normalized query: '{normalized_query}'")

for i, r in enumerate(results):
    title = r.get('title', '')
    norm_title = normalize_name(title)
    score_55 = is_match(normalized_query, norm_title, threshold=55.0)
    score_40 = is_match(normalized_query, norm_title, threshold=40.0)
    print(f"[{i}] price={r['price']} match@55={score_55} match@40={score_40}  title='{title[:60]}'")
