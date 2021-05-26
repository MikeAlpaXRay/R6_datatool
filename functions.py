import os
import time
import csv
import pathlib
import pickle
import json
import pandas as pd
import numpy as np
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
def getmapbanninput(team_name="", pool="comp", played=False):
    # manage user input regarding map ban

    banned_maps = []
    # set map pool
    if pool == "comp":
        comp_pool = True
    else:
        comp_pool = False
    # generate string
    if not played == True:
        team_string = str(team_name + " banned...:\n")
    else:
        team_string = "Map played...:\n"
    if comp_pool and not played:
        team_string += "Press\t0\tto continue\n"
    else:
        team_string += "Press\t0\tto other maps\n"
    if comp_pool:
        map_pool = loadjsonmapdata(comp=True, key="Name")
    else:
        map_pool = loadjsonmapdata(comp=False, key="Name")
    for idx, map_name in enumerate(map_pool):
        team_string += "Press\t" + str(idx + 1) + "\tfor\t" + str(map_name) + "\n"
    if pool == "comp" and not played:
        team_string += "Press\t" + str(len(map_pool) + 1) + "\tfor\tother mappool\n"

    # user input
    input_valid = False
    if not played:
        list_extend = 2
    else:
        list_extend = 1
    while not input_valid:
        maps = input(team_string)
        if maps.isdigit() and int(maps) in range(len(map_pool) + list_extend):
            if maps == "0":
                if played and pool == "comp":
                    maps = getmapbanninput(team_name, pool="nonComp", played=played)
                else:
                    input_valid = True
            elif maps == str(len(map_pool) + 1):
                maps = getmapbanninput(team_name, pool="nonComp", played=played)
                for imap in maps:
                    banned_maps.append(imap)
            else:
                maps = map_pool[int(maps) - 1]
                banned_maps.append(maps)
        else:
            print("Enter correct number")
        if played and len(banned_maps) == 1:
            input_valid = True

    return banned_maps
def handleuserinput(knowndata):
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

def loadjsonmapdata(comp="", name="", key=""):
    #keys: Name, Comp, Objectives
    data = []
    with open("map_info.json", 'r') as json_file:
        json_data = json.load(json_file)
        for entry in json_data:
            if comp == entry["comp"] or comp == "":
                if len(name) == 0 or entry["name"] == name:
                    map_obj = Map(name=entry["name"], comp=entry["comp"], obj=entry["objectives"])
                    if len(key) == 0:
                        data.append(map_obj)
                    else:
                        data.append(getattr(map_obj, key))

    return data


class Map:
    def __init__(self, name, comp=False, obj=[]):
        self.Name = name
        self.Comp = comp
        self.Objectives = obj


def editrow(row, column_name, map):
    # Att/Def Input
    if column_name == "Att Team":
        if row["Att Team"] == "Blue":
            row["Att Team"] = "Orange"
        else:
            row["Att Team"] = "Blue"

    # Result Input
    if column_name == "Win Team":
        if row["Win Team"] == "Blue":
            row["Win Team"] = "Orange"
        else:
            row["Win Team"] = "Blue"

    # Objectives Input
    if column_name == "Side":
        input_correct = False
        obj_sting = ""
        objectives = loadjsonmapdata(name=map, key="Objectives")[0]
        for i, obj in enumerate(objectives):
            obj_sting += str(int(i + 1)) + "\t" + str(obj) + "\n"
        while not input_correct:
            obj_pick = input("Pick objective: \n" + obj_sting)
            if obj_pick.isdigit() and int(obj_pick) in range(len(objectives) + 1):
                input_correct = True
                row["Side"] = objectives[int(obj_pick) - 1]
            else:
                print("Enter correct number\n")

    # Type Input
    if column_name == "Victory Type":
        input_correct = False
        types = ["Elimination", "Defuser", "Time Limit Reached"]
        type_string = ""
        for i, type in enumerate(types):
            type_string += str(int(i + 1)) + "\t" + str(type) + "\n"
        while not input_correct:
            type_pick = input("Round end by ...\n" + type_string)
            if type_pick.isdigit() and int(type_pick) in range(len(types) + 1):
                input_correct = True
                row["Victory Type"] = types[int(type_pick) - 1]
            else:
                print("Enter correct number\n")


