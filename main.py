from classes import *
from copy import copy

import common_data
import mr_tournament
import mr_tournaments
import mr_games

from request_cache import RequestCache

from analyze_league import analyze_league
import analyze_tournament


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


def report_tournament_places(data, tournaments):
    for id, t in tournaments.items():
        places = mr_tournament.get_tournament_places(data, id)

        # for debug only
        print(f"\nTournament table: {t.id} {t.name}")
        for pos, p in enumerate(places):
            player_id = p['player_id']
            player = data.players[player_id] if player_id in data.players else None
            player_name = player.name if player else "Unknown"
            print(f"{(pos+1)}: {player_name:20s}")


def report_top_players(data, tournaments):
    player_tournaments = {}
    for id, t in tournaments.items():
        places = mr_tournament.get_tournament_places(data, id)

        for p in places:
            player_id = p['player_id']
            if player_id not in player_tournaments:
                player_tournaments[player_id] = []
            player_tournaments[player_id].append(id)

    print(
        f"\n*** Players that played the most tournaments: {len(player_tournaments)}")
    sorted_players = sorted(
        player_tournaments, key=lambda id: len(player_tournaments[id]), reverse=True)
    for pos, id in enumerate(sorted_players):
        player = data.players[id] if id in data.players else None
        player_name = player.name if player else "Unknown"
        print(
            f"{(pos+1):3d} {player_name:16s} {len(player_tournaments[id]):3d}")


def report_player_games(data, tournaments):
    player_games = {}
    game_count = 0
    for id, t in tournaments.items():
        games = t.games

        for game in games:
            game_count += 1
            slots = game.slots
            for slot in slots:
                player_id = slot.player_id
                if player_id not in player_games:
                    player_games[player_id] = 0
                player_games[player_id] += 1

    print("\n*** Report - player and games count")
    print(f"Total number of tournaments: {len(tournaments)}")
    print(f"Total number of games: {game_count}")

    print(
        f"\n*** Players that played the most number of games: {len(player_games)}")
    sorted_players = sorted(
        player_games, key=lambda id: player_games[id], reverse=True)
    for pos, id in enumerate(sorted_players):
        player = data.players[id] if id in data.players else None
        player_name = player.name if player else "Unknown"
        print(
            f"{(pos+1):3d} {player_name:16s} {player_games[id]:3d}")


def report_moderators(data, tournaments):
    moderator_games = {}
    game_count = 0
    for id, t in tournaments.items():
        for game in t.games:
            game_count += 1
            moderator_id = int(game.moderator_id)
            if moderator_id not in moderator_games:
                moderator_games[moderator_id] = 0
            moderator_games[moderator_id] += 1

    print("\n*** Report - modetarots and games count")
    print(f"Total number of tournaments: {len(tournaments)}")
    print(f"Total number of games: {game_count}")

    print(
        f"\n*** Moderators that played the most number of games: {len(moderator_games)}")
    sorted_moderators = sorted(
        moderator_games.keys(), key=lambda id: moderator_games[id], reverse=True)
    for pos, id in enumerate(sorted_moderators):
        moderator = data.players[id] if id in data.players else None
        moderator_name = moderator.name if moderator else "Unknown"
        print(
            f"{(pos+1):2d} {id:4d} {moderator_name:16s} {moderator_games[id]:3d}")


def print_clubs(data):
    print("\n*** All clubs")
    for id, club in data.clubs.items():
        print(f"{id: 3d} {club.name}")


def main():
    cache = RequestCache()
    cache.load()

    data = common_data.CommonData(cache)
    data.load()

    seasons = analyze_league(data)

    # specify IDS of tournaments we want to process
    # all_ids = get_tournaments_all(seasons)
    all_ids = get_tournaments_2022(data, seasons)

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

    cache.save()
    pass


if __name__ == '__main__':
    main()
