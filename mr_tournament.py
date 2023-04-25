from classes import *
from mr_request import MrRequest
from common_data import CommonData


def get_tournament_info(data, tournament_id: int):
    url = f"/tournaments.php?tournament_id={tournament_id}"
    body_json = MrRequest(data.cache).execute(url)

    # there MUST be one and only ONE tournament
    assert(body_json['count'] == 1)
    tournament_json = body_json['tournaments'][0]

    tournament_name = tournament_json['name']
    club_id = tournament_json['club_id']
    club = data.clubs[club_id] if club_id in data.clubs else None
    city = club.city if club else None

    return Tournament(id=tournament_id, name=tournament_name, club=club, city=city)


def get_tournament_events(data, tournament_id: int):
    url = f"/events.php?tournament_id={tournament_id}"
    body_json = MrRequest(data.cache).execute(url)

    # need to find some events
    assert(body_json['count'] > 0)

    # check that we donwloaded all the events in a single page
    events_json = body_json['events']
    assert(body_json['count'] == len(events_json))

    events = []
    for event_json in events_json:
        id = event_json['id']

        is_main = False
        is_final = False
        weight = 1.0
        if 'scoring_options' in event_json:
            options_json = event_json['scoring_options']

            if 'weight' in options_json:
                weight = options_json['weight']
            if 'group' in options_json:
                is_final = options_json['group'] == "final"
                is_main = options_json['group'] == "main"

        event = Event(id, weight, is_main, is_final)
        events.append(event)
    return events
