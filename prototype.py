import pandas as pd
import numpy as np
import csv

# frame = '2021-02-23_Kafe Dostoyevsky_8-4.csv'
frame = '2021-02-23_Villa_8-4.csv'

indices = ["MATCH OVERVIEW", "MATCH PERFORMANCE", "SIXTH PICK OVERVIEW", "PLAYER ROUNDS DATA", "ROUND EVENTS BREAKDOWN"]
indices_no = []
frame_depth = []

with open(frame, 'r') as read_obj:
    frame_reader = csv.reader(read_obj)

    indices_no = []
    frame_depth = []
    for idx, row in enumerate(frame_reader):
        for indice in indices:
            if indice in row:
                indices_no.append(idx)
    indices_no.append(idx)
    frame_depth = [indices_no[n] - indices_no[n - 1] - 3 for n in range(1, len(indices_no))]

    indexFrame = pd.DataFrame(list(zip(indices, indices_no, frame_depth)), columns=['Name', 'Index', 'Depth'])

input(indexFrame)
for idx, name in enumerate(indexFrame.Name.values):
    print(name)
    print(pd.read_csv(frame, index_col=0, sep='\,', header=indexFrame["Index"][idx], skiprows=1,
                      nrows=indexFrame["Depth"][idx], engine='python'))
    if idx == 0:
        match_overview = pd.read_csv(frame, index_col=0, sep='\,', header=indexFrame["Index"][idx], skiprows=1,
                                     nrows=indexFrame["Depth"][idx], engine='python')
    elif idx == 1:
        match_performance = pd.read_csv(frame, index_col=0, sep='\,', header=indexFrame["Index"][idx], skiprows=1,
                                        nrows=indexFrame["Depth"][idx], engine='python')
    elif idx == 2:
        sixth_pick_overview = pd.read_csv(frame, index_col=0, sep='\,', header=indexFrame["Index"][idx], skiprows=1,
                                          nrows=indexFrame["Depth"][idx], engine='python')
    elif idx == 3:
        player_round_data = pd.read_csv(frame, index_col=0, sep='\,', header=indexFrame["Index"][idx], skiprows=1,
                                        nrows=indexFrame["Depth"][idx], engine='python')
    elif idx == 4:
        round_event_breakdown = pd.read_csv(frame, index_col=0, sep='\,', header=indexFrame["Index"][idx], skiprows=1,
                                            nrows=indexFrame["Depth"][idx], engine='python')


def getplayerindex(playername, match_performance):
    return match_performance.Player[match_performance.Player == playername].index[0]


filterd_data = player_round_data.loc[player_round_data["Team"] == "Orange"]
filterd_data = filterd_data.loc[filterd_data["Player"] == filterd_data["Player"].values[0]]

filterd_data["Round"] = pd.to_numeric(filterd_data["Round"], downcast='integer')
filterd_data = filterd_data.set_index("Round")
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



playerNames = ["Crowdsurfr.NGNS", "Jojo.NGNS", "memez.NGNS", "MikeAlpaX.NGNS", "Montezuma.NGNS", "Pran.NGNS",
               "ttheo.NGNS", "Yplaing.NGNS"]



filterd_data = player_round_data.loc[player_round_data["Team"] == "Orange"]
test_frame = pd.DataFrame([], index=playerNames, columns=["Operator"])
test_frame.index.name = "Player"
filterd_data = player_round_data.loc[player_round_data["Team"] == "Orange"]
if filterd_data["Player"].values[0] in playerNames:
    for round in filterd_data["Round"].values:
        test = filterd_data.loc[filterd_data["Round"] == int(round)]
        for player in playerNames:
            if player in test["Player"].values:
                op = test.loc[filterd_data["Player"] == player]["Operator"].values[0]
                test_frame._set_value(player, "Operator", op)
        test_frame = test_frame.dropna()
        print(round)
        input(test_frame)

input("doof")


filterd_data["Round"] = pd.to_numeric(filterd_data["Round"], downcast='integer')
filterd_data = filterd_data.set_index("Round")
for idx, type in enumerate(filterd_data["Victory Type"].values):
    if type == "Time Limit Reached":
        if int(filterd_data["Round Time (ms)"].iloc[idx]) >= 225000:
            filterd_data.loc[idx + 1, "Victory Type"] = "Time Limit Reached"
        else:
            filterd_data.loc[idx + 1, "Victory Type"] = "Team Killed"

round_data = filterd_data.drop(
    ["Match ID", "Team", "Player", "Map", "Round Time (ms)", "Operator", "Time Spent Alive (ms)", "Kills", "Refrags",
     "Headshots",
     "Underdog Kills", "1vX", "Death", "Traded Death", "Refragged By", "Traded by Enemy", "Opening Kill",
     "Opening Death", "Entry Kill", "Entry Death", "Planted Defuser", "Disabled Defuser", "Teamkills",
     "Teamkilled", "In-game Points"], axis='columns')

filterd_data = player_round_data.loc[player_round_data["Team"] == "Orange"]
#print(filterd_data["Player"].values[0])
#input(round_data)
# print(sixth_pick_overview)
# print(player_round_data)
# print(round_event_breakdown)
