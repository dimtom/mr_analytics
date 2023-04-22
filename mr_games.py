
from classes import *
from common_data import CommonData
from mr_request import MrRequest


def get_tournament_info(data, tournament_id: int):
    url = f"/tournaments.php?&tournament_id={tournament_id}"
    body_json = MrRequest(data.cache).execute(url)

    # there MUST be one and only ONE tournament
    assert(body_json['count'] == 1)
    tournament_json = body_json['tournaments'][0]

    tournament_name = tournament_json['name']
    club_id = tournament_json['club_id']
    club_name = data.club_name(club_id)
    club_city = data.club_city(club_id)

    # TODO: Return Tournament object!
    return {'id': tournament_id, 'name': tournament_name, 'club': club_name, 'city': club_city}


def load_tournament_games(data: CommonData, tournament_id: int):
    tournament_info = get_tournament_info(data, tournament_id)
    print(
        f"*** Tournament #{tournament_id}: {tournament_info['name']} ({tournament_info['club']}, {tournament_info['city']})")

    # Return all the games
    url = f"/games.php?&tournament_id={tournament_id}"
    body_json = MrRequest(data.cache).execute(url)

    num_games = body_json['count']
    print(f"Found games: {num_games}")

    sorted_games = sorted(body_json['games'], key=lambda item: item['endTime'])
    players_of_single_tournament = set()
    for game in sorted_games:
        game_id = game['id']
        winner = game['winner']
        moderator_id = game['moderator']['id']
        players = game['players']
        player_names = [item['name'] for item in players]
        # print(f"{game_id}: {winner} moderator: {moderator_id}")
        # print(f"Players: {player_names}")

        for p in players:
            if 'id' not in p or 'name' not in p:
                print(f"### Tournament: {tournament_id} Game: {game_id}")
                continue

            p_id = p['id']
            p_name = p['name']
            players_of_single_tournament.add(p_id)
            if p_id not in data.players:
                data.players[p_id] = Player(p_id)
                data.players[p_id].name = p_name
            else:
                data.players[p_id].games += 1
                data.players[p_id].name = p_name

    for p_id in players_of_single_tournament:
        data.players[p_id].tournaments += 1
