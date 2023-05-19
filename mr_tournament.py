from classes import *
from mr_request import MrRequest
from common_data import CommonData


def get_tournament_info(data: CommonData, tournament_id: int):
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


def get_tournament_events(data: CommonData, tournament_id: int):
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

        is_final = False
        weight = 1.0
        if 'scoring_options' in event_json:
            options_json = event_json['scoring_options']

            if 'weight' in options_json:
                weight = options_json['weight']
            if 'group' in options_json:
                group_str = options_json['group']
                if group_str == "final":
                    is_final = True
                elif group_str == "main":
                    is_final = False
                else:
                    print(f"### Unknown event group: {group_str}")

            # workaround for some stages without GROUP
            if weight > 1.0:
                is_final = True

        event = Event(id, weight, is_final)
        events.append(event)
    return events


def get_tournament_places(data: CommonData, tournament_id: int):
    url = f"/tournament_places.php?tournament_id={tournament_id}"
    body_json = MrRequest(data.cache).execute(url)

    assert('count' in body_json)
    assert('places' in body_json)
    if body_json['count'] == 0 or not body_json['places']:
        # This tournament does not have places
        # bad tournament, not finished tournament
        return None

    assert(body_json['count'] > 0)
    places_json = body_json['places']
    assert(body_json['count'] == len(places_json))

    places = []
    for item in places_json:
        player_id = item['user_id']
        place_num = item['place']
        games_count = item['games_count']
        place = {'player_id': player_id,
                 'place': place_num,
                 'games_count': games_count}
        places.append(place)
    return places
