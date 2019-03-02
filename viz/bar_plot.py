import pandas as pd
import matplotlib.pyplot as plt


class Visualizer:

    def __init__(self, game_results):
        self.game_results = game_results

    def create_plot(self):
        df = pd.DataFrame(self.game_results)

        wins = [df[k][0] for k in self.game_results.keys()]
        losses = [df[k][1] for k in self.game_results.keys()]
        draws = [df[k][2] for k in self.game_results.keys()]
        ind = [i for i in range(len(self.game_results.keys()))]
        width = 0.6 # the width of the bars: can also be len(x) sequence

        p1 = plt.bar(ind, wins, width, color='g')
        p2 = plt.bar(ind, losses, width, color='r')
        p3 = plt.bar(ind, draws, width, color = 'b')

        plt.ylabel('Games Played')
        plt.title('Game Results Amongst Openings Played')
        plt.xticks(ind, self.game_results.keys())
        plt.legend((p1[0], p2[0], p3[0]), ('Wins', 'Losses', 'Draws'))
        plt.xticks(rotation=90)
        plt.show()
