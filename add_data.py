import sys
import pandas as pd
import functions as fnc
import data_structure as ds


def main():
    for frame in sys.argv[1:]:
        csv_frames = fnc.handleCSV(frame)

        match_overview = csv_frames[0]
        match_performance = csv_frames[1]
        sixth_pick_overview = csv_frames[2]
        player_round_data = csv_frames[3]
        round_event_breakdown = csv_frames[4]

        all_players = []
        all_teams = []
        all_names = []
        all_players, all_teams = fnc.loadData()

        for player in all_players:
            all_names.append(player.name)
        for player_name in match_performance.Player.values:
            if not (player_name in all_names):
                all_players.append(ds.Player(player_name))
                all_players[len(all_players)-1].addMatch(player_name, match_overview, match_performance)
            else:
                for player in all_players:
                    if player.name == player_name:
                        player.addMatch(player_name, match_overview, match_performance)
        fnc.saveData(all_players, all_teams)


main()
