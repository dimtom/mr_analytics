from classes import *
from copy import copy

import common_data
import mr_tournament
import mr_tournaments
import mr_games

from request_cache import RequestCache

from analyze_league import analyze_league
import analyze_tournament


def load_tournaments(data, ids):
    tournaments = {}
    print("\n*** Loading info of all tournaments")
    for tournament_id in ids:
        t = mr_tournament.get_tournament_info(data, tournament_id)

        games = mr_games.load_tournament_games(
            data, tournament_id, event_id=None)
        t.games_json = games

        tournaments[tournament_id] = t

    return tournaments


def process_tournaments(data, tournaments):
    processed_tournaments = {}
    print("\n*** Processing tournaments")
    for id, tournament in tournaments.items():
        print(f"Tournament: {tournament.name}")
        t = analyze_tournament.process_tournament(data, id)
        if t:
            processed_tournaments[id] = t
        else:
            print(f"### Bad tournament, deleted: {id}")

    # put all players into common data
    # NB: we don't need scores, just
    for id, tournament in processed_tournaments.items():
        if not tournament.players:
            print(f"Tournament: {id} - no players ???")
            continue

        for player in tournament.players.values():
            if player.id not in data.players:
                p = Player(player.id, player.name)
                data.players[player.id] = p

    return processed_tournaments


def get_players(data, tournaments):
    player_tournaments = {}
    for id, t in tournaments.items():
        places = mr_tournament.get_tournament_places(data, id)

        # for debug only
        print(f"\nTournament table: {t.name}")
        for pos, p in enumerate(places):
            player_id = p['player_id']
            player = data.players[player_id] if player_id in data.players else None
            player_name = player.name if player else "Unknown"
            print(f"{(pos+1)}: {player_name:20s}")

        for p in places:
            player_id = p['player_id']
            if player_id not in player_tournaments:
                player_tournaments[player_id] = []
            player_tournaments[player_id].append(id)

    print(
        f"\n*** Players that played the most tournaments: {len(player_tournaments)}")
    sorted_players = sorted(
        player_tournaments, key=lambda id: len(player_tournaments[id]), reverse=True)
    for id in sorted_players:
        player = data.players[id] if id in data.players else None
        player_name = player.name if player else "Unknown"
        print(
            f"Player:{player_name:12s} Tournaments: {len(player_tournaments[id]):3d}")


def print_clubs(data):
    print("\n*** All clubs")
    for id, club in data.clubs.items():
        print(f"{id: 3d} {club.name}")


# Return valid good tournaments only from club_id
def filter_tournaments(tournaments, filter_club_id):
    invalid_tournaments = []
    no_club_tournaments = []
    good_tournaments = {}

    print(f"\n*** Filtered tournaments only in club: {filter_club_id}")
    for id, tournament in tournaments.items():
        if not tournament.games_json:
            invalid_tournaments.append(tournament)
            continue

        if not tournament.club:
            no_club_tournaments.append(tournament)
            continue

        if tournament.club.id == filter_club_id:
            good_tournaments[id] = tournament

    print(f"Invalid tournaments: {len(invalid_tournaments)}")
    '''for t in invalid_tournaments:
        print(f"{t.name}")
    '''

    print(f"Tournaments without a club: {len(no_club_tournaments)}")
    '''
    for t in no_club_tournaments:
        print(f"{t.name}")
    '''

    print(f"\n*** Filtered tournaments: {len(good_tournaments)}")
    for id, t in good_tournaments.items():
        print(f"{t.id:3d} Games: {len(t.games_json)} {t.name}")
    return good_tournaments


def main():
    cache = RequestCache()
    cache.load()

    data = common_data.CommonData(cache)
    data.load()

    seasons = analyze_league(data)
    # TODO: use tournaments for processing

    # Print all tournaments (by all seasons)
    # print(tournaments)

    # chose a single season - print tournaments
    '''
    year = 2022
    print(f"*** Tournaments in season {year}:")
    print(seasons[year])
    '''

    gatsby_id = 59

    '''
    ### Strange but we miss tournament id=70 (or 71)
    # use all tournaments
    all_ids = []
    for year, ids in seasons.items():
        all_ids.extend(ids)

    tournaments = load_tournaments(data, all_ids)
    print(f"Number of all tournaments: {len(tournaments)}")

    
    gatsby_tournaments = filter_tournaments(tournaments, gatsby_id)
    '''

    # That's why we use tournaments by CLUB ID
    # is not found in the year 2022
    gatsby_ids = mr_tournaments.load_tournaments_by_club(data, gatsby_id)
    print(f"Number of all tournaments: {len(gatsby_ids)}")

    gatsby_tournaments = load_tournaments(data, gatsby_ids)
    gatsby_tournaments = filter_tournaments(gatsby_tournaments, gatsby_id)

    # analyze all tournaments - we need to get player names!
    processed_tournaments = process_tournaments(data, gatsby_tournaments)

    # get all players
    get_players(data, gatsby_tournaments)

    # TODO:
    # gatsby_games = get_all games(gatsby_tournaments)

    # analyze single tournament

    # tournament_id = 115  # Friends cup 2023
    # tournament_id = 116  # Golgen Gate 2023
    # analyze_tournament(data, tournament_id)

    cache.save()
    pass


if __name__ == '__main__':
    main()
