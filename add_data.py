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


        all_players, all_teams = fnc.loadData()
        knowndata = fnc.getknowndata(all_players, all_teams)
        all_playernames = knowndata[0]
        all_teamnames = knowndata[1]
        used_gamemode = knowndata[2]
        used_match_info = knowndata[3]
        input_correct = False
        while not(input_correct):
            user_input = fnc.getuserinput(frame, knowndata)
            confirm = input("Input correct?\t confirm by y")
            if confirm == "y":
                input_correct = True

        winner_team = user_input[2]
        loser_team = user_input[5]


        if not (winner_team in all_teamnames):
            all_teams.append(ds.Team(winner_team))
        if not (loser_team in all_teamnames):
            all_teams.append(ds.Team(loser_team))
        for team in all_teams:
            if team.name == winner_team:
                team.addMatch(match_overview, user_input)
            if team.name == loser_team:
                team.addMatch(match_overview, user_input)

        for player_name in match_performance.Player.values:
            if not (player_name in all_playernames):
                all_players.append(ds.Player(player_name))
                all_players[len(all_players) - 1].addMatch(player_name, match_overview, match_performance)
            else:
                for player in all_players:
                    if player.name == player_name:
                        player.addMatch(player_name, match_overview, match_performance)

        fnc.saveData(all_players, all_teams)

main()
