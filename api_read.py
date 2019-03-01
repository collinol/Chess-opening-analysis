import requests
import datetime
import pandas as pd
import matplotlib.pyplot as plt


class ApiReader:

    def __init__(self, name, years):
        self.user_name = name
        self.past_years = years

    def get_games(self):
        current_day = datetime.datetime.now()
        year = current_day.year
        month = current_day.month
        all_games = ""
        print("collecting games from history...")
        while current_day.year - year < self.past_years:
            if current_day.year == year:
                for specific_month in range(month, -1, -1):
                    games_for_month = requests.get(
                        "https://api.chess.com/pub/player/{}/games/{}/{}".format(self.user_name, year,
                                                                                 specific_month))
                    if games_for_month.status_code != 404:
                        all_games += games_for_month.text
            else:
                for specific_month in range(12, -1, -1):
                    games_for_month = requests.get(
                        "https://api.chess.com/pub/player/{}/games/{}/{}".format(self.user_name, year,
                                                                                 specific_month))
                    if games_for_month.status_code != 404:
                        all_games += games_for_month.text
            year -= 1
        return all_games

    def parse_games(self):
        games = self.get_games()
        user = None
        openings = {}

        print('Parsing games for results...')
        for game in games.split(','):
            if 'pgn' in game:
                individual_results = [0, 0, 0]  # [w, l, d]
                for component in game.split('\\n'):
                    if self.user_name in component and ('Black' in component or 'White' in component):
                        user = 1 if 'White' in component else 0
                    if 'Result' in component:
                        if '0-1' in component:
                            if user == 0:
                                individual_results[1] += 1
                            else:
                                individual_results[0] += 1
                        elif '1-0' in component:
                            if user == 1:
                                individual_results[0] += 1
                            else:
                                individual_results[1] += 1
                        else:
                            individual_results[2] += 1
                    if 'ECOUrl' in component:
                        game_type = component.split('/')[-1].split('\\')[0][4:]
                        if game_type not in openings:
                            openings[game_type] = individual_results
                        else:
                            openings[game_type][0] += individual_results[0]
                            openings[game_type][1] += individual_results[1]
                            openings[game_type][2] += individual_results[2]

        return openings


class Visualizer:

    def __init__(self, game_results):
        self.game_results = game_results

    def create_plot(self):
        df = pd.DataFrame(self.game_results)

        wins = [df[k][0]/(df[k][0]+df[k][1]+df[k][2])*100 for k in self.game_results.keys()]
        losses = [df[k][1]/(df[k][0]+df[k][1]+df[k][2])*100 for k in self.game_results.keys()]
        draws = [df[k][2]/(df[k][0]+df[k][1]+df[k][2])*100 for k in self.game_results.keys()]
        ind = [i for i in range(len(self.game_results.keys()))]
        width = 0.6 # the width of the bars: can also be len(x) sequence

        p1 = plt.bar(ind, wins, width, color='r')
        p2 = plt.bar(ind, losses, width, color='b')
        p3 = plt.bar(ind, draws, width, color = 'g')

        plt.ylabel('Scores')
        plt.title('Scores by group and gender')
        plt.xticks(ind, self.game_results.keys())
        plt.legend((p1[0], p2[0], p3[0]), ('Wins', 'Losses', 'Draws'))

        plt.show()


api = ApiReader('GetSchwifty10', 2)
results = api.parse_games()

Visualizer(results).create_plot()

# TODO - 'squish' game type names (all variations can(/should?) just be shortened to the main line version)
    # ^ will get better spread data
# TODO - create main() with arg parser for user name and number of years
# TODO - tilt game type names to be readable on x-axis (to after step 1)
