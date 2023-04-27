import common_data
import mr_tournaments
import mr_games

from request_cache import RequestCache

from analyze_league import analyze_league
from analyze_tournament import analyze_tournament


def main():
    cache = RequestCache()
    cache.load()

    data = common_data.CommonData(cache)
    data.load()

    tournaments = analyze_league(data)
    # TODO: use tournaments for processing

    '''
    # Load all games of tournaments
    # NB: we need to use event_id, or update load_tournament_games
    # to handle event_id=None
    for year, ids in tournaments.items():
        print(f"\n*** Season: {year}")
        for tournament_id in ids:
            games = mr_games.load_tournament_games(
                data, tournament_id, event_id=None)
    '''

    # analyze single tournament

    # tournament_id = 115  # Friends cup 2023
    tournament_id = 116  # Golgen Gate 2023
    analyze_tournament(data, tournament_id)

    cache.save()
    pass


if __name__ == '__main__':
    main()
