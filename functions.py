import pandas as pd
import json


indices = ["MATCH OVERVIEW", "MATCH PERFORMANCE", "SIXTH PICK OVERVIEW", "PLAYER ROUNDS DATA", "ROUND EVENTS BREAKDOWN"]

def loadData():
    all_players = []
    all_teams = []
    with open("data\\player_data.json", 'r') as json_file:
        json_data = json.load(json_file)
        for entry in json_data:
            all_players.append(entry)
    with open("data\\team_data.json", 'r') as json_file:
        json_data = json.load(json_file)
        for entry in json_data:
            all_teams.append(entry)
    return all_players, all_teams


def saveData(all_players, all_teams):
    str_json = json.dumps(all_players, default=lambda o: o.__dict__, indent=4)
    json_file = open("data\\player_data.json", "w+")
    json_file.write(str_json)
    json_file.close()
    str_json = json.dumps(all_teams, default=lambda o: o.__dict__, indent=4)
    json_file = open("data\\team_data.json", "w+")
    json_file.write(str_json)
    json_file.close()


def handleCSV(frame):
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

    print(map_overview)
    print(match_performance)
    print(sixth_pick_overview)
    print(player_round_data)
    print(round_event_breakdown)
    csv_frames = [map_overview, match_performance, sixth_pick_overview, player_round_data, round_event_breakdown]
    return csv_frames

def newPlayerData(all_players, csv_frames):

def newTeamData(all_teams, csv_frames):