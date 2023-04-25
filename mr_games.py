
from classes import *
from common_data import CommonData
from mr_request import MrRequest


def load_tournament_games(data: CommonData, tournament_id: int, event_id: int):
    # Return all the games
    page_size = 1000  # big number to fit ALL the games of current tournament
    url = f"/games.php?&tournament_id={tournament_id}&event_id={event_id}&page_size={page_size}"
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
            # Sometimes game does not have player id
            # This is not a valid game,
            # moderator missed a player...
            if 'id' not in item:
                print(f"### Game: {game_id} slot: {pos+1} - no player_id!")
                player_id = 0
                player_name = "###"
            else:
                player_id = item['id']
                player_name = item['name']

            # TODO: move value 0.3 into Slot or score calculation
            # Just add bool flag "worst move" to the slot
            # sothat all magic numbers are in one place
            slot_auto = 0.3
            slot_bonus = 0.0
            if 'bonus' in item:
                if item['bonus'] == "worstMove":
                    slot_auto = 0.0
                else:
                    slot_bonus = float(item['bonus'])
            slot_role = item['role'] if 'role' in item else "civ"

            first_killed = False
            if 'death' in item:
                death = item['death']
                round = death['round'] if 'round' in death else -1
                death_type = death['type'] if 'type' in death else None
                if round == 1 and death_type == 'night':
                    first_killed = True

            legacy = None
            if 'legacy' in item:
                legacy = item['legacy']

            eliminated = None
            if 'death' in item:
                death_type = item['death']['type']
                if death_type != "night" and death_type != "day":
                    eliminated = death_type

            slot = Slot(game, pos+1, int(player_id), player_name)
            slot.role = slot_role
            slot.auto_score = slot_auto
            slot.bonus_score = slot_bonus
            slot.legacy = legacy
            slot.eliminated = eliminated
            slot.first_killed = first_killed
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

    return games, tournament_players


def calc_tournament_scores(data: CommonData, tournament: Tournament):
    pass


def calc_stage_scores(data: CommonData, tournament: Tournament, event: Event):
    # TODO
    pass


'''def process_game(data: CommonData, game: Game, game_json: str):

    for p in game_json['players']:
        if 'id' not in p or 'name' not in p:
            print(f"### Tournament: {game.tournament} Game: {game.id}")
            continue
        p_id = p['id']
        p_name = p['name']
'''
