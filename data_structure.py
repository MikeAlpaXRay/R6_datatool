import time






class Player:
    def __init__(self, name):
        self.alias = self.newAlias(name)
        self.matches = []

    def getName(self):
        return self.alias[len(self.alias) - 1]

    def newAlias(self, new_name):
        self.alias.append(new_name)

    def addMatch(self):
        self.matches.append(Playermatch[self.getName()])


class Playermatch:
    def __init__(self, playermatchstats):
        self.matchid=playermatchstats[""]
        self.date=playermatchstats[""]
        self.mode=playermatchstats[""]
        self.map=playermatchstats[""]
        self.win=playermatchstats[""]
        self.playerRating=playermatchstats[""]
        self.ATKRating=playermatchstats[""]
        self.DEFRating=playermatchstats[""]
        self.KOST=playermatchstats[""]
        self.KPR=playermatchstats[""]
        self.SRV=playermatchstats[""]
        self.kills=playermatchstats[""]
        self.headshots=playermatchstats[""]
        self.underdogKills=playermatchstats[""]
        self.vX=playermatchstats[""]
        self.multikillRounds=playermatchstats[""]
        self.deaths=playermatchstats[""]
        self.tradedDeaths=playermatchstats[""]
        self.tradedbyEnemy=playermatchstats[""]
        self.openingKills=playermatchstats[""]
        self.openingDeaths=playermatchstats[""]
        self.entryKills=playermatchstats[""]
        self.entryDeaths=playermatchstats[""]
        self.plantedDefuser=playermatchstats[""]
        self.disabledDefuser=playermatchstats[""]
        self.teamkills=playermatchstats[""]
        self.teamkilled=playermatchstats[""]



class Team:
    def __init__(self, name):
        self.name=name
        self.teammatch=[]

    def addMatch(self):
        self.teammatch.append()


class Teammatch:
    def __init__(self):
        self.matchID = matchid
        self.mode = mode
        self.map = played_map
        self.team


