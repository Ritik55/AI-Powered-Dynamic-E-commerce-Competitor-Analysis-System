import requests
from itertools import cycle

class ProxyRotator:
    def __init__(self):
        self.proxies = self.fetch_proxies()
        self.proxy_pool = cycle(self.proxies)

    def fetch_proxies(self):
        response = requests.get('https://free-proxy-list.net/')
        proxies = []
        for row in response.text.split('\n')[1:-1]:
            fields = row.split()
            if len(fields) > 1:
                ip, port = fields[0], fields[1]
                proxies.append(f"{ip}:{port}")
        return proxies

    def get_proxy(self):
        return next(self.proxy_pool)
