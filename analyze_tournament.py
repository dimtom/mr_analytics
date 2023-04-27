from classes import *
from common_data import CommonData
from mr_request import MrRequest
from request_cache import RequestCache

from copy import copy

import mr_tournament
import mr_games
import output
import score
from stage import *
import json


def analyze_tournament(data: CommonData, tournament_id: int):
    tournament = mr_tournament.get_tournament_info(data, tournament_id)
    print(
        f"\n*** Tournament: {tournament.name} Club: {tournament.club} City: {tournament.city}")

    events = mr_tournament.get_tournament_events(data, tournament_id)
    tournament.events = events

    output_stages(events)
    if not validate_stages(events):
        print("### Tournament validation failed, exit")
        return

    main_stage = find_main_stage(events)
    final_stage = find_final_stage(events)

    stages = [main_stage, final_stage]
    for stage in stages:
        print(f"\n*** Stage: {stage.id}")
        games_json = mr_games.load_tournament_games(
            data, tournament_id, stage.id)
        stage_games, stage_players = mr_games.process_tournament_games(
            data, tournament, games_json)
        stage.games = stage_games
        stage.players = stage_players

        stage.distance = calculate_stage_distance(stage)

        # calculate scores for every player
        weight = stage.weight
        score.calc_event_scores(stage, weight)

        output.output_games(stage.games, stage.players)

        # print(stage_players)
        output.output_players(stage.players)

    # TODO: merge players of stages
    # Technically, it is not good to have MANY sets of players
    # as game points to Stage-Player with not final scores
    tournament_players = dict[int, Player]()
    for p in main_stage.players.values():
        # here we create COPY of Player
        # so we have 3 instances of the same player:
        # in main stage, in final stage, and in tournament itself...
        tournament_players[p.id] = copy(p)

    for p in final_stage.players.values():
        if p.id not in tournament_players:
            # it CAN NOT happen, final player MUST be in main stage
            # but...
            print(
                f"### Player in finals but does not play in main stage: {p.name}")
            tournament_players[p.id] = copy(p)
            continue

        tournament_players[p.id].total_score += p.total_score
        tournament_players[p.id].main_score += p.main_score
        tournament_players[p.id].ci_score += p.ci_score

        tournament_players[p.id].legacy_score += p.legacy_score
        tournament_players[p.id].auto_score += p.auto_score
        tournament_players[p.id].bonus_score += p.bonus_score
        tournament_players[p.id].penalty_score += p.penalty_score

    tournament.players = tournament_players
    tournament.games = main_stage.games + final_stage.games

    print("\n*** Final table of tournament:")
    output.output_players(tournament_players)

    print("\n*** Top5 players by total bonus score")
    output.output_bonus_players(tournament_players)

    # use places API to get only places
    places = mr_tournament.get_tournament_places(data, tournament_id)
    sorted_places = sorted(places, key=lambda item: item['place'])

    print("\n*** Tournament places")
    for p in sorted_places:
        player = tournament.players[p['player_id']]
        games_count = p['games_count']
        print(f"#{p['place']:<2d} {player.name[:20]:<20s} games:{games_count}")

    return tournament
