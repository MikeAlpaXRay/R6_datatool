import pandas as pd
import pickle
from os.path import exists


def loadData():
    all_players = []
    all_teams = []

    if exists("data\\player_data.txt"):
        file_pi2 = open("data\\player_data.txt", 'rb')
        all_players = pickle.load(file_pi2)
    if exists("data\\team_data.txt"):
        file_pi2 = open("data\\team_data.txt", 'rb')
        all_teams = pickle.load(file_pi2)
    return all_players, all_teams


def saveData(all_players, all_teams):
    file_pi2 = open("data\\player_data.txt", "wb")
    pickle.dump(all_players, file_pi2)
    file_pi2 = open("data\\team_data.txt", "wb")
    pickle.dump(all_teams, file_pi2)


def handleCSV(frame):
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
            map_overview = map_overview.loc[:, map_overview.columns.notnull()]
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

    csv_frames = [map_overview, match_performance, sixth_pick_overview, player_round_data, round_event_breakdown]
    return csv_frames
