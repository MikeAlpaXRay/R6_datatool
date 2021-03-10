import os
import time
import csv
import pandas as pd
import numpy as np
import pickle
from os.path import exists
import user_constants as uc


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
    if exists("data\\player_data.txt") and exists("data\\team_data.txt"):
        x = os.stat("data\\player_data.txt")
        y = os.stat("data\\team_data.txt")
        last_updated = (time.time() - max(x, y).st_mtime)
        if last_updated > uc.DaysToBackup * 24 * 60 * 60:
            old_all_players, old_all_teams = loadData()
            file_pi2 = open("data\\player_data_backup.txt", "wb")
            pickle.dump(old_all_players, file_pi2)
            file_pi2 = open("data\\team_data_backup.txt", "wb")
            pickle.dump(old_all_teams, file_pi2)
            file_pi2 = open("data\\player_data.txt", "wb")
            pickle.dump(all_players, file_pi2)
            file_pi2 = open("data\\team_data.txt", "wb")
            pickle.dump(all_teams, file_pi2)
        else:
            file_pi2 = open("data\\player_data.txt", "wb")
            pickle.dump(all_players, file_pi2)
            file_pi2 = open("data\\team_data.txt", "wb")
            pickle.dump(all_teams, file_pi2)
    else:
        file_pi2 = open("data\\player_data.txt", "wb")
        pickle.dump(all_players, file_pi2)
        file_pi2 = open("data\\team_data.txt", "wb")
        pickle.dump(all_teams, file_pi2)


def handleCSV(frame):
    with open(frame, 'r') as read_obj:
        frame_reader = csv.reader(read_obj)

        indices_no = []
        frame_depth = []
        for idx, row in enumerate(frame_reader):
            for indice in uc.indices:
                if indice in row:
                    indices_no.append(idx)
        indices_no.append(idx)
        frame_depth = [indices_no[n] - indices_no[n - 1] - 3 for n in range(1, len(indices_no))]

        index_frame = pd.DataFrame(list(zip(uc.indices, indices_no, frame_depth)), columns=['Name', 'Index', 'Depth'])

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
    return match_performance.Player[match_performance.Player == playername].index[0]


def getknowndata(all_players, all_teams):
    all_playernames = []
    all_teamnames = []
    used_gamemode = [uc.noMatchInfoMode]
    used_match_info = []
    for player in all_players:
        all_playernames.append(player.name)
    for team in all_teams:
        all_teamnames.append(team.name)
    for team in all_teams:
        used_gamemode.append(team.matches["Gamemode"].values[0])
    used_gamemode = list(set(used_gamemode))
    for team in all_teams:
        used_match_info.append(team.matches["Comp Info"].values[0])
    used_match_info = list(set(used_match_info))
    return all_playernames, all_teamnames, used_gamemode, used_match_info


def getgamemodeinput(used_gamemode):
    gamemode_string = "Enter Gamemode:\n"
    gamemode_string += "Press\t0\tfor new entry\n"
    for idx, gamemode in enumerate(used_gamemode):
        gamemode_string += "Press\t" + str(idx + 1) + "\tfor\t" + str(gamemode) + "\n"

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
    match_info_string = "Enter Matchinfo:\n"
    match_info_string += "Press\t0\tfor new entry\n"
    for idx, match_info in enumerate(used_match_info):
        match_info_string += "Press\t" + str(idx + 1) + "\tfor\t" + str(match_info) + "\n"

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
    if team == "blue":
        team_string = "Enter blue team:\n"
    elif team == "orange":
        team_string = "Enter  orange team:\n"
    team_string += "Press\t0\tfor new entry\n"
    for idx, team_name in enumerate(all_teamnames):
        team_string += "Press\t" + str(idx + 1) + "\tfor\t" + str(team_name) + "\n"
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


def getopbanninput(team):
    if team == "blue":
        op_string = "Blue banned...:\n"
    elif team == "orange":
        op_string = "Orange banned:\n"
    for idx, op_name in enumerate(uc.attOps):
        op_string += "Press\t" + str(idx) + "\tfor\t" + str(op_name)
        if not (len(str(op_name))) > 7:
            op_string += "\t|\t"
        else:
            op_string += "|\t"
        if (idx % 2) == 0:
            op_string += "\n"
    input_valid = False
    while not input_valid:
        ops = input(op_string)
        if ops.isdigit() and int(ops) in range(len(uc.attOps) + 1):
            input_valid = True
            attban = uc.attOps[int(ops)]
        else:
            print("Enter correct number")
    if team == "blue":
        op_string = "\nBlue banned...:\n"
    elif team == "orange":
        op_string = "\nOrange banned:\n"
    for idx, op_name in enumerate(uc.defOps):
        op_string += "Press\t" + str(idx) + "\tfor\t" + str(op_name)
        if not (len(str(op_name))) > 7:
            op_string += "\t|\t"
        else:
            op_string += "|\t"
        if (idx % 2) == 0:
            op_string += "\n"

    input_valid = False
    while not input_valid:
        team = input(op_string)
        if team.isdigit() and int(team) in range(len(uc.defOps) + 1):
            input_valid = True
            defban = uc.defOps[int(team)]
        else:
            print("Enter correct number")

    return [attban, defban]


def getmapbanninput(team, pool="comp"):
    banned_maps = []
    if pool == "comp":
        comp_pool = True
    else:
        comp_pool = False
    if team == "blue":
        team_string = "Blue banned...:\n"
    elif team == "orange":
        team_string = "Orange banned:\n"
    if comp_pool:
        team_string += "Press\t0\tto continue\n"
    else:
        team_string += "Press\t0\tto other maps\n"
    if comp_pool:
        map_pool = uc.compMaps
    else:
        map_pool = uc.nonCompMaps
    for idx, map_name in enumerate(map_pool):
        team_string += "Press\t" + str(idx + 1) + "\tfor\t" + str(map_name) + "\n"
    if pool == "comp":
        team_string += "Press\t" + str(len(map_pool) + 1) + "\tfor\tother mappool\n"

    input_valid = False
    while not input_valid:
        maps = input(team_string)
        if maps.isdigit() and int(maps) in range(len(map_pool) + 2):
            if maps == "0":
                input_valid = True
            elif maps == str(len(map_pool) + 1):
                maps = getmapbanninput(team, pool="nonComp")
                for imap in maps:
                    banned_maps.append(imap)
            else:
                maps = map_pool[int(maps) - 1]
                banned_maps.append(maps)
        else:
            print("Enter correct number")
    input(banned_maps)
    return banned_maps


def getuserinput(frame, knowndata):
    all_teamnames = knowndata[1]
    used_gamemode = knowndata[2]
    used_match_info = knowndata[3]

    gamemode = getgamemodeinput(used_gamemode)
    if not (gamemode == uc.noMatchInfoMode):
        match_info = getmatchinfoinput(used_match_info)
    else:
        match_info = "None"
    blue_team = getteaminput(all_teamnames, "blue")
    orange_team = getteaminput(all_teamnames, "orange")

    if not (gamemode == uc.noMatchInfoMode):
        blue_maps = getmapbanninput("blue", pool="comp")
        orange_maps = getmapbanninput("orange", pool="comp")
    else:
        blue_maps = ""
        orange_maps = ""

    blue_ops = getopbanninput("blue")
    orange_ops = getopbanninput("orange")

    user_input = [gamemode, match_info, blue_team, blue_maps, blue_ops, orange_team, orange_maps, orange_ops]
    return user_input
