from classes import Event
from collections import defaultdict


def output_stages(events):
    for event in events:
        print(
            f"Stage. Final: {event.is_final_stage} Weight: {event.weight}")


def find_main_stage(events):
    for event in events:
        if not event.is_final_stage:
            return event
    return None


def find_final_stage(events):
    for event in events:
        if event.is_final_stage:
            return event
    return None


def validate_stages(events: list[Event]) -> bool:
    if len(events) == 0:
        print(f"### No stages found!")
        return False

    if len(events) == 1:
        # print(f"Only one stage found")
        event = events[0]
        # single stage MUST be main, not final
        return not event.is_final_stage

    if len(events) == 2:
        # print(f"Tournament with 2 stages")
        main_stage = find_main_stage(events)
        final_stage = find_final_stage(events)
        return main_stage and final_stage

    print(f"### Found more than two stages: {len(events)}")
    return False


def calculate_stage_distance(stage: Event):
    # technically, every player MUST play the same number of games in a stage
    # Except rare cases: substitutions, unknown players in the game

    player_distance = defaultdict(int)
    for game in stage.games:
        for slot in game.slots:
            player_id = slot.player_id
            player_distance[player_id] += 1

    distance_players = defaultdict(list)
    for player_id, distance in player_distance.items():
        distance_players[distance].append(player_id)

    if len(distance_players) == 1:
        # great! this is a good stage
        return list(distance_players.keys())[0]

    print("### This is unusual stage: check the distances")
    print(distance_players)

    best_distance = None
    best_player_len = None
    for d, players in distance_players.items():
        if best_distance is None or best_player_len < len(players):
            best_distance = d
            best_player_len = len(players)

    print(f"Picked the best distance: {best_distance}")
    return best_distance
