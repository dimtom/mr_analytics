from classes import *


def output_games(games, players):
    print("Games of tournament:")
    print(f"*** Total number of games: {len(games)}")
    for game in games:
        output_game_score(game, players)


def output_game_score(game: Game, players: dict[int, Player]):
    print(f"\n* Game {game.id}. Result: {game.result}")
    for slot in game.slots:
        blank_str = "      "

        total_score_str = f"{slot.total_score: 6.2f}"
        main_score_str = f"{slot.main_score: 6.2f}" if slot.main_score != 0.0 else blank_str
        legacy_score_str = f"{slot.legacy_score: 6.2f}" if slot.legacy_score != 0.0 else blank_str
        auto_score_str = " X " if slot.auto_score == 0.0 else " - "
        bonus_score_str = f"{slot.bonus_score: 6.2f}" if slot.bonus_score != 0.0 else blank_str
        penalty_score_str = f"{slot.penalty_score:6.2f}" if slot.penalty_score != 0.0 else blank_str

        print(
            f"({slot.short_role()}) {slot.player_name[:16]:16s}: {total_score_str} {main_score_str} {auto_score_str} {bonus_score_str} {penalty_score_str}")

    # print info on first-kill
    for slot in game.slots:
        if not slot.first_killed:
            continue
        fk_name = players[slot.player_id].name
        print(
            f"FK: {fk_name}. Legacy: {slot.legacy}. Score: {slot.legacy_score}. Ci: {slot.ci_score: 4.2f}")


def output_players(players):
    print(f"\n***Total number of players: {len(players)}")
    sorted_players = sorted(players.values(),
                            key=lambda player: player.total_score, reverse=True)

    print("Players of tournament:")
    for player in sorted_players:
        total_score_str = f"{player.total_score: 6.2f}"
        main_score_str = f"{player.main_score: 6.2f}"
        print(f"{player.name[:16]:16s} {total_score_str} {main_score_str} {player.legacy_score:6.2f} {player.bonus_score:6.2f} {player.penalty_score:6.2f} {player.ci_score:6.2f}")
