from classes import *


import common_data
import mr_tournament
import mr_tournaments
import mr_games

from request_cache import RequestCache

from analyze_league import analyze_league
from analyze_tournament import *

from report import *


def get_tournaments_all(data, seasons):
    all_ids = []
    for year, ids in seasons.items():
        all_ids.extend(ids)
    return all_ids


def get_tournaments_2022(data, seasons):
    return seasons[2022]


def load_tournaments(data, ids):
    tournaments = {}
    print("\n*** Loading info of all tournaments")
    for tournament_id in ids:
        t = mr_tournament.get_tournament_info(data, tournament_id)
        tournaments[tournament_id] = t

        # load places to make sure tournament is good
        places = mr_tournament.get_tournament_places(data, tournament_id)
        t.places = places

    print(f"Loaded tournaments: {len(tournaments)}")
    return tournaments


def filter_tournaments(tournaments):
    print(f"\n*** Filter tournaments. Before: {len(tournaments)}")

    no_club_tournaments = []
    no_places_tournaments = []

    good_tournaments = {}
    for id, tournament in tournaments.items():
        if not tournament.club:
            no_club_tournaments.append(tournament)
            continue

        if not tournament.places:
            no_places_tournaments.append(tournament)
            continue

        good_tournaments[id] = tournament

    print(f"Tournaments without a club: {len(no_club_tournaments)}")
    for t in no_club_tournaments:
        print(f"{t.name}")

    print(f"Tournament without places: {len(no_places_tournaments)}")
    for t in no_places_tournaments:
        print(f"{t.name}")

    print(f"\n*** Filtered tournaments: {len(good_tournaments)}")
    for id, t in good_tournaments.items():
        print(f"{t.id:3d} {t.name}")
    return good_tournaments


def process_tournaments(data, tournaments):
    print("\n*** Processing tournaments")

    processed_tournaments = {}
    for id, tournament in tournaments.items():
        t = process_tournament(data, id)
        if t:
            processed_tournaments[id] = t
        else:
            print(f"### Bad tournament, deleted: {id}")
    return processed_tournaments


def get_players_from_tournaments(data, tournaments):
    print(f"\n*** Populate player names from tournaments...")
    # put all players into common data
    # NB: we don't need scores, just
    for id, tournament in tournaments.items():
        if not tournament.players:
            print(f"Tournament: {id} - no players ???")
            continue

        for player in tournament.players.values():
            if player.id not in data.players:
                p = Player(player.id, player.name)
                data.players[player.id] = p


def command_largest_tournaments(data):
    seasons = analyze_league(data)
    all_ids = get_tournaments_all(data, seasons)

    tournaments = load_tournaments(data, all_ids)
    tournaments = filter_tournaments(tournaments)

    report_largest_tournaments(data, tournaments)


def command_tournaments_of_siberian(data):
    seasons = analyze_league(data)
    all_ids = get_tournaments_all(data, seasons)

    tournaments = load_tournaments(data, all_ids)
    tournaments = filter_tournaments(tournaments)
    processed_tournaments = process_tournaments(data, tournaments)

    siberian_id = 838
    report_tournament_by_moderator(data, processed_tournaments, siberian_id)


def commands_alina_and_shnurok(data):
    process_tournament(data, )

    tournaments = load_tournament(tournament_id)
    tournaments = filter_tournaments(tournaments)

    eva_id = 1088
    shnurok_id = 1862
    tournaments_by_player(data, tournaments, eva_id)
    tournaments_by_player(data, tournaments, shnurok_id)


def get_tournament_players(data, tournament_id):
    t = process_tournament(data, tournament_id)

    print(f"\n*** Tournament: {t.name}")
    print(f"*** Players: ")
    for id, player in t.players.items():
        print(f"{id} {player.name}")


def big_apple_players(data):
    players = [2287, 963, 2781, 2295, 2633,
               2250, 1158, 2054, 2084, 2861, 2215,
               3142, 2187, 3144, 1269, 2188, 2177,
               2461, 1862, 2746, 2202, 1088, 2045,
               2616, 2610, 2124, 2195, 2213, 2206,
               2239, 2271, 2617, 2750, 2613, 2118,
               2976,  2197]
    players = sorted(players)

    print(f"\*** Players ({len(players)} items):")
    for id in players:
        player_name = data.players[id].name if id in data.players else "Unknown"
        print(f"{id} {player_name}")

    return players


def get_all_games(data, tournaments):
    all_games = []
    for id, t in tournaments.items():
        all_games.extend(t.games)

    # debug - print all games
    '''
    print(f"\n*** Games: ({len(games)} items)")
    for pos, game in enumerate(games):
        print(f"#{(pos+1)} id:{game.id:4d}")
    '''

    return all_games


def game_player_slot(game: Game, player_id: int):
    for slot in game.slots:
        if slot.player_id == player_id:
            return slot

    return None


def prepare_2d_matrix(size):
    matrix = [[]] * size
    for i, item in enumerate(matrix):
        matrix[i] = [0] * size
    return matrix


def print_all_matrix(data, players, matrix):
    for idx, id in enumerate(players):

        line = matrix[idx]
        id_line = [{'id': players[i], 'games': value}
                   for i, value in enumerate(line)]
        sorted_id_line = sorted(
            id_line, key=lambda x: x['games'], reverse=True)

        print(f"#{(idx+1):2d} {data.players[id].name}")
        top5 = 3
        for i, item in enumerate(sorted_id_line[:top5]):
            item_id = item['id']
            item_games = item['games']
            player_name = data.players[item_id]

            if item_games > 0 and (i == 0 or item_games > 40):
                print(f"{item_games:3d}: {data.players[item_id].name}")


