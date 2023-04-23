
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


class Game:
    id: int
    tournament: Tournament

    players: list[Player]

    def __init__(self, id: int, tournament: Tournament):
        self.id = id
        self.tournament = tournament

    def __str__(self):
        return f"game #{self.id:04d}"


class Player:
    id: int
    name: str
    all_names: set[str] = None

    games: int = 0
    tournaments: int = 0

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
