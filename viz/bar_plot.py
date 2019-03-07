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
                cleaner_string += word+' '
                if i == len(g.split(' ')) - 1:
                    cleaner_list.append(cleaner_string[0:-1])
                    cleaner_string = ""
        import pdb
        pdb.set_trace()
        return cleaner_list

    def create_plot(self):
        df = pd.DataFrame(self.game_results)
        games = self.game_results.keys()
        wins = [df[k][0] for k in games]
        losses = [df[k][1] for k in games]
        draws = [df[k][2] for k in games]
        ind = [i for i in range(len(games))]
        width = 0.6 # the width of the bars: can also be len(x) sequence
        #self._break_up_xlabels(games)
        fig, axs = plt.subplots(nrows=1, ncols=1)
        data = axs
        p1 = data.bar(ind, losses, width, color='g')
        p2 = data.bar(ind, wins, width, color='r')
        p3 = data.bar(ind, draws, width, color='b')
        import pdb
        pdb.set_trace()
        data.set_ylabel('Games Played')
        #data.title('Game Results Amongst Openings Played')
        data.set_xticks(ind)
        # plt.tick_params(labelsize=3)
        data.legend((p1[0], p2[0], p3[0]), ('Losses', 'Wins', 'Draws'))
        #data.xticks(rotation=90)
        rects = data.patches
        
        #game_legend = axs[1]
        for label in data.xaxis.get_ticklabels()[::2]:
            label.set_visible(False)
        for rect,label in zip(rects, games):
            height = rect.get_height()
            data.text(rect.get_x() + rect.get_width() / 2, height+5, label, ha='center', va='bottom', rotation=90)
        #game_legend.figure(figsize=(8, (len(tests) * 1) + 2))
        #game_legend.plot([0, 0], 'r')
        #game_legend.axis([0, 3, -len(games), 0])
        #game_legend.set_yticks([-i for i in range(len(games))])
        #for i, s in enumerate(games):
        #    game_legend.text(0.1, -i, s, fontsize=8)
        #for label in game_legend.yaxis.get_ticklabels()[::2]:
        #    label.set_visible(False)
        plt.show()

        #todo - get rid of subplots and try to put the label at the top of the bar maybe?
