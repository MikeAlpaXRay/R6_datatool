import pandas as pd
import numpy as np

frame = '2021-02-23_Kafe Dostoyevsky_8-4.csv'

indices = ["MATCH OVERVIEW", "MATCH PERFORMANCE", "SIXTH PICK OVERVIEW", "PLAYER ROUNDS DATA", "ROUND EVENTS BREAKDOWN"]
indices_no = []
frame_depth = []
unfiltered_frame = pd.read_csv(frame, sep=';')
row_count = unfiltered_frame.shape[0]

for row_no in range(0, row_count):
    row_content = unfiltered_frame.iloc[row_no, 0]
    for name in indices:
        if name in row_content:
            indices_no.append(row_no)

for idx, x in enumerate(indices_no):
    indices_no[idx] = x + 2
    if not (idx + 1 == len(indices_no)):
        frame_depth.append(indices_no[idx + 1] - x - 2)
    else:
        frame_depth.append(row_count - x - 2)

indexFrame = pd.DataFrame(list(zip(indices, indices_no, frame_depth)),
                          columns=['Name', 'Index', 'Depth'])

for idx, name in enumerate(indices):
    dataframe = pd.read_csv(frame, sep='\,', header=None, skiprows=indexFrame["Index"][idx],
                            nrows=indexFrame["Depth"][idx],
                            engine='python')
    dataframe = pd.read_csv(frame, sep='\,', header=None, skiprows=indexFrame["Index"][idx] + 1,
                            nrows=indexFrame["Depth"][idx] - 1, engine='python', names=dataframe.iloc[0].values)
    if idx == 0:
        match_overview = dataframe.iloc[:, :-1]
        match_overview = match_overview.loc[:, match_overview.columns.notnull()]
    elif idx == 1:
        match_performance = dataframe.iloc[:, :-1]
        match_performance = match_performance.loc[:, match_performance.columns.notnull()]
    elif idx == 2:
        sixth_pick_overview = dataframe.iloc[:, :-1]
        sixth_pick_overview = sixth_pick_overview.loc[:, sixth_pick_overview.columns.notnull()]
    elif idx == 3:
        player_round_data = dataframe.iloc[:, :-1]
        player_round_data = player_round_data.loc[:, player_round_data.columns.notnull()]
    elif idx == 4:
        round_event_breakdown = dataframe.iloc[:, :-1]
        round_event_breakdown = round_event_breakdown.loc[:, round_event_breakdown.columns.notnull()]


def getplayerindex(playername, match_performance):
    return match_performance.Player[match_performance.Player == playername].index[0]




filterd_data = player_round_data.loc[player_round_data["Team"] == "Blue"]
filterd_data = filterd_data.loc[filterd_data["Player"] == filterd_data["Player"].values[0]]

filterd_data["Round"] = pd.to_numeric(filterd_data["Round"], downcast='integer')
filterd_data = filterd_data.set_index("Round")
for idx, type in enumerate(filterd_data["Victory Type"].values):
    if type == "Time Limit Reached":
        if int(filterd_data["Round Time (ms)"].iloc[idx]) >= 225000:
            filterd_data.loc[idx+1, "Victory Type"] = "Time Limit Reached"
        else:
            filterd_data.loc[idx+1, "Victory Type"] = "Team Killed"

round_data = filterd_data.drop(
    ["Match ID", "Team", "Player", "Map", "Round Time (ms)", "Operator", "Time Spent Alive (ms)", "Kills", "Refrags",
     "Headshots",
     "Underdog Kills", "1vX", "Death", "Traded Death", "Refragged By", "Traded by Enemy", "Opening Kill",
     "Opening Death", "Entry Kill", "Entry Death", "Planted Defuser", "Disabled Defuser", "Teamkills",
     "Teamkilled", "In-game Points"], axis='columns')


filterd_data = player_round_data.loc[player_round_data["Team"] == "Orange"]
print(filterd_data["Player"].values[0])
input(round_data)
# print(sixth_pick_overview)
# print(player_round_data)
# print(round_event_breakdown)
