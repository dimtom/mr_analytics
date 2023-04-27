import mr_tournaments
from common_data import CommonData


def analyze_league(data: CommonData):
    seasons = {
        2017: ["2017-01-01", "2020-01-01"],
        2020: ["2020-01-01", "2021-01-01"],
        2021: ["2021-01-01", "2022-01-01"],
        2022: ["2022-01-01", "2023-01-01"],
        2023: ["2023-01-01", "now"],
    }

    tournaments = {}
    for year, dates in seasons.items():
        print(f"\n*** Season: {year}")
        date_from, date_to = dates
        t = mr_tournaments.load_tournaments(
            data, date_from, date_to, verbose=True)
        tournaments[year] = t

    return tournaments
