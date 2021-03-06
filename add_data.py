import sys
import functions as fnc
import data_structure as ds


def main():
    for frame in sys.argv[1:]:
        input(frame)
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
        while not (input_correct):
            user_input = fnc.getuserinput(frame, knowndata)
            confirm = input("Input correct?\t confirm by y\n")
            if confirm == "y":
                input_correct = True

        blue_team = user_input[2]
        orange_team = user_input[5]

        if not (blue_team in all_teamnames):
            all_teams.append(ds.Team(blue_team))
        if not (orange_team in all_teamnames):
            all_teams.append(ds.Team(orange_team))
        for team in all_teams:
            if team.name in [blue_team, orange_team]:
                team.addMatch(match_overview, player_round_data, user_input)

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
