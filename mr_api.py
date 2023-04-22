from collections import defaultdict
from urllib.request import urlopen, Request

mr_url_home = "https://mafiaratings.com"
mr_url_api_get = f"{mr_url_home}/api/get"
mr_headers = {'User-Agent': 'Mozilla/5.0 Chrome/112.0.0.0'}

mr_league_aml = "league_id=2"
mr_country_canada = 1
mr_country_usa = 4
