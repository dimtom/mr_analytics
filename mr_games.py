
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
    club = data.clubs[club_id] if club_id in data.clubs else None
    city = club.city if club else None

    return Tournament(id=tournament_id, name=tournament_name, club=club, city=city)


def load_tournament_games(data: CommonData, tournament_id: int):
    tournament = get_tournament_info(data, tournament_id)
    print(
        f"*** Tournament #{tournament.id}: {tournament.name} ({tournament.club}, {tournament.city})")

    # Return all the games
    page_size = 1000  # big number to fit ALL the games of current tournament
    url = f"/games.php?&tournament_id={tournament_id}&page_size={page_size}"
    body_json = MrRequest(data.cache).execute(url)

    num_games = body_json['count']
    print(f"Found games: {num_games}")
    print(f"Games in the list: {len(body_json['games'])}")

    # ensure that we downloaded all the games in the first single page
    assert(num_games == len(body_json['games']))
    return body_json['games']


def process_tournament_games(data: CommonData, tournament: Tournament, games_json: dict):
    games = list[Game]()
    tournament_players = dict[int, Player]()
    sorted_games = sorted(games_json,
                          key=lambda item: item['endTime'])

    for game_json in sorted_games:
        game_players = []

        game_id = game_json['id']
        winner = game_json['winner']
        moderator_id = game_json['moderator']['id']
        players_json = game_json['players']

        game_is_rating = game_json['rating'] if 'rating' in game_json else True
        if not game_is_rating:
            print(f"Skipping non-rating game: {game_id}")
            continue

        for item in players_json:
            player_id = item['id']
            player_name = item['name']
            slot = Player(int(player_id), player_name)
            game_players.append(slot)

        # update tournament players from this game players
        for slot in game_players:
            if slot.id not in tournament_players:
                tournament_players[slot.id] = Player(slot.id, slot.name)
            tournament_players[slot.id].add_name(slot.name)

        game = Game(game_id, tournament)
        game.winner = winner

        # here we need to find players in Tournament (to keep allnames)
        game.players = [tournament_players[player.id]
                        for player in game_players]
        game.game_json = game_json
        games.append(game)

    return games, tournament_players


'''def process_game(data: CommonData, game: Game, game_json: str):

    for p in game_json['players']:
        if 'id' not in p or 'name' not in p:
            print(f"### Tournament: {game.tournament} Game: {game.id}")
            continue
        p_id = p['id']
        p_name = p['name']
'''
