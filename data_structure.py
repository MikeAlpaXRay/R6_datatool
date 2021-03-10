import time
import pandas as pd
import functions as fnc
import user_constants as uc


class Player:
    def __init__(self, name):
        self.name = name
        self.matches = pd.DataFrame()

    def addMatch(self, playername, match_overview, match_performance):

        filterd_overview = match_overview.iloc[0].drop(
            ["Team 1", "Team 2", "Team 1 Score", "Team 2 Score", "ATK at Start", "Team 1 ATK Wins", "Team 1 DEF Wins",
             "Team 2 ATK Wins", "Team 2 DEF Wins", "Team 1 Score at Half", "Team 2 Score at Half"])
        filterd_performance = match_performance.loc[fnc.getplayerindex(playername, match_performance)]

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
        self.matches = pd.DataFrame(columns=fnc.uc.team_match_columns_names)

    def addMatch(self, match_overview, player_round_data, user_input):
        mo = match_overview
        if not (mo["Match ID"].values[0] in self.matches["Match ID"].values):
            gamemode = user_input[0]
            match_info = user_input[1]
            blue_team = user_input[2]
            blue_maps = user_input[3]
            blue_ops = user_input[4]
            orange_team = user_input[5]
            orange_maps = user_input[6]
            orange_ops = user_input[7]

            if mo["Team 1 Score"].values[0] == mo["Team 2 Score"].values[0]:
                outcome = "Draw"
            else:
                outcome = mo["Winner"].values[0]
            if not (outcome == "Draw"):
                if self.name == blue_team:
                    if outcome == "Blue":
                        outcome = "Win"
                    else:
                        outcome = "Lose"
                else:
                    if outcome == "Orange":
                        outcome = "Win"
                    else:
                        outcome = "Lose"

            if self.name == blue_team:
                round_data = self.getRoundData(player_round_data, "Blue")
                banned_maps = blue_maps
                banned_ops = blue_ops
                own_score = max(mo["Team 1 Score"].values[0], mo["Team 2 Score"].values[0])
                enemy_score = min(mo["Team 1 Score"].values[0], mo["Team 2 Score"].values[0])
            else:
                round_data = self.getRoundData(player_round_data, "Orange")
                banned_maps = orange_maps
                banned_ops = orange_ops
                own_score = min(mo["Team 1 Score"].values[0], mo["Team 2 Score"].values[0])
                enemy_score = max(mo["Team 1 Score"].values[0], mo["Team 2 Score"].values[0])
            data = [mo["Match ID"].values[0], mo["Timestamp"].values[0], gamemode, match_info, banned_maps, banned_ops,
                    mo["Map"].values[0], outcome, own_score, enemy_score, round_data]

            self.matches = self.matches.append(pd.DataFrame([data], columns=fnc.uc.team_match_columns_names))

        else:
            print("Matchdata already added")
            time.sleep(5)

    def getRoundData(self, player_round_data, team):
        filterd_team_data = player_round_data.loc[player_round_data["Team"] == team]
        filterd_data = filterd_team_data.loc[filterd_team_data["Player"] == filterd_team_data["Player"].values[0]]
        filterd_data = filterd_data.astype({"Round": 'int'}).set_index("Round")
        for idx, end_type in enumerate(filterd_data["Victory Type"].values):
            if end_type == "Time Limit Reached":
                if int(filterd_data["Round Time (ms)"].iloc[idx]) >= 225000:
                    filterd_data.loc[idx + 1, "Victory Type"] = "Time Limit Reached"
                else:
                    filterd_data.loc[idx + 1, "Victory Type"] = "Team Killed"

        round_data = filterd_data.drop(
            ["Match ID", "Team", "Player", "Map", "Round Time (ms)", "Operator", "Time Spent Alive (ms)", "Kills",
             "Refrags",
             "Headshots",
             "Underdog Kills", "1vX", "Death", "Traded Death", "Refragged By", "Traded by Enemy", "Opening Kill",
             "Opening Death", "Entry Kill", "Entry Death", "Planted Defuser", "Disabled Defuser", "Teamkills",
             "Teamkilled", "In-game Points", "Unnamed: 31"], axis='columns')

        if filterd_team_data["Player"].values[0] in uc.playerNames:
            op_data = []
            round_op_data = pd.DataFrame([], index=uc.playerNames, columns=["Operator"])
            round_op_data.index.name = "Player"
            for round in list(set(filterd_team_data["Round"].values)):
                test = filterd_team_data.loc[filterd_team_data["Round"] == int(round)]
                for player in uc.playerNames:
                    if player in test["Player"].values:
                        op = test.loc[filterd_team_data["Player"] == player]["Operator"].values[0]
                        round_op_data._set_value(player, "Operator", op)
                    round_op_data = round_op_data.dropna()
                op_data.append(round_op_data)

            round_data["Operatorstats"] = op_data
        return round_data
