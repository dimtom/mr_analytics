import json
from urllib.request import urlopen, Request

from request_cache import RequestCache

mr_league_aml = "league_id=2"
mr_country_canada = 1
mr_country_usa = 4


class MrRequest:
    cache: RequestCache = None

    mr_url_home = "https://mafiaratings.com"
    mr_url_api_get = f"{mr_url_home}/api/get"
    mr_headers = {'User-Agent': 'Mozilla/5.0 Chrome/112.0.0.0'}

    def __init__(self, cache=None):
        self.cache = cache
        pass

    def execute(self, url: str) -> str:
        full_url = self.mr_url_api_get + url
        response = self.cache.get(full_url)
        if response is None:
            print(f"Request not found in cache: {full_url}")
            req = Request(url=full_url, headers=self.mr_headers)
            with urlopen(req) as response:
                body = response.read()
                response = json.loads(body)
            self.cache.put(full_url, response)
        return response
