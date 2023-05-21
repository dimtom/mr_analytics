from classes import *
from copy import copy
from common_data import CommonData

import mr_tournament
import mr_tournaments
import mr_games

from request_cache import RequestCache

from analyze_league import analyze_league


def report_tournament_places(data: CommonData, tournaments):
    for id, t in tournaments.items():
        places = mr_tournament.get_tournament_places(data, id)

        # for debug only
        print(f"\nTournament table: {t.id} {t.name}")
        for pos, p in enumerate(places):
            player_id = p['player_id']
            player = data.players[player_id] if player_id in data.players else None
            player_name = player.name if player else "Unknown"
            print(f"{(pos+1)}: {player_name:20s}")


def report_top_players(data: CommonData, tournaments: dict[int, Tournament]):
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


def report_player_games(data: CommonData, tournaments: dict[int, Tournament]):
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


def report_moderators(data: CommonData, tournaments: dict[int, Tournament]):
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


def report_games_result(data: CommonData, tournaments: dict[int, Tournament]):
    game_results = {}
    game_count = 0
    for id, t in tournaments.items():
        for game in t.games:
            game_count += 1
            if game.result not in game_results:
                game_results[game.result] = 0
            game_results[game.result] += 1

    print("\n*** Report - game results")
    print(f"Total number of games: {game_count}")

    for res in game_results:
        count = game_results[res]
        percentage = count / game_count
        print(
            f"{res:8s} {count:3d} {100.0 * percentage:.2f}%")


def report_player_win_role(data: CommonData, tournaments: dict[int, Tournament]):
    player_win_sheriff = defaultdict(int)
    player_games_sheriff = defaultdict(int)

    player_win_don = defaultdict(int)
    player_games_don = defaultdict(int)

    game_count = 0
    for id, t in tournaments.items():
        for game in t.games:
            game_count += 1
            for slot in game.slots:
                if slot.role == "sheriff":
                    player_id = slot.player_id
                    player_games_sheriff[player_id] += 1
                    if game.result == "red":
                        player_win_sheriff[player_id] += 1
                elif slot.role == "don":
                    player_id = slot.player_id
                    player_games_don[player_id] += 1
                    if game.result == "black":
                        player_win_don[player_id] += 1

    print("\n*** Sheriff")
    sorted_sheriff = sorted(player_games_sheriff,
                            key=lambda id: player_win_sheriff[id], reverse=True)
    for id in sorted_sheriff:
        player = data.players[id] if id in data.players else None
        player_name = player.name if player else "Unknown"
        win = player_win_sheriff[id]
        total = player_games_sheriff[id]

        # drop small results
        if total <= 3 or win <= 1:
            continue
        rate = win/total
        print(f"{player_name:16s} {(100.0 * rate):8.2f}% {win:2d} / {total:2d}")

    print("\n*** Don")
    sorted_don = sorted(player_games_don,
                        key=lambda id: player_win_don[id], reverse=True)
    for id in sorted_don:
        player = data.players[id] if id in data.players else None
        player_name = player.name if player else "Unknown"
        win = player_win_don[id]
        total = player_games_don[id]

        # drop small results
        if total <= 3 or win <= 1:
            continue

        rate = win/total
        print(f"{player_name:16s} {(100.0 * rate):8.2f}% {win:2d} / {total:2d}")


def report_largest_tournaments(data: CommonData, tournaments: dict[int, Tournament]):
    sorted_tournaments = sorted(tournaments, key=lambda id: len(
        tournaments[id].places), reverse=True)

    top_10 = 10
    print(f"\n*** Top {top_10} largest tournaments")
    for pos, id in enumerate(sorted_tournaments[:top_10]):
        t = tournaments[id]
        num_players = len(t.places)
        print(f"#{(pos+1):2d} Players: {num_players} id:{t.id:4d} {t.name}")


def report_tournament_by_moderator(data: CommonData, tournaments: dict[int, Tournament], moderator_id: int):
    print(f"\nTotal number of tournaments: {len(tournaments)}")

    good_tournaments = {}
    for id, tournament in tournaments.items():
        for game in tournament.games:
            if game.moderator_id == moderator_id:
                good_tournaments[id] = tournament

    print(
        f"\n*** Tournaments of moderator: {moderator_id} ({len(good_tournaments)} items):")
    for id, t in good_tournaments.items():
        print(f"{t.id} {t.name}")


def tournaments_by_player(data: CommonData, tournaments: dict[int, Tournament], player_id: int):
    good_tournaments = []
    for id, tournament in tournaments.items():
        for place in tournament.places:
            if place['player_id'] == player_id:
                good_tournaments.append(id)

    print(f"\n*** Tournaments of player {player_id}")
    for id in sorted(good_tournaments):
        t = tournaments[id]
        num_players = len(t.places)
        print(f"{t.id:4d} {t.name}")
