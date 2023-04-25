from classes import Event


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
        print(f"Only one stage found")
        event = events[0]
        return event.is_main

    if len(events) == 2:
        print(f"Tournament with 2 stages")
        main_stage = find_main_stage(events)
        final_stage = find_final_stage(events)
        return main_stage and final_stage

    print(f"### Found more than two stages: {len(events)}")
    return False
