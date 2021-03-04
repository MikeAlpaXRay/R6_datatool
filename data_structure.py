class Player:
    def __init__(self, alias=[]):
        self.playerid = time.time()
        self.alias = alias
        self.matches = []

    def getName(self):
        return self.alias[len(self.alias) - 1]

    def newAlias(self, new_name):
        self.alias.append(new_name)

    def addMatch(self):
        self.matches.append()


class Playermatch:
    def __init__(self):
        self.date=date
        self.matchid=matchid
        self.mode=mode
        self.map=map
        self.win=win
        self.playerRating=playerRating
        self.ATKRating=ATKRating
        self.DEFRating=DEFRating
        self.KOST=KOST
        self.KPR=KPR
        self.SRV=SRV
        self.kills=kills
        self.headshots=headshots
        self.underdogKills=underdogKills
        self.vX=vX
        self.multikillRounds=multikillRounds
        self.deaths=deaths
        self.tradedDeaths=tradedDeaths
        self.tradedbyEnemy=tradedbyEnemy
        self.openingKills=openingKills
        self.openingDeaths=openingDeaths
        self.entryKills=entryKills
        self.entryDeaths=entryDeaths
        self.plantedDefuser=plantedDefuser
        self.disabledDefuser=disabledDefuser
        self.teamkills=teamkills
        self.teamkilled=teamkilled

class Team():
    def __init__(self):
