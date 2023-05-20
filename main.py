from classes import *


import common_data
import mr_tournament
import mr_tournaments
import mr_games

from request_cache import RequestCache

from analyze_league import analyze_league
import analyze_tournament

from report import *


def get_tournaments_all(data, seasons):
    all_ids = []
    for year, ids in seasons.items():
        all_ids.extend(ids)
    return all_ids


def get_tournaments_2022(data, seasons):
    return seasons[2022]


def analyze_single_tournament(data, tournament_id):
    # tournament_id = 115  # Friends cup 2023
    # tournament_id = 116  # Golgen Gate 2023
    # analyze_tournament(data, tournament_id)
    pass


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
        t = analyze_tournament.process_tournament(data, id)
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
    seasons = analyze_league(data)
    all_ids = get_tournaments_all(data, seasons)

    tournaments = load_tournaments(data, all_ids)
    tournaments = filter_tournaments(tournaments)

    eva_id = 1088
    shnurok_id = 1862
    tournaments_by_player(data, tournaments, eva_id)
    tournaments_by_player(data, tournaments, shnurok_id)


def print_clubs(data):
    print("\n*** All clubs")
    for id, club in data.clubs.items():
        print(f"{id: 3d} {club.name}")


def main():
    cache = RequestCache()
    cache.load()

    data = common_data.CommonData(cache)
    data.load()

    # REPORT LARGEST TOURNAMENTS
    # command_largest_tournaments(data)
    # return

    # REPORT TOURNAMENTS of Siberian
    # command_tournaments_of_siberian(data)
    # return

    # REPORT ALINA and SHNUROK
    commands_alina_and_shnurok(data)
    return

    seasons = analyze_league(data)

    # specify IDS of tournaments we want to process
    all_ids = get_tournaments_all(data, seasons)
    # all_ids = get_tournaments_2022(data, seasons)

    tournaments = load_tournaments(data, all_ids)
    tournaments = filter_tournaments(tournaments)

    # analyze all tournaments - we need to get player names!
    processed_tournaments = process_tournaments(data, tournaments)
    get_players_from_tournaments(data, processed_tournaments)

    # get all players
    # report_tournament_places(data, processed_tournaments)
    # report_top_players(data, processed_tournaments)
    # report_player_games(data, processed_tournaments)

    report_moderators(data, processed_tournaments)
    report_games_result(data, processed_tournaments)

    report_player_win_role(data, processed_tournaments)

    report_largest_tournaments(data, tournaments)
    cache.save()
    pass


if __name__ == '__main__':
    main()
