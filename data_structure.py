import pandas as pd
import functions as fnc


class Player:
    def __init__(self, name):
        self.name = name
        self.matches = pd.DataFrame()

    def addMatch(self, playername, match_overview, match_performance):
        filterd_overview = match_overview.iloc[0].drop(
            ["Team 1", "Team 2", "Team 1 Score", "Team 2 Score", "ATK at Start", "Team 1 ATK Wins", "Team 1 DEF Wins",
             "Team 2 ATK Wins", "Team 2 DEF Wins", "Team 1 Score at Half"])
        filterd_performance = match_performance.iloc[fnc.getplayerindex(playername, match_performance)]
        filterd_performance = filterd_performance.drop(
            ["Match ID", "Player", "K-D (+/-)", "Entry (+/-)", "Trade Diff.", "HS%", "ATK Op", "DEF Op",
             "In-game Points"])
        if filterd_overview["Winner"] == filterd_performance["Team"]:
            filterd_overview["Winner"] = True
        else:
            filterd_overview["Winner"] = False
        filterd_data = pd.concat([filterd_overview, filterd_performance.drop("Team")])
        if not self.matches.empty:
            if not (filterd_overview["Match ID"] in self.matches["Match ID"].values):
                self.matches = self.matches.append(filterd_data, ignore_index=True)
        else:
            self.matches = self.matches.append(filterd_data, ignore_index=True)

class Team:
    def __init__(self, name):
        self.name = name
        self.matches = pd.DataFrame(columns=fnc.team_match_columns_names)

    def addMatch(self, match_overview, user_input):
        mo = match_overview
        if not(mo["Match ID"][0] in self.matches["Match ID"].values):
            gamemode = user_input[0]
            match_info = user_input[1]
            winner_team = user_input[2]
            winner_maps = user_input[3]
            winner_ops = user_input[4]
            loser_team = user_input[5]
            loser_maps = user_input[6]
            loser_ops = user_input[7]
            if self.name == winner_team:
                winner = True
                banned_maps = winner_maps
                banned_ops = winner_ops
                own_score = max(mo["Team 1 Score"][0], mo["Team 2 Score"][0])
                enemy_score = min(mo["Team 1 Score"][0], mo["Team 2 Score"][0])
            else:
                winner = False
                banned_maps = loser_maps
                banned_ops = loser_ops
                own_score = min(mo["Team 1 Score"][0], mo["Team 2 Score"][0])
                enemy_score = max(mo["Team 1 Score"][0], mo["Team 2 Score"][0])

            data = [mo["Match ID"][0], mo["Timestamp"][0], gamemode, match_info, banned_maps, banned_ops, mo["Map"][0], winner, own_score, enemy_score, pd.DataFrame()]
            self.matches = self.matches.append(pd.DataFrame([data], columns=fnc.team_match_columns_names))
        else:
            print("Matchdata alreay added")

    #def addRound(self):