def print_percent_matrix(data, players, win_matrix, all_matrix):
    for idx, id in enumerate(players):

        win_line = win_matrix[idx]
        all_line = all_matrix[idx]

        id_line = [{'id': players[i], 'wins': value_wins, 'games': value_games}
                   for i, (value_wins, value_games) in enumerate(zip(win_line, all_line))]
        sorted_id_line = sorted(
            id_line, key=lambda x: x['wins'] / x['games'] if x['games'] > 0 else 0.0, reverse=True)

        print(f"#{(idx+1):2d} {data.players[id].name}")

        # for debug only!
        # print(win_line)
        # print(all_line)
        # print(id_line)
        # print(sorted_id_line[:5])

        top5 = 5
        count = 0
        for i, item in enumerate(sorted_id_line):
            item_id = item['id']
            item_wins = item['wins']
            item_games = item['games']
            player_name = data.players[item_id]

            rate = (100. * item_wins / item_games) if item_games > 0 else 0.0
            if item_games > 3:
                print(
                    f"Rate: {rate:6.2f}%. Wins: {item_wins:3d} of {item_games:3d}: {player_name}")
                count += 1
                if count >= top5:
                    break


def command_find_pairs(data):
    seasons = analyze_league(data)
    all_ids = get_tournaments_2022(data, seasons)

    tournaments = load_tournaments(data, all_ids)
    tournaments = filter_tournaments(tournaments)

    # analyze all tournaments - we need to get player names!
    processed_tournaments = process_tournaments(data, tournaments)

    games = get_all_games(data, processed_tournaments)

    # get playres with their names from BigApple tournament
    big_apple_2023_id = 136
    big_apple = load_tournaments(data, [big_apple_2023_id])
    big_apple = process_tournaments(data, big_apple)
    get_players_from_tournaments(data, big_apple)
    players = big_apple_players(data)

    pairs_all_games = prepare_2d_matrix(len(players))
    pairs_red_wins = prepare_2d_matrix(len(players))
    pairs_red_games = prepare_2d_matrix(len(players))
    pairs_black_wins = prepare_2d_matrix(len(players))
    pairs_black_games = prepare_2d_matrix(len(players))

    for idx_a, id_a in enumerate(players):
        for idx_b, id_b in enumerate(players):
            if id_a >= id_b:
                continue

            for game in games:
                slot_a = game_player_slot(game, id_a)
                slot_b = game_player_slot(game, id_b)
                if slot_a and slot_b:
                    pairs_all_games[idx_a][idx_b] += 1
                    pairs_all_games[idx_b][idx_a] += 1

                    red_a = slot_a.role_red()
                    red_b = slot_b.role_red()
                    if red_a and red_b:
                        pairs_red_games[idx_a][idx_b] += 1
                        pairs_red_games[idx_b][idx_a] += 1
                        if game.result == "red":
                            pairs_red_wins[idx_a][idx_b] += 1
                            pairs_red_wins[idx_b][idx_a] += 1

                    if (not red_a) and (not red_b):
                        pairs_black_games[idx_a][idx_b] += 1
                        pairs_black_games[idx_b][idx_a] += 1
                        if game.result == "black":
                            pairs_black_wins[idx_a][idx_b] += 1
                            pairs_black_wins[idx_b][idx_a] += 1

    # print("\n*** Player pair - ALL games count")
    # print_all_matrix(data, players, pairs_all_games)

    # print("\n*** Player pair - RED WINS")
    # print_percent_matrix(data, players, pairs_red_wins, pairs_red_games)

    print("\n*** Player pair - BLACK WINS")
    print_percent_matrix(data, players, pairs_black_wins, pairs_black_games)


def command_reports(data):
    seasons = analyze_league(data)
    all_ids = get_tournaments_2022(data, seasons)

    tournaments = load_tournaments(data, all_ids)
    tournaments = filter_tournaments(tournaments)

    # analyze all tournaments - we need to get player names!
    processed_tournaments = process_tournaments(data, tournaments)

    # get all players
    # report_tournament_places(data, processed_tournaments)
    # report_top_players(data, processed_tournaments)
    # report_player_games(data, processed_tournaments)

    report_moderators(data, processed_tournaments)
    report_games_result(data, processed_tournaments)

    report_player_win_role(data, processed_tournaments)

    report_largest_tournaments(data, tournaments)


def print_clubs(data):
    print("\n*** All clubs")
    for id, club in data.clubs.items():
        print(f"{id: 3d} {club.name}")


def in_main(data):
    command_find_pairs(data)

    # tournament_id = 115  # Friends cup 2023
    # tournament_id = 116  # Golgen Gate 2023
    # big_apple_2023_id = 136  # BigApple Cup 2023
    # get_tournament_players(data, big_apple_2023_id)
    # return

    # REPORT LARGEST TOURNAMENTS
    # command_largest_tournaments(data)
    # return

    # REPORT TOURNAMENTS of Siberian
    # command_tournaments_of_siberian(data)
    # return

    # REPORT ALINA and SHNUROK
    # commands_alina_and_shnurok(data)
    # return

    # command_reports(data)

    pass


def main():
    cache = RequestCache()
    cache.load()

    data = common_data.CommonData(cache)
    data.load()

    in_main(data)

    cache.save()


if __name__ == '__main__':
    main()
