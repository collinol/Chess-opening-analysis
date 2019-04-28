import argparse
import datetime
import os
from api.api_read import ApiReader
from viz.bar_plot import Visualizer
import io
import random
from flask import Flask, Response, render_template
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

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
    VizClass = Visualizer(results)
    return VizClass.create_plot(args.user_name, write_to_db=True)


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

    app = Flask(__name__)


    @app.route('/')
    def main():
        return render_template('index.html')


    @app.route('/analysis')
    def plot_png():
        fig = create_figure()
        output = io.BytesIO()
        import pdb
        pdb.set_trace()
        FigureCanvas(fig).print_png(output)

        return Response(output.getvalue(), mimetype='image/png')


    def create_figure():

        return _create_from_api()

    app.run()





