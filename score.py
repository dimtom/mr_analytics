from classes import *


def calcSlotMainScore(self: Slot):
    slot_red = self.role == "civ" or self.role == "sheriff"
    game_red = (self.game.result == "red")
    self.main_score = 1.0 if (slot_red and game_red) or (
        not slot_red and not game_red) else 0.0


def calcSlotLegacyScore(self: Slot):
    self.legacy_score = 0.0

    if self.legacy:
        legacy_count = 0
        for pos in self.legacy:
            idx = pos - 1
            role = self.game.slots[idx].role
            if role == "maf" or role == "don":
                legacy_count += 1

        if legacy_count == 2:
            self.legacy_score = 0.3
        elif legacy_count == 3:
            self.legacy_score = 0.5


def calcSlotPenaltyScore(self: Slot):
    self.penalty_score = 0.0
    if self.eliminated:
        if self.eliminated == "kickOut":
            self.penalty_score = -0.5
        elif self.eliminated == "warnings":
            self.penalty_score = -0.5
        elif self.eliminated == "teamKickOut":
            self.penalty_score = -0.7
        else:
            print("### Unknown eliminated: {self.eliminated}")


def calcSlotScores(self: Slot, weight: float):
    calcSlotMainScore(self)
    calcSlotLegacyScore(self)
    calcSlotPenaltyScore(self)

    # TODO: refactor, use Score object
    # sothat we can easy copy/merge/update scores
    self.main_score *= weight
    self.ci_score *= weight
    self.auto_score *= weight
    self.bonus_score *= weight
    self.penalty_score *= weight

    # TODO: refactor, create get_total_score() func
    # Also create function:
    # get_total_main_score (main + ci)
    # get_total_bonus_score (all bonuses)
    self.total_score = (self.main_score + self.ci_score +
                        self.legacy_score +
                        self.auto_score +
                        self.bonus_score +
                        self.penalty_score)


def calc_event_scores(event: Event, weight: float):
    print("\n*** Calculating event scores")

    # calc c(i)
    player_games_first_killed = defaultdict(set)
    player_games_first_killed_and_lost = defaultdict(set)
    for game in event.games:
        for slot in game.slots:
            if slot.first_killed and (slot.role == "civ" or slot.role == "sheriff"):
                player_games_first_killed[slot.player_id].add(game.id)

                if game.result == "black":
                    player_games_first_killed_and_lost[slot.player_id].add(
                        game.id)

    # Magic value: 0.4 (fiim rules)
    fiim_first_night_score = 0.4

    # TODO: TEMP WORKAROUND
    event.distance = 12  # TODO: calculate for every tournament!

    print("Calculating Ci for every player...")
    fiim_coeff_b = round(fiim_first_night_score * event.distance)
    for player in event.players.values():
        player.ci_score = 0.0

        games_first_killed = player_games_first_killed[player.id]
        games_first_killed_and_lost = player_games_first_killed_and_lost[player.id]
        num_games_first_killed = len(games_first_killed)
        num_games_first_killed_and_lost = len(games_first_killed_and_lost)
        if num_games_first_killed_and_lost == 0:
            continue

        # points =  * fiim_first_night_score
        ci_score = num_games_first_killed * fiim_first_night_score / fiim_coeff_b
        if ci_score < 0.0:
            ci_score = 0.0
        if ci_score > fiim_first_night_score:
            ci_score = fiim_first_night_score

        for game in event.games:
            if game.id in games_first_killed_and_lost:
                for slot in game.slots:
                    if slot.player_id == player.id:
                        slot.ci_score = ci_score

    # calc slots total scores
    print("Calculating slots scores...")
    for game in event.games:
        for slot in game.slots:
            calcSlotScores(slot, weight)

    print("Calculating players scores...")
    for player in event.players.values():
        player.total_score = 0.0
        player.main_score = 0.0
        player.ci_score = 0.0
        player.legacy_score = 0.0
        player.auto_score = 0.0
        player.bonus_score = 0.0
        player.penalty_score = 0.0

    for game in event.games:
        for slot in game.slots:
            player = event.players[slot.player_id]
            player.total_score += slot.total_score
            player.main_score += slot.main_score
            player.ci_score += slot.ci_score
            player.legacy_score += slot.legacy_score
            player.auto_score += slot.auto_score
            player.bonus_score += slot.auto_score + slot.bonus_score
            player.penalty_score += slot.penalty_score
