import datetime

import pandas as pd
import matplotlib.pyplot as plt


class Visualizer:

    def __init__(self, game_results):
        self.game_results = game_results

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

    def create_plot(self, user, write_to_db=False):
        df = pd.DataFrame(self.game_results)
        df = df.sort_values(by=0, axis=1, ascending=False)
        #if write_to_db:
         #   df.to_csv('Data/{}_{}.tsv'.format(user,str(datetime.datetime.utcnow()).replace(' ','-')), sep='\t')
            #TODO ^ should write to DB
            #'''
            #columns: user-name (key) | time-updated | opening1 | opening2 | ... | opening n
            #'''

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

        fig, axs = plt.subplots(nrows=1, ncols=1)
        data = axs

        p1 = data.bar(ind, [i + j + k for i, j, k in zip(losses, wins, draws)], width, color='g')
        p2 = data.bar(ind, [i + j for i, j in zip(losses, draws)], width, color='r')
        p3 = data.bar(ind, draws, width, color='b')

        data.set_ylabel('Games Played')

        data.set_xticks(ind)
        data.legend((p1[0], p2[0], p3[0]), ('Wins', 'Losses', 'Draws'))
        rects = data.patches

        for label in data.xaxis.get_ticklabels()[::2]:
            label.set_visible(False)
        for rect, label in zip(rects, [item[0] for item in sorted_sums]):
            height = rect.get_height()
            data.text(rect.get_x() + rect.get_width() / 2, height, label, ha='center', va='bottom', rotation=90)
        plt.title("Game Results Amongst Openings Played")
        return fig
