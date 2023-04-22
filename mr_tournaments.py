import json
from mr_api import *
from common_data import CommonData


def load_tournaments(data: CommonData, date_from, date_to, verbose=False):
    '''
    Tournaments
    https://mafiaratings.com/api/get/tournaments.php?help
    '''

    # url = f"{url_api_get}/tournaments.php?{league_aml}&started_after={date_from}&ended_before={date_to}&lod=1"
    url = f"{mr_url_api_get}/tournaments.php?&started_after={date_from}&ended_before={date_to}&lod=1"

    req = Request(url=url, headers=mr_headers)
    with urlopen(req) as response:
        body = response.read()
        body_json = json.loads(body)

    print(f"Found tournaments: {body_json['count']}")
    sorted_tournaments = sorted(
        body_json['tournaments'], key=lambda item: item['end'])
    for tournament in sorted_tournaments:
        club_id = tournament['club_id']
        club_name = data.club_name(club_id)
        club_city = data.club_city(club_id)
        date_finished, _ = tournament['end'].split('T')
        print(
            f"{date_finished}: {tournament['id']:03d} {tournament['name']} ({club_name}, {club_city})")

    # convert to simple tournament
    tournaments = {}
    for item in body_json['tournaments']:
        tournaments[item['id']] = item['name']
    # print(tournaments)

    if verbose:
        print(f"Tournaments: {tournaments}")
    return tournaments
