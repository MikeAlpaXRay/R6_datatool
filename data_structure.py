import pandas as pd


class Player:
    def __init__(self, name):
        self.name = name
        self.matches = pd.DataFrame()

    def addMatch(self, playername, match_overview, match_performance):
        filterd_overview = match_overview.iloc[0].drop(
            ["Team 1", "Team 2", "Team 1 Score", "Team 2 Score", "ATK at Start", "Team 1 ATK Wins", "Team 1 DEF Wins",
             "Team 2 ATK Wins", "Team 2 DEF Wins", "Team 1 Score at Half"])
        filterd_performance = match_performance.iloc[match_performance.Player[match_performance.Player == playername].index[0]]
        filterd_performance = filterd_performance.drop(
            ["Match ID", "Player", "K-D (+/-)", "Entry (+/-)", "Trade Diff.", "HS%", "ATK Op", "DEF Op", "In-game Points"])
        if filterd_overview["Winner"] == filterd_performance["Team"]:
            filterd_overview["Winner"] = True
        else:
            filterd_overview["Winner"] = False
        filterd_data = pd.concat([filterd_overview, filterd_performance.drop("Team")])
        if not(self.matches.empty):
            if not(filterd_overview["Match ID"] in self.matches["Match ID"].values):
                self.matches = self.matches.append(filterd_data)
        else:
            self.matches = self.matches.append(filterd_data)
