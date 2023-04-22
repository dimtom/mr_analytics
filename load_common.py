from mr_api import *
import json


def load_countries(verbose=False):
    '''
    Loading all countries 
    https://mafiaratings.com/api/get/countries.php?help
    '''

    print("Loading countries...")

    url = f"{mr_url_api_get}/countries.php"
    req = Request(url=url, headers=mr_headers)
    with urlopen(req) as response:
        body = response.read()
        body_json = json.loads(body)

    if verbose:
        print(f"Loaded countries: {body_json['count']}")

    # convert json to simple dict country_id -> name
    countries = {}
    for item in body_json['countries']:
        countries[item['id']] = item['country']

    if verbose:
        print(countries)
    return countries


def load_cities(verbose=False):
    '''
    Loading cities: ONLY from Canada (country=1) and USA (country=4)
    https://mafiaratings.com/api/get/cities.php?help
    '''

    print("Loading cities...")
    big_number = 5000

    country_ids = [mr_country_canada, mr_country_usa]
    body_all_cities = []
    for country_id in country_ids:
        url = f"{mr_url_api_get}/cities.php?country={country_id}&page_size={big_number}"
        req = Request(url=url, headers=mr_headers)
        with urlopen(req) as response:
            body = response.read()
            body_json = json.loads(body)

        print(
            f"Country id: {country_id}. Loaded cities: {body_json['count']} - in current page {len(body_json['cities'])}")
        body_all_cities.extend(body_json['cities'])

    # convert json to simple dict city_id -> name
    cities = {}
    for item in body_all_cities:
        cities[item['id']] = item['city']

    print(f"Total cities found: {len(cities)}")
    if verbose:
        print(cities)
    return cities


def load_clubs(cities, countries, verbose=False):
    '''
    Loading clubs
    https://mafiaratings.com/api/get/clubs.php?help
    '''

    print("Loading clubs...")

    # find all clubs in AML, but there are some depricated clubs, like Seattle Mafia Club
    #url = f"{url_api_get}/clubs.php?{league_aml}"

    # another approach, get all the clubs in Canada and USA
    ids = [mr_country_canada, mr_country_usa]
    clubs_json = []
    for country_id in ids:
        url = f"{mr_url_api_get}/clubs.php?country_id={country_id}"
        req = Request(url=url, headers=mr_headers)
        with urlopen(req) as response:
            body = response.read()
            body_json = json.loads(body)

        country_name = countries[country_id]
        club_count = body_json['count']
        print(
            f"Found clubs in country {country_name}: {club_count}")
        clubs_json.extend(body_json['clubs'])

        if verbose:
            sorted_clubs = sorted(
                body_json['clubs'], key=lambda item: item['id'])
            for club in sorted_clubs:
                print(
                    f"id: {club['id']:02d} name: {club['name']} city: {cities[club['city_id']]}")

    clubs = {}
    for item in clubs_json:
        clubs[item['id']] = {'name': item['name'],
                             'city': cities[item['city_id']]}

    # workaround - BlackCat club is not returned (cancelled?)
    blackcat_club_id = 41
    print("Adding club manually: {blackcat_club_id}")
    clubs[blackcat_club_id] = {
        'name': "Black Cat", 'city': "San Francisco"}

    # workaround - seattle club is not returned (cancelled?)
    seattle_club_id = 42
    print("Adding club manually: {seattle_club_id}")
    clubs[seattle_club_id] = {
        'name': "Seattle Mafia Club", 'city': "Seattle"}

    print(f"Total clubs: {len(clubs)}")
    return clubs
