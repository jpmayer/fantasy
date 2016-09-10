import sqlite3
import operator
from conf import *

conn = sqlite3.connect("league.db")
c = conn.cursor()

playerData = 'history'  # breakdown by player data
matchupData = 'matchups'  # breakdown by matchup totals

def getSacko(year):
    "Return League League Sacko Holder for Given Year"
    c.execute('SELECT manager, year, week, winLoss, score FROM {tn} WHERE year = {yr} AND week < 14 ORDER BY manager ASC, year ASC, week ASC'.\
            format(tn=matchupData, yr=year))
    player_matchups = c.fetchall()
    ownerMap = {}
    for game in player_matchups:
        if str(game[0]) in ownerMap:
            if(game[3] == 'loss'):
                ownerMap[str(game[0])] = {
                    'manager': str(game[0]),
                    'count': ownerMap[str(game[0])].get('count') + 0,
                    'score': ownerMap[str(game[0])].get('score') + game[4],
                    'gamesPlayed': ownerMap[str(game[0])].get('gamesPlayed') + 1
                }
            elif(game[3] == 'win'):
                ownerMap[str(game[0])] = {
                    'manager': str(game[0]),
                    'count': ownerMap[str(game[0])].get('count') + 1,
                    'score': ownerMap[str(game[0])].get('score') + game[4],
                    'gamesPlayed': ownerMap[str(game[0])].get('gamesPlayed') + 1
                }
            else:
                ownerMap[str(game[0])] = {
                    'manager': str(game[0]),
                    'count': ownerMap[str(game[0])].get('count') + .5,
                    'score': ownerMap[str(game[0])].get('score') + game[4],
                    'gamesPlayed': ownerMap[str(game[0])].get('gamesPlayed') + 1
                }
        else:
            if(game[3] == 'loss'):
                ownerMap[str(game[0])] = {
                    'manager': str(game[0]),
                    'count': 0,
                    'score': game[4],
                    'gamesPlayed': 1
                }
            elif(game[3] == 'win'):
                ownerMap[str(game[0])] = {
                    'manager': str(game[0]),
                    'count': 1,
                    'score': game[4],
                    'gamesPlayed': 1
                }
            else:
                ownerMap[str(game[0])] = {
                    'manager': str(game[0]),
                    'count': .5,
                    'score': game[4],
                    'gamesPlayed': 1
                }
    sacko = {
        'count': 9999,
        'score': 9999,
        'gamesPlayed': 13
    }
    for owner in ownerMap:
        if ownerMap[owner].get('gamesPlayed') == 13:
            if ownerMap[owner].get('count') < sacko.get('count'):
                sacko = ownerMap[owner]
            elif ownerMap[owner].get('count') == sacko.get('count'):
                if ownerMap[owner].get('score') < sacko.get('score'):
                    sacko = ownerMap[owner]
    return sacko

def getRegularSeasonLeader(year):
    "Return League Regular Season Leader for Given Year"
    c.execute('SELECT manager, year, week, winLoss, score FROM {tn} WHERE year = {yr} AND week < 14 ORDER BY manager ASC, year ASC, week ASC'.\
            format(tn=matchupData, yr=year))
    player_matchups = c.fetchall()
    ownerMap = {}
    for game in player_matchups:
        if str(game[0]) in ownerMap:
            if(game[3] == 'loss'):
                ownerMap[str(game[0])] = {
                    'manager': str(game[0]),
                    'count': ownerMap[str(game[0])].get('count') + 0,
                    'score': ownerMap[str(game[0])].get('score') + game[4],
                    'gamesPlayed': ownerMap[str(game[0])].get('gamesPlayed') + 1
                }
            elif(game[3] == 'win'):
                ownerMap[str(game[0])] = {
                    'manager': str(game[0]),
                    'count': ownerMap[str(game[0])].get('count') + 1,
                    'score': ownerMap[str(game[0])].get('score') + game[4],
                    'gamesPlayed': ownerMap[str(game[0])].get('gamesPlayed') + 1
                }
            else:
                ownerMap[str(game[0])] = {
                    'manager': str(game[0]),
                    'count': ownerMap[str(game[0])].get('count') + .5,
                    'score': ownerMap[str(game[0])].get('score') + game[4],
                    'gamesPlayed': ownerMap[str(game[0])].get('gamesPlayed') + 1
                }
        else:
            if(game[3] == 'loss'):
                ownerMap[str(game[0])] = {
                    'manager': str(game[0]),
                    'count': 0,
                    'score': game[4],
                    'gamesPlayed': 1
                }
            elif(game[3] == 'win'):
                ownerMap[str(game[0])] = {
                    'manager': str(game[0]),
                    'count': 1,
                    'score': game[4],
                    'gamesPlayed': 1
                }
            else:
                ownerMap[str(game[0])] = {
                    'manager': str(game[0]),
                    'count': .5,
                    'score': game[4],
                    'gamesPlayed': 1
                }
    champ = {
        'count': 0,
        'score': 0,
        'gamesPlayed': 13
    }
    for owner in ownerMap:
        if ownerMap[owner].get('gamesPlayed') == 13:
            if ownerMap[owner].get('count') > champ.get('count'):
                champ = ownerMap[owner]
            elif ownerMap[owner].get('count') == champ.get('count'):
                if ownerMap[owner].get('score') > champ.get('score'):
                    champ = ownerMap[owner]
    return champ

def getChampion(year):
    "Return League Champion for Given Year"
    c.execute('SELECT manager, year, week, winLoss, score FROM {tn} WHERE year = {yr} AND week = 16 AND winLoss = "win" ORDER BY manager ASC, year ASC, week ASC'.\
            format(tn=matchupData, yr=year))
    champ = c.fetchone()
    if champ is None:
        return "N/A"
    return champ[0]

