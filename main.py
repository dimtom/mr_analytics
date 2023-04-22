import mr_api
import common_data
import mr_tournaments


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

    tournaments = {}
    for year, dates in seasons.items():
        print(f"Season: {year}")
        date_from, date_to = dates
        t = mr_tournaments.load_tournaments(
            data, date_from, date_to, verbose=True)
        tournaments[year] = t

    # TODO: save tournaments to disk
    pass


if __name__ == '__main__':
    main()
