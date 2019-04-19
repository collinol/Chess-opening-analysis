import argparse
import datetime
import os
from api.api_read import ApiReader
from viz.bar_plot import Visualizer


def _create_from_api():
    api = ApiReader(args.user_name, 3)
    results = api.parse_games()
    # thread1 => create visual (move dataframe creation out)
    '''
    brainstorm about workflow:
    take `results` and create sorted dataframe (rip out logic from create_plot
    thread 1 creates visualization from sorted_dataframe
    thread 2 connects to DB.user via db.user.name(key) and writes sorted_dataframe.to_json to db.user.game_data
    
    '''
    # thread2 => write to db
    Visualizer(results).create_plot(args.user_name, write_to_db=True)


def _pull_from_db():
    # TODO
    '''
    connect to db.user via name (key)
    get json from db.user.game_data
    results = json -> dataframe
    Visualizer(results).create_plot(args.user_name)
       ^^^ after ripping out df creation logic, Visualizer shouldn't be initliazed with a dictionary data

    '''

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Visualize Chess Opening Stats')
    parser.add_argument('--user-name', type=str, help='chess.com username to get stats for')
    #parser.add_argument('--years', type=int, help='how many years back do you want to collect data for')

    args = parser.parse_args()
    # TODO
    '''
    connect to db
    look up by args.user_name
    if user_name found in db.users.name:
        created = db.users.time-created
        time_since_created = datetime.datetime.utcnow() - datetime.datetime.strptime(str(created), "%Y-%m-%d-%H:%M:%S.%f")
        if time_since_created.total_seconds() > 86400: #24 hour
            _create_from_api()
        else:
            _pull_from_db()
    else:
        create_from_api()
    '''
