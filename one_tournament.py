from common_data import CommonData
from mr_request import MrRequest
from request_cache import RequestCache

import mr_tournament
import mr_games
import output
import json


def analyze_goldengate_2023(data: CommonData):
    tournament_id = 116

    tournament = mr_tournament.get_tournament_info(data, tournament_id)
    print(
        f"Tournament: {tournament.name} Club: {tournament.club} City: {tournament.city}")

    events = mr_tournament.get_tournament_events(data, tournament_id)
    tournament.events = events
    if len(events) == 0:
        print(f"### No events found!")
    elif len(events) == 1:
        event = events[0]
        print(f"Single event. Final: {event.is_final} Weight: {event.weight}")
    elif len(events) == 2:
        print(f"Tournament with final")
        one = events[0]
        two = events[1]
        print(f"Event1. Final: {one.is_final} Weight: {one.weight}")
        print(f"Event2. Final: {two.is_final} Weight: {two.weight}")
    else:
        print(f"Found events: {len(events)}")

    # TODO: remove workaround
    # we assume that main stage is event[1]
    # usually event[0] is a final
    final_event = events[0]
    assert(final_event.is_final == True)
    main_event = events[1]
    assert(main_event.is_final == False)

    games_json = mr_games.load_tournament_games(
        data, tournament_id, main_event.id)
    tournament_games, tournament_players = mr_games.process_tournament_games(
        data, tournament, games_json)
    tournament.games = tournament_games
    tournament.players = tournament_players

    # calculate scores for every player
    mr_games.calc_tournament_scores(data, tournament)

    output.output_games(tournament_games, tournament_players)

    output.output_players(tournament_players)

    '''
    with open('gg_players.txt', 'w') as f:
        d = [{'id': player.id, 'name': player.name}
             for player in tournament_players.values()]
        f.write(json.dumps(d))
    '''

    return tournament
