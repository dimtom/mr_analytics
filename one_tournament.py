from common_data import CommonData
from mr_request import MrRequest
from request_cache import RequestCache

import mr_tournament
import mr_games
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

    print("Games of tournament:")
    print(f"*** Total number of games: {len(tournament_games)}")
    for game in tournament_games:
        print(f"\n* Game {game.id}. Result: {game.result}")
        for slot in game.slots:
            blank_str = "    "

            total_score_str = f"{slot.total_score: 4.2f}"
            main_score_str = f"{int(slot.main_score): 1d}" if slot.main_score != 0.0 else "  "
            legacy_score_str = f"{slot.legacy_score: 4.2f}" if slot.legacy_score != 0.0 else blank_str
            auto_score_str = "  " if slot.auto_score == 0.3 else "--"
            bonus_score_str = f"{slot.bonus_score: 4.2f}" if slot.bonus_score != 0.0 else blank_str
            penalty_score_str = f"{slot.penalty_score:4.2f}" if slot.penalty_score != 0.0 else blank_str

            print(
                f"({slot.short_role()}) {slot.player_name[:10]:10s}: {total_score_str} {main_score_str} {legacy_score_str} {auto_score_str} {bonus_score_str} {penalty_score_str}")

    print(f"\n***Total number of players: {len(tournament_players)}")
    sorted_players = sorted(tournament.players.values(),
                            key=lambda player: player.total_score, reverse=True)

    print("Players of tournament:")
    for player in sorted_players:
        total_score_str = f"{player.total_score: 4.2f}"
        main_score_str = f"{int(player.main_score): 2d}"
        print(f"{player.name:20s} {total_score_str} {main_score_str} {player.legacy_score:4.2f} {player.bonus_score:4.2f} {player.penalty_score:4.2f} ")

    '''
    with open('gg_players.txt', 'w') as f:
        d = [{'id': player.id, 'name': player.name}
             for player in tournament_players.values()]
        f.write(json.dumps(d))
    '''

    return tournament
