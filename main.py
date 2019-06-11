import argparse
import datetime
import os
from api.api_read import ApiReader
from viz.bar_plot import Visualizer
import io
import random
import base64
from flask import Flask, Response, render_template, flash, redirect, request, url_for
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from plotly.offline import plot
from plotly.graph_objs import Scatter
from flask import Markup


app = Flask(__name__)

def _create_from_api(username):
    api = ApiReader(username, 3)
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
    return VizClass.create_plot(username, write_to_db=True)





@app.route('/')
def main():
    return render_template('homepage.html')


@app.route('/result', methods=['GET', 'POST'])
def result():
    error = None
    if request.method == 'POST':
        username = request.form.get('comp_select')
        fig = _create_from_api(username)
        return render_template('result.html')
    # If user tries to get to page directly, redirect to submission page
    elif request.method == "GET":
        return redirect(url_for('submission', error=error))



if __name__=='__main__':
    app.run(debug=True)
    #_create_from_api('GetSchwifty10')
