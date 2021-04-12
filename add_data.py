import os
import sys
import time
import random
import functions as fnc
import data_structure as ds


def main():
    user = sys.argv[-1]
    for frame in sys.argv[1:-1]:
        # Loop over all csv files
        os.system("cls")
        print("User: " + str(user))
        print("File Path: " + str(frame))
        csv_frames = fnc.handleCSV(frame)

        match_overview = csv_frames[0]
        match_performance = csv_frames[1]
        # sixth_pick_overview = csv_frames[2]
        player_round_data = csv_frames[3]
        # round_event_breakdown = csv_frames[4]

        all_players, all_teams = fnc.loadData()
        knowndata = fnc.getknowndata(all_players, all_teams)
        all_playernames = knowndata[0]
        all_teamnames = knowndata[1]
        used_gamemode = knowndata[2]
        used_match_info = knowndata[3]

        input_correct = False
        user_input = []
        while not input_correct:
            user_input = fnc.getuserinput(frame, knowndata)
            print("\n\nMatchdata: " + str(user_input[0]) + " | Remarks:\t" + str(user_input[1]) + "\n")

            map_string = ""
            for data in user_input[3]:
                map_string += "\t\t\t\t" + str(data) + "\n"
            op_string = ""
            for data in user_input[4]:
                op_string += "\t\t\t\t" + str(data) + "\n"
            print(
                "Team 1: " + str(user_input[2]) + "\n\tBanned:\n\t\tMaps:\n" + map_string + "\n\t\tOps:\n" + op_string)
            map_string = ""
            for data in user_input[6]:
                map_string += "\t\t\t\t" + str(data) + "\n"
            op_string = ""
            for data in user_input[7]:
                op_string += "\t\t\t\t" + str(data) + "\n"
            print(
                "Team 2: " + str(user_input[5]) + "\n\tBanned:\n\t\tMaps:\n" + map_string + "\n\t\tOps:\n" + op_string)
            confirm = input("Input correct?\t Press y to confirm...\n")
            if confirm == "y" or confirm == "Y":
                input_correct = True

        blue_team = user_input[2]
        orange_team = user_input[5]

        if not (blue_team in all_teamnames):
            print("Add new team...")
            all_teams.append(ds.Team(blue_team))
        if not (orange_team in all_teamnames):
            print("Add new team...")
            all_teams.append(ds.Team(orange_team))
        for team in all_teams:
            print("Add team round data...")
            if team.name in [blue_team, orange_team]:
                team.addMatch(match_overview, player_round_data, user_input, user)

        for player_name in match_performance.Player.values:
            if not (player_name in all_playernames):
                print("Add new player match data...")
                all_players.append(ds.Player(player_name))
                all_players[len(all_players) - 1].addMatch(player_name, match_overview, match_performance)
            else:
                for player in all_players:
                    if player.name == player_name:
                        print("Add player match data...")
                        player.addMatch(player_name, match_overview, match_performance)
        fnc.saveData(all_players, all_teams)

        if random.randint(1, 1001) > 999:
            # this ends the progress bar
            toolbar_width = 100
            # setup toolbar
            sys.stdout.write("[%s]" % (" " * toolbar_width))
            sys.stdout.flush()
            sys.stdout.write("\b" * (toolbar_width + 1))  # return to start of line, after '['

            for i in range(toolbar_width):
                time.sleep(1 / random.randint(25, 50))  # do real work here
                # update the bar
                if i == (toolbar_width / 4):
                    sys.stdout.write("TR")
                    sys.stdout.flush()
                elif (3 * toolbar_width / 4) > i > (toolbar_width / 4):
                    sys.stdout.write("OL")
                    sys.stdout.flush()
                else:
                    sys.stdout.write("-")
                    sys.stdout.flush()
            sys.stdout.write("]\n")

        print("File Path: " + str(frame))
        print("Finished")


if __name__ == "__main__":
    main()