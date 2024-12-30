from .base_scraper import BaseScraper
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class WalmartScraper(BaseScraper):
    def scrape_product(self, url):
        driver = self.get_driver()
        driver.get(url)
        
        try:
            title = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h1.prod-ProductTitle"))
            ).text
            price = driver.find_element(By.CSS_SELECTOR, "span.price-characteristic").text
            rating = driver.find_element(By.CSS_SELECTOR, "span.average-rating").text.split()[0]
            
            reviews = []
            review_elements = driver.find_elements(By.CSS_SELECTOR, "div.review-text")
            for review in review_elements[:5]:
                reviews.append(review.text)
            
            return {
                "title": title,
                "price": float(price.replace('$', '').replace(',', '')),
                "rating": float(rating),
                "platform": "Walmart",
                "reviews": reviews
            }
        finally:
            driver.quit()
