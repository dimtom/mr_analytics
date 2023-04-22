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


class Tournament:
    id: int
    name: str
    club: Club
    city: City


class Player:
    id: int
    name: str
    all_names: list[str] = None

    games: int = 0
    tournaments: int = 0

    def __init__(self, id: int):
        self.id = id
        self.name = None
        self.all_names = []
        self.games = 0
        self.tournaments = 0
    pass
