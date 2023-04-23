from common_data import CommonData
from mr_request import MrRequest
from request_cache import RequestCache

import mr_games
import json


def analyze_goldengate_2023(data: CommonData):
    tournament_id = 116

    tournament = mr_games.get_tournament_info(data, tournament_id)
    print(
        f"Tournament: {tournament.name} Club: {tournament.club} City: {tournament.city}")

    games_json = mr_games.load_tournament_games(data, tournament_id)
    tournament_games, tournament_players = mr_games.process_tournament_games(
        data, tournament, games_json)
    tournament.games = tournament_games
    tournament.players = tournament_players

    print("Games of tournament:")
    print(f"*** Total number of games: {len(tournament_games)}")
    for game in tournament_games:
        print(f"\n* Game {game.id}. Result: {game.result}")
        for slot in game.slots:
            blank_str = "      "
            main_score_str = f"{slot.main_score: 4.2f}" if slot.main_score != 0.0 else blank_str
            legacy_score_str = f"{slot.legacy_score: 4.2f}" if slot.legacy_score != 0.0 else blank_str
            bonus_score_str = f"{slot.bonus_score: 4.2f}" if slot.bonus_score != 0.0 else blank_str
            penalty_score_str = f"{slot.penalty_score:4.2f}" if slot.penalty_score != 0.0 else blank_str
            total_score_str = f"{slot.total_score: 4.2f}" if slot.total_score != 0.0 else blank_str

            print(
                f"{slot.player_name:20s} : {slot.role}\t {main_score_str} {legacy_score_str} {bonus_score_str} {penalty_score_str} {total_score_str} ")

    # calculate scores for every player
    mr_games.calc_tournament_scores(data, tournament)

    print(f"\n***Total number of players: {len(tournament_players)}")
    sorted_players = sorted(tournament.players.values(),
                            key=lambda player: player.total_score, reverse=True)

    print("Players of tournament:")
    for player in sorted_players:
        print(f"{player.name:20s} {player.total_score:4.2f} {player.main_score:4.2f} {player.legacy_score:4.2f} {player.bonus_score:4.2f} {player.penalty_score:4.2f} ")

    with open('gg_players.txt', 'w') as f:
        d = [{'id': player.id, 'name': player.name}
             for player in tournament_players.values()]
        f.write(json.dumps(d))

    # with open('gg_games.txt', 'w') as f:
    #     f.write(json.dumps(games))

    return tournament
