import datetime
import time

import pandas as pd

import plotly.graph_objs as go


class Visualizer:

    def __init__(self, game_results, data):
        self.game_results = game_results
        self.current_data = data

    @staticmethod
    def _break_up_xlabels(string_list):
        cleaner_list = []
        cleaner_string = ""
        for g in string_list:
            for i, word in enumerate(g.split(' ')):
                if i == 3:
                    cleaner_string += '\n '
                cleaner_string += word + ' '
                if i == len(g.split(' ')) - 1:
                    cleaner_list.append(cleaner_string[0:-1])
                    cleaner_string = ""
        return cleaner_list

    def create_plot(self, user, datatree):


        df = pd.DataFrame(self.game_results)
        df = df.sort_values(by=0, axis=1, ascending=False)

        games = self.game_results.keys()
        sorted_by_sum = {}
        for k in games:
            sorted_by_sum[k] = sum(df[k])
        sorted_sums = sorted(sorted_by_sum.items(), key=lambda x: x[1], reverse=True)
        wins = [df[k[0]][0] for k in sorted_sums]
        losses = [df[k[0]][1] for k in sorted_sums]
        draws = [df[k[0]][2] for k in sorted_sums]
        ind = [i for i in range(len(games))]
        width = 0.6  # the width of the bars: can also be len(x) sequence
        trace1 = go.Bar(
            x=[k[0] for k in sorted_sums],
            y=wins,
            name='Wins'
        )
        trace2 = go.Bar(
            x=[k[0] for k in sorted_sums],
            y=losses,
            name='Losses'
        )

        trace3 = go.Bar(
            x=[k[0] for k in sorted_sums],
            y=draws,
            name='Draws'
        )



        data = [trace1, trace2, trace3]
        layout = go.Layout(
            barmode='stack',
            title=user+" Game Results"
        )

        fig = go.Figure(data=data, layout=layout)
        new_time = str(datetime.datetime.now()).replace(" ", "-")
        datatree.add("{}_{}".format(user, new_time))
        fig.write_html('templates/{}_{}.html'.format(user, new_time))
        return('{}_{}.html'.format(user, new_time))
