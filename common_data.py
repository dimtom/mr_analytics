import load_common


class CommonData:
    def __init__(self):
        self.countries = None
        self.cities = None
        self.clubs = None
        self.players = None

    def load(self):
        self.countries = load_common.load_countries()
        self.cities = load_common.load_cities()
        self.clubs = load_common.load_clubs(self.cities, self.countries)

        # TODO:
        # self.players = load_common.load_players()

    pass
