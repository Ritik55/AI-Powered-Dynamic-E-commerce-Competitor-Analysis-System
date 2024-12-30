from src.scrapers.amazon_scraper import AmazonScraper
from src.scrapers.ebay_scraper import EbayScraper
from src.scrapers.walmart_scraper import WalmartScraper
from src.analysis.sentiment_analyzer import SentimentAnalyzer
from src.analysis.product_matcher import ProductMatcher
from src.utils.proxy_rotator import ProxyRotator
from src.utils.user_agent_rotator import UserAgentRotator
from src.database.db_handler import DatabaseHandler
import concurrent.futures

def scrape_product(scraper, url):
    return scraper.scrape_product(url)

def main():
    proxy_rotator = Pro
