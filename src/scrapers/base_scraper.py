from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from abc import ABC, abstractmethod

class BaseScraper(ABC):
    def __init__(self, proxy_rotator, user_agent_rotator):
        self.proxy_rotator = proxy_rotator
        self.user_agent_rotator = user_agent_rotator

    def get_driver(self):
        options = Options()
        options.add_argument(f'--proxy-server={self.proxy_rotator.get_proxy()}')
        options.add_argument(f'user-agent={self.user_agent_rotator.get_user_agent()}')
        return webdriver.Chrome(options=options)

    @abstractmethod
    def scrape_product(self, url):
        pass
