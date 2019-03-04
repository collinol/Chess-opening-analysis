import pandas as pd
import matplotlib.pyplot as plt


class Visualizer:

    def __init__(self, game_results):
        self.game_results = game_results

    def _break_up_xlabels(self, string_list):
        cleaner_list = []
        cleaner_string = ""
        for g in string_list:
            import pdb
            #pdb.set_trace()
            for i, word in enumerate(g.split(' ')): 
                # pdb.set_trace()
                if i == 3:
                    cleaner_string += '\n'
                cleaner_string += word+' '
                # print(i,len(g.split(' ')) -1, word)
                if i == len(g.split(' ')) - 1:
                    cleaner_list.append(cleaner_string[0:-1])
                    cleaner_string = ""
        return cleaner_list 

    def create_plot(self):
        df = pd.DataFrame(self.game_results)
        import pdb
        # pdb.set_trace()
        games = self.game_results.keys()
        wins = [df[k][0] for k in games]
        losses = [df[k][1] for k in games]
        draws = [df[k][2] for k in games]
        ind = [i for i in range(len(games))]
        width = 0.6 # the width of the bars: can also be len(x) sequence
        self._break_up_xlabels(games)
        p1 = plt.bar(ind, wins, width, color='g')
        p2 = plt.bar(ind, losses, width, color='r')
        p3 = plt.bar(ind, draws, width, color = 'b')

        plt.ylabel('Games Played')
        plt.title('Game Results Amongst Openings Played')
        plt.xticks(ind, games)
        # plt.tick_params(labelsize=3)
        plt.legend((p1[0], p2[0], p3[0]), ('Wins', 'Losses', 'Draws'))
        plt.xticks(rotation=90)
        plt.show()
