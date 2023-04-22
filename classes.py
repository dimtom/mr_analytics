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
    nickname: str
    all_names: list[str]
