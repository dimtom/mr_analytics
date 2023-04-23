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
    tournament.tournament_players = tournament_players

    print("Players of tournament:")
    for id, player in tournament_players.items():
        print(f"{player.toJson()}")
    print(f"Total number of players: {len(tournament_players)}")

    print("Games of tournament:")
    for game in tournament_games:
        print(f"{game.id} {[player.name for player in game.players]}")
    print(f"Total number of games: {len(tournament_games)}")

    with open('gg_players.txt', 'w') as f:
        d = [{'id': player.id, 'name': player.name}
             for player in tournament_players.values()]
        f.write(json.dumps(d))

    # with open('gg_games.txt', 'w') as f:
    #     f.write(json.dumps(games))

    return tournament
