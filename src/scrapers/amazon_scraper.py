from .base_scraper import BaseScraper
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AmazonScraper(BaseScraper):
    def scrape_product(self, url):
        driver = self.get_driver()
        driver.get(url)
        
        try:
            title = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "productTitle"))
            ).text
            price = driver.find_element(By.CLASS_NAME, "a-price-whole").text
            rating = driver.find_element(By.CLASS_NAME, "a-icon-alt").text.split()[0]
            
            reviews = []
            review_elements = driver.find_elements(By.CSS_SELECTOR, "div[data-hook='review']")
            for review in review_elements[:5]:
                review_text = review.find_element(By.CSS_SELECTOR, "span[data-hook='review-body']").text
                reviews.append(review_text)
            
            return {
                "title": title,
                "price": float(price.replace(',', '')),
                "rating": float(rating),
                "platform": "Amazon",
                "reviews": reviews
            }
        finally:
            driver.quit()
