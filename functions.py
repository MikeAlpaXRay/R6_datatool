import os
import time
import csv
import pickle
import pandas as pd
from os.path import exists
import user_constants as uc
import program_constants as pc


def loadData():
    all_players = []
    all_teams = []
    # absolut path to safe files
    playerpath = str(os.path.dirname(__file__)) + "\\data\\player_data.txt"
    teampath = str(os.path.dirname(__file__)) + "\\data\\team_data.txt"
    # without safe file dont load data
    if exists(playerpath):
        file_pi2 = open(playerpath, 'rb')
        all_players = pickle.load(file_pi2)
    if exists(teampath):
        file_pi2 = open(teampath, 'rb')
        all_teams = pickle.load(file_pi2)

    return all_players, all_teams


def saveData(all_players, all_teams):
    # absolut path to safe files
    playerpath = str(os.path.dirname(__file__)) + "\\data\\player_data.txt"
    teampath = str(os.path.dirname(__file__)) + "\\data\\team_data.txt"
    playerpath_backup = str(os.path.dirname(__file__)) + "\\data\\player_data_backup.txt"
    teampath_backup = str(os.path.dirname(__file__)) + "\\data\\team_data_backup.txt"
    if exists(playerpath) and exists(teampath):
        # if data exist check last changed date
        x = os.stat(playerpath)
        y = os.stat(teampath)
        last_updated = (time.time() - max(x, y).st_mtime)
        if last_updated > uc.DaysToBackup * 24 * 60 * 60:
            # create backup
            print("Last input was longer then " + str(uc.DaysToBackup) + " days in the past. Creating backup")
            old_all_players, old_all_teams = loadData()
            file_pi2 = open(playerpath_backup, "wb")
            pickle.dump(old_all_players, file_pi2)
            file_pi2 = open(teampath_backup, "wb")
            pickle.dump(old_all_teams, file_pi2)
    # update data files
    file_pi2 = open(playerpath, "wb")
    pickle.dump(all_players, file_pi2)
    file_pi2 = open(teampath, "wb")
    pickle.dump(all_teams, file_pi2)


def handleCSV(frame):
    # Separate csv file into separate pandas dataframes
    with open(frame, 'r') as read_obj:
        frame_reader = csv.reader(read_obj)

        # Find indices and row count of sub tables and fill index_frame
        indices_no = []
        for idx, row in enumerate(frame_reader):
            for indice in pc.indices:
                if indice in row:
                    indices_no.append(idx)
        indices_no.append(idx)
        frame_depth = [indices_no[n] - indices_no[n - 1] - 3 for n in range(1, len(indices_no))]

        index_frame = pd.DataFrame(list(zip(pc.indices, indices_no, frame_depth)), columns=['Name', 'Index', 'Depth'])

    # Write sub tables to own dataframes
    for idx, name in enumerate(index_frame.Name.values):
        if idx == 0:
            match_overview = pd.read_csv(frame, index_col=0, sep='\,', header=index_frame["Index"][idx], skiprows=1,
                                         nrows=index_frame["Depth"][idx], engine='python')
        elif idx == 1:
            match_performance = pd.read_csv(frame, index_col=0, sep='\,', header=index_frame["Index"][idx], skiprows=1,
                                            nrows=index_frame["Depth"][idx], engine='python')
        elif idx == 2:
            sixth_pick_overview = pd.read_csv(frame, index_col=0, sep='\,', header=index_frame["Index"][idx],
                                              skiprows=1,
                                              nrows=index_frame["Depth"][idx], engine='python')
        elif idx == 3:
            player_round_data = pd.read_csv(frame, index_col=0, sep='\,', header=index_frame["Index"][idx], skiprows=1,
                                            nrows=index_frame["Depth"][idx], engine='python')
        elif idx == 4:
            round_event_breakdown = pd.read_csv(frame, index_col=0, sep='\,', header=index_frame["Index"][idx],
                                                skiprows=1,
                                                nrows=index_frame["Depth"][idx], engine='python')

    csv_frames = [match_overview, match_performance, sixth_pick_overview, player_round_data, round_event_breakdown]

    return csv_frames


def getplayerindex(playername, match_performance):
    # get index of playername in match performance sub table
    return match_performance.Player[match_performance.Player == playername].index[0]


def getknowndata(all_players, all_teams):
    # load know user input from saved data
    all_playernames = []
    all_teamnames = []
    used_gamemode = [uc.noMatchInfoMode]
    used_mode_info = []
    # get known player names
    for player in all_players:
        all_playernames.append(player.name)
    # get known team names
    for team in all_teams:
        all_teamnames.append(team.name)
    # get known game mode
    for team in all_teams:
        used_gamemode.append(team.matches["Gamemode"].values[0])
    used_gamemode = list(set(used_gamemode))
    # get knowwn game mode info
    for team in all_teams:
        used_mode_info.append(team.matches["Comp Info"].values[0])
    used_mode_info = list(set(used_mode_info))

    return all_playernames, all_teamnames, used_gamemode, used_mode_info


def getgamemodeinput(used_gamemode):
    # manage user input regarding game mode

    # generate string
    gamemode_string = "Enter Gamemode:\n"
    gamemode_string += "Press\t0\tfor new entry\n"
    for idx, gamemode in enumerate(used_gamemode):
        gamemode_string += "Press\t" + str(idx + 1) + "\tfor\t" + str(gamemode) + "\n"

    # user input
    input_valid = False
    while not input_valid:
        gamemode = input(gamemode_string)
        if gamemode.isdigit() and int(gamemode) in range(len(used_gamemode) + 1):
            input_valid = True
            if gamemode == "0":
                gamemode = input("New gamemode...\n")
            else:
                gamemode = used_gamemode[int(gamemode) - 1]
        else:
            print("Enter correct number")

    return gamemode


