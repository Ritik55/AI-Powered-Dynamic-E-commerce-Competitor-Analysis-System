from .base_scraper import BaseScraper
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class EbayScraper(BaseScraper):
    def scrape_product(self, url):
        driver = self.get_driver()
        driver.get(url)
        
        try:
            title = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "itemTitle"))
            ).text
            price = driver.find_element(By.ID, "prcIsum").text
            rating = driver.find_element(By.CLASS_NAME, "reviews-star-rating").get_attribute("title").split()[0]
            
            reviews = []
            review_elements = driver.find_elements(By.CSS_SELECTOR, "div.review-item")
            for review in review_elements[:5]:
                review_text = review.find_element(By.CSS_SELECTOR, "p.review-item-content").text
                reviews.append(review_text)
            
            return {
                "title": title,
                "price": float(price.replace('$', '').replace(',', '')),
                "rating": float(rating),
                "platform": "eBay",
                "reviews": reviews
            }
        finally:
            driver.quit()
