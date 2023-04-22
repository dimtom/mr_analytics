import mr_api
import common_data
import mr_tournaments
import mr_games


def main():
    data = common_data.CommonData()
    data.load()

    seasons = {
        2017: ["2017-01-01", "2020-01-01"],
        2020: ["2020-01-01", "2021-01-01"],
        2021: ["2021-01-01", "2022-01-01"],
        2022: ["2022-01-01", "2023-01-01"],
        2023: ["2023-01-01", "now"],
    }

    # uncomment it
    '''
    tournaments = {}
    for year, dates in seasons.items():
        print(f"\n*** Season: {year}")
        date_from, date_to = dates
        t = mr_tournaments.load_tournaments(
            data, date_from, date_to, verbose=True)
        tournaments[year] = t
    '''

    '''for year, ids in tournaments.items():
        print(f"\n*** Season: {year}")
        for tournament_id in ids:
            games = mr_games.load_tournament_games(data, tournament_id)
    '''

    # just try to load games of VaWaCa
    tournament_id = 11
    games = mr_games.load_tournament_games(data, tournament_id)

    # TODO: save tournaments to disk
    pass


if __name__ == '__main__':
    main()
