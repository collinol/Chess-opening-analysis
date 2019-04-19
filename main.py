import argparse
import datetime
import os
from api.api_read import ApiReader
from viz.bar_plot import Visualizer


def _create_from_api():
    api = ApiReader(args.user_name, 3)
    results = api.parse_games()
    Visualizer(results).create_plot(args.user_name, write_to_db=True)


def _create_from_file():
    # TODO
    '''
    connect to db
    look up by args.user_name
    results = create dict out of DB lookup (some kind of function?)
    Visualizer(results).create_plot(args.user_name)
    '''



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Visualize Chess Opening Stats')
    parser.add_argument('--user-name', type=str, help='chess.com username to get stats for')
    #parser.add_argument('--years', type=int, help='how many years back do you want to collect data for')

    args = parser.parse_args()
    # check for file
    for fname in os.listdir('Data'):
        if args.user_name in fname:
            created = fname.split('_')[1].split('.tsv')[0]
            time_since_created = datetime.datetime.utcnow() - datetime.datetime.strptime(str(created), "%Y-%m-%d-%H:%M:%S.%f")
            if time_since_created.total_seconds() > 86400: #24 hours
                _create_from_api()
            else:
                _create_from_file('Data/'+fname)
        else:
            _create_from_api()