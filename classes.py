from collections import defaultdict


class Country:
    id: int
    name: str

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return self.name
    pass


class City:
    id: int
    name: str

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return self.name

    pass


class Club:
    id: int
    name: str
    city: City

    def __init__(self, id: int, name: str, city: City):
        self.id = id
        self.name = name
        self.city = city

    def __str__(self):
        return self.name

    pass


class Game:
    pass


class Player:
    pass


class Tournament:
    id: int
    name: str
    club: Club
    city: City
    games: list[Game] = None
    players: list[Player] = None

    def __init__(self, id: int, name: str, club: Club, city: City):
        self.id = id
        self.name = name
        self.club = club
        self.city = city

    def __str__(self):
        return self.name


class Event:
    id: int
    weight: float
    is_final_stage: bool

    def __init__(self, id: int, weight: float, is_final: bool):
        self.id = id
        self.weight = weight
        self.is_final_stage = is_final


class Slot:
    pass


class Game:
    tournament: Tournament
    id: int
    moderator_id: int
    result: str
    slots: list[Slot]

    def __init__(self, tournament: Tournament, id: int, moderator_id: int, winner: str):
        self.tournament = tournament
        self.id = id
        self.moderator_id = moderator_id
        self.result = "red" if winner == "civ" else "black"
        # for debug
        # print(f"Init game: {self.id} result: {self.result}")

    def check_slots_valid(self, slots: list[Slot]):
        for s in slots:
            assert(s.game == self)

        role_count = defaultdict(int)
        for s in slots:
            role_count[s.role] += 1
        assert(role_count['civ'] == 6)
        assert(role_count['sheriff'] == 1)
        assert(role_count['maf'] == 2)
        assert(role_count['don'] == 1)

    def set_slots(self, slots: list[Slot]):
        assert(len(slots) == 10)

        self.check_slots_valid(slots)
        self.slots = slots

    def __str__(self):
        return f"game #{self.id:04d}"


class Slot:
    '''
    Slot represents player in current game sitting at specific position (1-10)
    with specific role and specific outcome
    '''
    game: Game
    position: int
    player_id: int
    player_name: str

    first_killed: bool
    eliminated: str = None

    legacy: list[int] = None
    role: str  # civ, maf, don, sheriff

    # TODO: refactor and put Score class inside player
    main_score: float  # main score (win or loose)
    ci_score: float
    legacy_score: float
    auto_score: float
    bonus_score: float  # additional score (by moderator)
    penalty_score: float  # penalty for kick-out (team kick-out)
    total_score: float  # main total number of score for player per game

    def __init__(self, game: Game, position: int, player_id: int, player_name: str):
        self.game = game
        self.position = position
        assert(self.position >= 1 and self.position <= 10)

        self.player_id = player_id
        self.player_name = player_name

        self.main_score = 0.0
        self.ci_score = 0.0

        self.auto_score = 0.0
        self.bonus_score = 0.0
        self.penalty_score = 0.0
        self.total_score = 0.0

    def short_role(self):
        if self.role == "civ":
            return " "
        elif self.role == "maf":
            return "M"
        elif self.role == "don":
            return "D"
        elif self.role == "sheriff":
            return "S"
        else:
            # for debug
            # print(f"### Unknown role: {self.role}")
            return None

    def calcMainScore(self):
        slot_red = self.role == "civ" or self.role == "sheriff"
        game_red = (self.game.result == "red")
        self.main_score = 1.0 if (slot_red and game_red) or (
            not slot_red and not game_red) else 0.0

    def calcLegacyScore(self):
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

    def calcPenaltyScore(self):
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

    def calcTotalScore(self):
        self.calcMainScore()
        self.calcLegacyScore()
        self.calcPenaltyScore()
        self.total_score = (self.main_score + self.ci_score +
                            self.legacy_score +
                            self.auto_score +
                            self.bonus_score +
                            self.penalty_score)

    pass


class Player:
    id: int
    name: str
    all_names: set[str] = None

    games: int = 0
    tournaments: int = 0

    # TODO: refactor and put Score class inside player

    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
        self.all_names = {name}
        self.games = 0
        self.tournaments = 0

    def add_name(self, another_name: str):
        self.all_names.add(another_name)

    def __str__(self):
        return self.name

    def toJson(self):
        return {'id': self.id, 'name': self.name}
