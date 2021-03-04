import sys
import pandas as pd
import functions as fnc

for frame in sys.argv[1:]:
    csv_frames = fnc.handleCSV(frame)

    match_overview = csv_frames[0]
    match_performance = csv_frames[1]
    sixth_pick_overview = csv_frames[2]
    player_round_data = csv_frames[3]
    round_event_breakdown = csv_frames[4]

    all_players, all_teams = fnc.loadData()
    fnc.newPlayerData(all_players, csv_frames)
    fnc.newTeamData(all_teams, csv_frames)
