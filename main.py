import common_data
import mr_tournaments
import mr_games

from request_cache import RequestCache

from analyze_tournament import analyze_tournament


def main():
    cache = RequestCache()
    cache.load()

    data = common_data.CommonData(cache)
    data.load()

    '''seasons = {
        2017: ["2017-01-01", "2020-01-01"],
        2020: ["2020-01-01", "2021-01-01"],
        2021: ["2021-01-01", "2022-01-01"],
        2022: ["2022-01-01", "2023-01-01"],
        2023: ["2023-01-01", "now"],
    }

    # uncomment it
    tournaments = {}
    for year, dates in seasons.items():
        print(f"\n*** Season: {year}")
        date_from, date_to = dates
        t = mr_tournaments.load_tournaments(
            data, date_from, date_to, verbose=True)
        tournaments[year] = t
    '''

    '''
    for year, ids in tournaments.items():
        print(f"\n*** Season: {year}")
        for tournament_id in ids:
            games = mr_games.load_tournament_games(data, tournament_id)
    '''

    # just try to load games of VaWaCa
    # tournament_id = 11
    # games = mr_games.load_tournament_games(data, tournament_id)

    # Analyze GoldenGate-2023
    tournament_id = 116
    analyze_tournament(data, tournament_id)

    # TODO: save tournaments to disk

    cache.save()
    pass


if __name__ == '__main__':
    main()