def getmatchinfoinput(used_match_info):
    # manage user input regarding game mode info

    # generate string
    match_info_string = "Enter Matchinfo:\n"
    match_info_string += "Press\t0\tfor new entry\n"
    for idx, match_info in enumerate(used_match_info):
        match_info_string += "Press\t" + str(idx + 1) + "\tfor\t" + str(match_info) + "\n"

    # user input
    input_valid = False
    while not input_valid:
        match_info = input(match_info_string)
        if match_info.isdigit() and int(match_info) in range(len(used_match_info) + 1):
            input_valid = True
            if match_info == "0":
                match_info = input("New matchinfo...\n")
            else:
                match_info = used_match_info[int(match_info) - 1]
        else:
            print("Enter correct number")
    return match_info


def getteaminput(all_teamnames, team):
    # manage user input regarding team names

    # generate string
    if team == "blue":
        team_string = "Enter blue team:\n"
    elif team == "orange":
        team_string = "Enter  orange team:\n"
    team_string += "Press\t0\tfor new entry\n"
    for idx, team_name in enumerate(all_teamnames):
        team_string += "Press\t" + str(idx + 1) + "\tfor\t" + str(team_name) + "\n"

    # user input
    input_valid = False
    while not input_valid:
        team = input(team_string)
        if team.isdigit() and int(team) in range(len(all_teamnames) + 1):
            input_valid = True
            if team == "0":
                team = input("New team...\n")
            else:
                team = all_teamnames[int(team) - 1]
        else:
            print("Enter correct number")

    return team


def getopbanninput(team_name):
    # manage user input regarding operator ban

    # attacker operator
    # generate string
    op_string = str(team_name + " banned attacker op...:\n")
    for idx, op_name in enumerate(pc.attOps):
        op_string += "Press\t" + str(idx) + "\tfor\t" + str(op_name)
        if not (len(str(op_name))) > 7:
            op_string += "\t|\t"
        else:
            op_string += "|\t"
        if (idx % 2) == 0:
            op_string += "\n"

    # user input
    input_valid = False
    while not input_valid:
        ops = input(op_string)
        if ops.isdigit() and int(ops) in range(len(pc.attOps) + 1):
            input_valid = True
            attban = pc.attOps[int(ops)]
        else:
            print("Enter correct number")

    # defender operator
    # generate string
    op_string = str(team_name + " banned defender op...:\n")
    for idx, op_name in enumerate(pc.defOps):
        op_string += "Press\t" + str(idx) + "\tfor\t" + str(op_name)
        if not (len(str(op_name))) > 7:
            op_string += "\t|\t"
        else:
            op_string += "|\t"
        if (idx % 2) == 0:
            op_string += "\n"

    # user input
    input_valid = False
    while not input_valid:
        team = input(op_string)
        if team.isdigit() and int(team) in range(len(pc.defOps) + 1):
            input_valid = True
            defban = pc.defOps[int(team)]
        else:
            print("Enter correct number")

    return [attban, defban]


def getmapbanninput(team_name, pool="comp"):
    # manage user input regarding map ban

    banned_maps = []
    # set map pool
    if pool == "comp":
        comp_pool = True
    else:
        comp_pool = False
    # generate string
    team_string = str(team_name + " banned...:\n")
    if comp_pool:
        team_string += "Press\t0\tto continue\n"
    else:
        team_string += "Press\t0\tto other maps\n"
    if comp_pool:
        map_pool = pc.compMaps
    else:
        map_pool = pc.nonCompMaps
    for idx, map_name in enumerate(map_pool):
        team_string += "Press\t" + str(idx + 1) + "\tfor\t" + str(map_name) + "\n"
    if pool == "comp":
        team_string += "Press\t" + str(len(map_pool) + 1) + "\tfor\tother mappool\n"

    # user input
    input_valid = False
    while not input_valid:
        maps = input(team_string)
        if maps.isdigit() and int(maps) in range(len(map_pool) + 2):
            if maps == "0":
                input_valid = True
            elif maps == str(len(map_pool) + 1):
                maps = getmapbanninput(team_name, pool="nonComp")
                for imap in maps:
                    banned_maps.append(imap)
            else:
                maps = map_pool[int(maps) - 1]
                banned_maps.append(maps)
        else:
            print("Enter correct number")
    return banned_maps


def getuserinput(frame, knowndata):
    # manage all user input

    # get already knwon data
    all_teamnames = knowndata[1]
    used_gamemode = knowndata[2]
    used_match_info = knowndata[3]

    # game mode input
    gamemode = getgamemodeinput(used_gamemode)
    if not (gamemode == uc.noMatchInfoMode):
        # match info input
        match_info = getmatchinfoinput(used_match_info)
    else:
        match_info = "None"

    # team name input
    blue_team = getteaminput(all_teamnames, "blue")
    orange_team = getteaminput(all_teamnames, "orange")
    os.system("cls")

    # map ban input
    if not (gamemode == uc.noMatchInfoMode):
        blue_maps = getmapbanninput(blue_team, pool="comp")
        os.system("cls")
        orange_maps = getmapbanninput(orange_team, pool="comp")
        os.system("cls")
    else:
        blue_maps = ""
        orange_maps = ""

    # map op input
    blue_ops = getopbanninput(blue_team)
    os.system("cls")
    orange_ops = getopbanninput(orange_team)
    os.system("cls")

    user_input = [gamemode, match_info, blue_team, blue_maps, blue_ops, orange_team, orange_maps, orange_ops]

    return user_input
