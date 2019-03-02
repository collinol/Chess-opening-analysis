import argparse

from api.api_read import ApiReader
from viz.bar_plot import Visualizer

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Visualize Chess Opening Stats')
    parser.add_argument('--user-name', type=str, help='chess.com username to get stats for')
    parser.add_argument('--years', type=int, help='how many years back do you want to collect data for')

    args = parser.parse_args()
    api = ApiReader(args.user_name, args.years)
    results = api.parse_games()
    Visualizer(results).create_plot()
    results = api.parse_games()

# TODO - create main() with arg parser for user name and number of years
# TODO - flask app
# TODO - Port to GCP