def getNumPlayoffAppearences(manager):
    "Return the Number of Playoff Appearences for a given Manager"
    c.execute('SELECT manager, year, week FROM {tn} WHERE manager = "{mn}" AND week > 13 ORDER BY year ASC, week ASC'.\
            format(tn=matchupData, mn=manager))
    playoff_rows = c.fetchall()
    playoffYears = set()
    for playoff_game in playoff_rows:
        playoffYears.add(playoff_game[1])
    return len(playoffYears)

def getRecord(manager):
    "Return League Regular Season Leader for Given Year"
    c.execute('SELECT manager, year, week, winLoss FROM {tn} WHERE manager = "{mn}" ORDER BY year ASC, week ASC'.\
            format(tn=matchupData, mn=manager))
    games = c.fetchall()
    wins = 0
    losses = 0
    ties = 0
    for game in games:
        if game[3] == 'win':
            wins = wins + 1
        elif game[3] == 'loss':
            losses = losses + 1
        else:
            ties = ties + 1
    if wins + losses + ties == 0:
        return (0, 0, 0, 0, manager)
    else:
        return (wins, losses, ties, "%.1f" % ( (wins + .5 * ties ) * 100 / (wins + losses + ties)), manager)

records = []
sackos = []
championships = []
midLine = 0

def generateRecords():
    for manager in managers:
        records.append(getRecord(manager))
    return records.sort(key=lambda tup: tup[3], reverse=True)

def generateSackos():
    for year in yearsCompleted:
        sackos.append(getSacko(year))

def generateChampionships():
    for year in yearsCompleted:
        championships.append(getChampion(year))

generateRecords()
generateSackos()
generateChampionships()

def generateSackoImageString(manager):
    selfSackos = []
    count = 0
    for sacko in sackos:
        sackoManager = sacko.get("manager")
        if sackoManager == manager:
            selfSackos.append(str(firstYear + count))
        count = count + 1
    sackoImageStr = ""
    for sacko in selfSackos:
        sackoImageStr = sackoImageStr + "<img src='https://www.emojibase.com/resources/img/emojis/apple/x1f4a9.png.pagespeed.ic.292Eth5N9Z.png' height='16px' title='" + str(sacko) + "' style='position:relative;top:3px'/>"
    return sackoImageStr

def generateTrophyImageString(manager):
    selfTrophies = []
    count = 0
    for champ in championships:
        if champ == manager:
            selfTrophies.append(str(firstYear + count))
        count = count + 1
    champImageStr = ""
    for champ in selfTrophies:
        champImageStr = champImageStr + "<img src='http://www.tiande-online.ru/uploads/images/00/32/51/2016/01/15/0u45f0ed81-2d657924-26a019f6.png' height='16px' title='" + str(champ) + "' style='position:relative;top:3px'/>"
    return champImageStr

def appendRow(place, acunaRendered, resultString):
    stats = records[place - 1]
    if acunaRendered == 0 and float(stats[3]) < 50.0:
        acunaRendered = acunaRendered + 1
        resultString = resultString + "<tr class='acunaRow' title='The Threshold to Measure How Good Your Team Truly is.'> <td colspan='9' class='acuna'><b>The Acuna Line<b></td></tr>"
    resultString = resultString + "<tr class='row'> <td class='place'>" + str(place) + ". </td><td>" + str(stats[4]) + "</td><td>" + str(stats[0]) + "</td><td>" + str(stats[1]) + "</td><td>" + str(stats[2]) + "</td><td>" + str(stats[3]) + "%</td><td>" + generateTrophyImageString(str(stats[4])) + "</td><td>" + generateSackoImageString(str(stats[4])) + "</td><td>" + str(getNumPlayoffAppearences(str(stats[4]))) + "</td></tr>"
    return (acunaRendered, resultString)



resultString = "<div id='winLeaders'>"
resultString = resultString + "<table class='win-leader-table'>"
resultString = resultString + "<tr><th colspan='9'><h3>All Time Leader Board</h3></th></tr>"
resultString = resultString + "<tr class='leader-header'><td><b>Place</b></td><td><b>Holder</b></td><td><b>Wins</b></td><td><b>Losses</b></td><td><b>Ties</b></td><td><b>Win %</b></td><td><b>Titles</b></td><td><b>Sackos</b></td><td><b>Playoff App.</b></td></tr>"
rowCount = 1
acunaRendered = 0
while rowCount < len(managers) + 1:
    results = appendRow(rowCount, acunaRendered, resultString)
    acunaRendered = results[0]
    resultString = results[1]
    rowCount = rowCount + 1
resultString = resultString + "</table></div>"
resultString = resultString + "<style>"
resultString = resultString + "#winLeaders{position:relative;margin-left:auto;margin-right:auto;}"
resultString = resultString + ".win-leader-table{width:100%;border:0px solid black; font-size:12px;position:relative;text-align:center;}"
resultString = resultString + ".win-leader-table th{width:500px;background-color:#1D7225;color:white;}"
resultString = resultString + ".place{width:40px;padding-left:5px;padding-top:5px}"
resultString = resultString + ".row:nth-child(odd) {background-color:#F2F2E8;}"
resultString = resultString + ".row:nth-child(even) {background-color:#F8F8F2;}"
resultString = resultString + ".leader-header{background-color:#6DBB75;}"
resultString = resultString + ".acunaRow{background-color:#e35e52;}"
resultString = resultString + ".acuna{font-size: 7px;line-height: 7px;color: white;}"
resultString = resultString + "</style>"

print(resultString)

conn.commit()
conn.close()