def getrounddata(player_round_data, team):
    perspective = team
    if perspective == "Blue":
        anti_perspective = "Orange"
    else:
        anti_perspective = "Blue"


    filterd_team_data = player_round_data.loc[player_round_data["Team"] == perspective]
    filterd_data = filterd_team_data.loc[filterd_team_data["Player"] == filterd_team_data["Player"].values[0]]
    filterd_data = filterd_data.reset_index(drop=True)

    round_breakdown = pd.DataFrame([], index=range(1, len(filterd_data) + 1), columns=["Round", "Att Team", "Side", "Win Team", "Victory Type"])
    round_breakdown["Round"] = filterd_data["Round"].values
    round_breakdown["Side"] = filterd_data["Site"].values
    round_breakdown["Victory Type"] = filterd_data["Victory Type"].values
    round_breakdown["Att Team"] = filterd_data["Side"].values
    round_breakdown["Win Team"] = filterd_data["Result"].values

    round_breakdown = round_breakdown.set_index('Round')

    for row in round_breakdown.iterrows():
        row = row[1]
        if row["Att Team"] == "Attack":
            row.at["Att Team"] = perspective
        else:
            row.at["Att Team"] = anti_perspective
        if row["Win Team"] == "Win":
            row.at["Win Team"] = perspective
        else:
            row.at["Win Team"] = anti_perspective


    round_input_correct = False
    while not round_input_correct:
        os.system("cls")
        print(round_breakdown)
        print("\n")
        round_input = input("Type \ny if round data is correct or type \nround no to edit or \nedit to add or delete...\n")
        if round_input == "y":
            round_input_correct = True
        elif round_input in "edit":
            round_no = input("Enter round number to add or delete new round\n")
            if round_no.isdigit() and int(round_no) not in round_breakdown.index.values:
                new_row = pd.DataFrame([[int(round_no), "Attacker", "unknown", "Winner", "End"]], columns=["Round", "Att Team", "Side", "Win Team", "Victory Type"])
                new_row = new_row.set_index('Round')
                round_breakdown = round_breakdown.append(new_row).sort_index()
            if round_no.isdigit() and int(round_no) in round_breakdown.index.values:
                print("deleting not yet implemented")
                #todo
        else:
            if round_input.isdigit() and  int(round_input) in range(1, len(round_breakdown) + 1):
                round_count = int(round_input) - 1

                change_string = "Enter number to edit round " + str(round_count + 1) + "\n"
                for i, columns_names in enumerate(round_breakdown.columns.values):
                    change_string += str(int(i + 1)) + "->\t" + str(columns_names) + "\n"
                change_input_correct = False
                while not change_input_correct:
                    change_pick = input(change_string)
                    if change_pick.isdigit() and int(change_pick) in range(1, len(round_breakdown.columns.values) + 3):
                        change_pick = int(change_pick) - 1
                        change_input_correct = True
                        editrow(round_breakdown.iloc[round_count], round_breakdown.columns.values[change_pick], filterd_data["Map"][0])
                    else:
                        print("Enter correct number\n")


            else:
                print("Enter correct input\n")
    return round_breakdown








def handlefileinput(frame):
    filetype = pathlib.Path(frame).suffix

    # print(loadjsonmapdata(comp=True, name="Club House", key="Objectives"))
    if filetype == ".xlsx":
        playedMap = getmapbanninput(played=True)
        csv_frames = [[],[],[],[]]
        match_info = pd.read_excel(frame)
        if not len(match_info["Player"].values) == 10 and not len(match_info["Kills"].values) ==\
                                                              10 and not len(match_info["Deaths"].values) == 10:
            print("Enter all Playerdata")
            exit()
        print("User scoreboard is used...")
        match_id = str(playedMap[0]).lower().replace(" ", "") + "_" + str(time.time()).split(".")[0]
        match_info = match_info.drop(["Scorebord_Userinput"], axis=1)
        match_info["match ID"] = pd.Series([match_id for x in range(len(match_info.index))])
        csv_frames[1] = match_info
        match_performance = []

    else:
        csv_frames = handleCSV(frame)

    #getrounddata(playedMap)
    #input(csv_frames)
    return csv_frames