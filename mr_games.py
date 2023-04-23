
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
        # do not include non-rating games!
        game_is_rating = game_json['rating'] if 'rating' in game_json else True
        if not game_is_rating:
            print(f"Skipping non-rating game: {game_id}")
            continue

        game_id = game_json['id']
        moderator_id = game_json['moderator']['id']
        game_result = game_json['winner']
        players_json = game_json['players']

        game = Game(tournament, game_id, moderator_id, game_result)

        game_slots = []
        for pos, item in enumerate(players_json):
            player_id = item['id']
            player_name = item['name']

            slot_bonus = 0.0
            if 'bonus' in item:
                if item['bonus'] == "worstMove":
                    slot_bonus = -0.3
                else:
                    slot_bonus = float(item['bonus'])
            slot_role = item['role'] if 'role' in item else "civ"

            legacy = None
            if 'legacy' in item:
                legacy = item['legacy']

            eliminated = None
            if 'death' in item:
                death_type = item['death']['type']
                if death_type == "kickOut" or death_type == "teamKickOut":
                    eliminated = death_type

            slot = Slot(game, pos+1, int(player_id), player_name)
            slot.role = slot_role
            slot.bonus_score = slot_bonus
            slot.legacy = legacy
            slot.eliminated = eliminated
            game_slots.append(slot)

        # update tournament players from this game players
        for slot in game_slots:
            id = slot.player_id
            name = slot.player_name
            if id not in tournament_players:
                tournament_players[id] = Player(id, name)
            tournament_players[id].add_name(name)

        # here we need to find players in Tournament (to keep allnames)
        game.slots = game_slots
        game.game_json = game_json
        games.append(game)

        # calc scores after all slots are added (required for legacy)
        for slot in game.slots:
            slot.calcMainScore()
            slot.calcLegacyScore()
            slot.calcPenaltyScore()
            slot.calcTotalScore()

    return games, tournament_players


def calc_tournament_scores(data: CommonData, tournament: Tournament):

    for player in tournament.players.values():
        player.main_score = 0.0
        player.bonus_score = 0.0
        player.legacy_score = 0.0
        player.penalty_score = 0.0
        player.total_score = 0.0

    for game in tournament.games:
        for slot in game.slots:
            player = tournament.players[slot.player_id]
            player.main_score += slot.main_score
            player.bonus_score += slot.bonus_score
            player.legacy_score += slot.legacy_score
            player.penalty_score += slot.penalty_score
            player.total_score += slot.total_score


'''def process_game(data: CommonData, game: Game, game_json: str):

    for p in game_json['players']:
        if 'id' not in p or 'name' not in p:
            print(f"### Tournament: {game.tournament} Game: {game.id}")
            continue
        p_id = p['id']
        p_name = p['name']
'''
