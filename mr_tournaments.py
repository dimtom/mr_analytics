
from common_data import CommonData
from mr_request import MrRequest


def load_tournaments(data: CommonData, date_from, date_to, verbose=False):
    '''
    Tournaments
    https://mafiaratings.com/api/get/tournaments.php?help
    '''

    # url = f"{url_api_get}/tournaments.php?{league_aml}&started_after={date_from}&ended_before={date_to}&lod=1"
    url = f"/tournaments.php?&started_after={date_from}&ended_before={date_to}&lod=1"
    body_json = MrRequest(data.cache).execute(url)

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

    # if verbose:
    #    print(f"Tournaments: {tournaments}")
    return tournaments
