import pandas as pd

frame = 'data/2021-02-23_Villa_8-4.csv'

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
        map_overview = dataframe.iloc[:, :-1]
    elif idx == 1:
        match_performance = dataframe.iloc[:, :-1]
    elif idx == 2:
        sixth_pick_overview = dataframe.iloc[:, :-1]
    elif idx == 3:
        player_round_data = dataframe.iloc[:, :-1]
    elif idx == 4:
        round_event_breakdown = dataframe.iloc[:, :-1]


def getplayerindex(playername, match_performance):
    return match_performance.Player[match_performance.Player == playername].index[0]


print(map_overview)
print(match_performance.iloc[match_performance.Player[match_performance.Player == "one.DR"].index[0]])
print(sixth_pick_overview)
print(player_round_data)
print(round_event_breakdown)
