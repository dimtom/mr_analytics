import load_common


class CommonData:
    def __init__(self):
        self.countries = None
        self.cities = None
        self.clubs = None
        self.players = None

    def load(self, verbose=False):
        self.countries = load_common.load_countries()
        self.cities = load_common.load_cities()
        self.clubs = load_common.load_clubs(self.cities, self.countries)

        # TODO:
        # self.players = load_common.load_players()

    def country_name(self, country_id):
        return self.countries[country_id]

    def city_name(self, city_id):
        return self.cities[city_id]

    def club_name(self, club_id):
        return self.clubs[club_id]['name'] if club_id in self.clubs else "### Unknown club"

    def club_city(self, club_id):
        return self.clubs[club_id]['city'] if club_id in self.clubs else "### Unknown city"

    pass
