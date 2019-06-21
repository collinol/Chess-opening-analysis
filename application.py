import argparse
import datetime
import os
from api.api_read import ApiReader
from viz.bar_plot import Visualizer
import io
import random
import base64
from flask import Flask, Response, render_template, flash, redirect, request, url_for
from plotly.offline import plot
from plotly.graph_objs import Scatter
from flask import Markup
from FileTree.FileTrie import FileTrie
import os

app = Flask(__name__)
data = os.listdir("templates")
datatree = FileTrie()
for filename in data:
    if "_" in filename:
        datatree.add(filename)

def _create_from_api(username, datatree):
    pass


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/result', methods=['GET', 'POST'])
def result():
    error = None
    if request.method == 'POST':
        username = request.form.get('comp_select')

        lookup = datatree.lookup(username)
        
        def writer(data_exists):
            if data_exists:
                file_to_erase = lookup["user"]
                print("erasing",lookup["user"])
                datatree.remove(file_to_erase)
                os.system("rm templates/"+file_to_erase)
            api = ApiReader(username, 3) # TODO make years input-able
            results = api.parse_games()
            VizClass = Visualizer(results, datatree)
            new_file = VizClass.create_plot(username, datatree)
            return new_file


        if not lookup:
            return render_template(writer(data_exists=False)) # case where there's no data
        else:
            past = datetime.datetime.now() - datetime.timedelta(days=3)
            if past > lookup["last_updated"]: # obviously change the .now() after debugging
                print("need to replace old data")
                return render_template(writer(data_exists=True))
            else:
                print("recent data for this user exists, returned:", lookup["user"])
                return render_template(lookup["user"])

    # If user tries to get to page directly, redirect to submission page
    elif request.method == "GET":
        return redirect(url_for('submission', error=error))


if __name__=='__main__':
    app.run(debug=True)
    #_create_from_api('GetSchwifty10', tree)
