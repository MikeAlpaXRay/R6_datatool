import pandas as pd
import functions as fnc
import time


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

    def addMatch(self, match_overview, player_round_data, user_input):
        mo = match_overview
        if not (mo["Match ID"][0] in self.matches["Match ID"].values):
            gamemode = user_input[0]
            match_info = user_input[1]
            blue_team = user_input[2]
            blue_maps = user_input[3]
            blue_ops = user_input[4]
            orange_team = user_input[5]
            orange_maps = user_input[6]
            orange_ops = user_input[7]

            if mo["Team 1 Score"][0] == mo["Team 2 Score"][0]:
                outcome = "Draw"
            else:
                outcome = mo["Winner"][0]
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
                own_score = max(mo["Team 1 Score"][0], mo["Team 2 Score"][0])
                enemy_score = min(mo["Team 1 Score"][0], mo["Team 2 Score"][0])
            else:
                round_data = self.getRoundData(player_round_data,"Orange")
                banned_maps = orange_maps
                banned_ops = orange_ops
                own_score = min(mo["Team 1 Score"][0], mo["Team 2 Score"][0])
                enemy_score = max(mo["Team 1 Score"][0], mo["Team 2 Score"][0])

            data = [mo["Match ID"][0], mo["Timestamp"][0], gamemode, match_info, banned_maps, banned_ops, mo["Map"][0],
                    outcome, own_score, enemy_score, round_data]
            self.matches = self.matches.append(pd.DataFrame([data], columns=fnc.team_match_columns_names))

        else:
            print("Matchdata already added")
            time.sleep(5)

    def getRoundData(self, player_round_data, Team):
        filterd_data = player_round_data.loc[player_round_data["Team"] == Team]
        filterd_data = filterd_data.loc[filterd_data["Player"] == filterd_data["Player"].values[0]]

        filterd_data["Round"] = pd.to_numeric(filterd_data["Round"], downcast='integer')
        filterd_data = filterd_data.set_index("Round")
        for idx, type in enumerate(filterd_data["Victory Type"].values):
            if type == "Time Limit Reached":
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
             "Teamkilled", "In-game Points"], axis='columns')
        return round_data
