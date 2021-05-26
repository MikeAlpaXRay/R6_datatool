import time
import pandas as pd
import functions as fnc


class Player:
    # player object
    def __init__(self, name):
        # name of player
        self.name = name
        # data frame of matches each row represents a match
        self.matches = pd.DataFrame()

    def addMatch(self, playername, match_overview, match_performance, roundoverview):
        # add match data to player matches data frame

        # drop unwanted data
        filterd_overview = match_overview.iloc[0].drop(
            ["Team 1", "Team 2", "Team 1 Score", "Team 2 Score", "ATK at Start", "Team 1 ATK Wins", "Team 1 DEF Wins",
             "Team 2 ATK Wins", "Team 2 DEF Wins", "Team 1 Score at Half", "Team 2 Score at Half"])

        filterd_performance = match_performance.loc[fnc.getplayerindex(playername, match_performance)]
        # drop unwanted data
        filterd_performance = filterd_performance.drop(
            ["Match ID", "Player", "K-D (+/-)", "Entry (+/-)", "Trade Diff", "HS%", "ATK Op", "DEF Op",
             "In-game Points", "Unnamed: 34"])


        round_won = roundoverview["Win Team"].tolist().count(filterd_performance["Team"])
        if round_won > (len(roundoverview["Win Team"]) - round_won):
            filterd_overview["Winner"] = True
        else:
            filterd_overview["Winner"] = False


        # merge wanted data
        filterd_data = pd.concat([filterd_overview, filterd_performance.drop("Team")])
        # check if match already added or first match
        if not self.matches.empty:
            if not (filterd_overview["Match ID"] in self.matches["Match ID"].values):
                self.matches = self.matches.append(filterd_data, ignore_index=True)
        else:
            self.matches = self.matches.append(filterd_data, ignore_index=True)


class Team:
    # team object
    def __init__(self, name):
        # name of player
        self.name = name
        # data frame of matches each row represents a match
        self.matches = pd.DataFrame(columns=fnc.pc.team_match_columns_names)

    def addMatch(self, match_overview, player_round_data, user_input, roundoverview=[]):
        # add match data to team matches data frame
        mo = match_overview
        # check if match already added
        if not (mo["Match ID"].values[0] in self.matches["Match ID"].values):
            gamemode = user_input[0]
            match_info = user_input[1]
            blue_team = user_input[2]
            blue_maps = user_input[3]
            blue_ops = user_input[4]
            orange_team = user_input[5]
            orange_maps = user_input[6]
            orange_ops = user_input[7]


            if self.name == blue_team:
                # add round data
                print("Perspective of " + str(self.name))
                if len(roundoverview) == 0:
                    roundoverview = fnc.getrounddata(player_round_data, "Blue")
                round_data = self.getRoundData(roundoverview, player_round_data, "Blue")
                banned_maps = blue_maps
                banned_ops = blue_ops
            else:
                # add round data
                print("Perspective of " + str(self.name))
                if len(roundoverview) == 0:
                    roundoverview = fnc.getrounddata(player_round_data, "Orange")
                round_data = self.getRoundData(roundoverview, player_round_data, "Orange")
                banned_maps = orange_maps
                banned_ops = orange_ops

            # handle outcome
            results = round_data["Result"].values.tolist()

            own_score = results.count("Win")
            enemy_score = results.count("Loss")

            if own_score > enemy_score:
                outcome = "Win"
            elif own_score < enemy_score:
                outcome = "Lose"
            else:
                outcome = "Draw"




            data = [mo["Match ID"].values[0], mo["Timestamp"].values[0], gamemode, match_info, banned_maps, banned_ops,
                    mo["Map"].values[0], outcome, own_score, enemy_score, round_data]

            self.matches = self.matches.append(pd.DataFrame([data], columns=fnc.pc.team_match_columns_names))

        else:
            print("Matchdata already added")
            time.sleep(3)

        return roundoverview

    def getRoundData(self, roundoverview, player_round_data, team):
        # get round data containing site, outcome
        filterd_team_data = player_round_data.loc[player_round_data["Team"] == team]
        filterd_data = filterd_team_data.loc[filterd_team_data["Player"] == filterd_team_data["Player"].values[0]]
        filterd_data = filterd_data.reset_index(drop=True)

        round_data = roundoverview.copy()
        round_data["Round"] = round_data.index.values


        for index, row in round_data.iterrows():
            # row = row[1]
            if row["Att Team"] == team:
                round_data.loc[index, "Att Team"] = "Attack"
            else:
                round_data.loc[index, "Att Team"] = "Defence"

            if row["Win Team"] == team:
                round_data.loc[index, "Win Team"] = "Win"
            else:
                round_data.loc[index, "Win Team"] = "Loss"
            if "Defuser" in row["Victory Type"]:
                if row["Att Team"] == "Attack":
                    if row["Win Team"] == "Win":
                        round_data.loc[index, "Victory Type"] = "Defuser Planted"
                    else:
                        round_data.loc[index, "Victory Type"] = "Defuser Disabled"
                else:
                    if row["Win Team"] == "Win":
                        round_data.loc[index, "Victory Type"] = "Defuser Disabled"
                    else:
                        round_data.loc[index, "Victory Type"] = "Defuser Planted"

        # op tracking
        if filterd_team_data["Player"].values[0] in fnc.uc.playerNames:
            op_data = []
            for round in round_data["Round"].values:
                round_info = filterd_team_data.loc[filterd_team_data["Round"] == int(round)]
                if round in list(set(filterd_team_data["Round"].values)):
                    round_op_data = pd.DataFrame([], index=fnc.uc.playerNames, columns=["Operator"])
                    round_op_data.index.name = "Player"
                    for player in fnc.uc.playerNames:
                        if player in round_info["Player"].values:
                            op = round_info.loc[filterd_team_data["Player"] == player]["Operator"].values[0]
                            round_op_data._set_value(player, "Operator", op)
                        round_op_data = round_op_data.dropna()
                else:
                    round_op_data = []
                op_data.append(round_op_data)
            round_data["Operatorstats"] = op_data
        column_names = round_data.columns.values
        if len(column_names) == 5:
            round_data.columns = ["Side", "Site", "Result", "Victory Type", "Round"]
        if len(column_names) == 6:
            round_data.columns = ["Side", "Site", "Result", "Victory Type", "Round", "Operatorstats"]
        round_data = round_data.astype({"Round": 'int'}).set_index("Round")
        return round_data


