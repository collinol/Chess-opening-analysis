import requests
import datetime


class ApiReader:

    def __init__(self, name, years):
        self.user_name = name
        self.past_years = years

    def get_games(self):
        # todo - check for existing file and write instead of api callling on user already analyzed
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
                        split_up = game_type.split('-')
                        game_type_abbrv = "Other"
                        try:
                            game_type_abbrv = ' '.join(split_up[0:split_up.index('Attack')])
                        except ValueError:
                            pass
                        try:
                            game_type_abbrv = ' '.join(split_up[0:split_up.index('Opening')])
                        except ValueError:
                            pass
                        try:
                            game_type_abbrv = ' '.join(split_up[0:split_up.index('Defense')])
                        except ValueError:
                            pass
                        if game_type_abbrv not in openings:
                            openings[game_type_abbrv] = individual_results
                        else:
                            openings[game_type_abbrv][0] += individual_results[0]
                            openings[game_type_abbrv][1] += individual_results[1]
                            openings[game_type_abbrv][2] += individual_results[2]
        return openings

