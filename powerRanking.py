import sqlite3
import operator
import sys
from conf import *

conn = sqlite3.connect("league.db")
c = conn.cursor()

playerData = 'history'  # breakdown by player data
matchupData = 'matchups'  # breakdown by matchup totals
rankingData = 'rankings'  # power ranking history table

# For when using the prompt to form the rankings, array to keep track of which managers have already been placed in the rankings (used for validation)
usedManagers = []

orderedManager = []
orderedDescriptions = []

def validateManager(manager):
    if manager in usedManagers:
        print("Manager already in position " + str(usedManagers.index(manager) + 1))
        return 0
    elif manager not in managers:
        print("Manager name not valid")
        return 0
    else:
        usedManagers.append(manager)
        return 1

def getPlaceString(position):
    if position == 0:
        return "first"
    elif position == 1:
        return "second"
    elif position == 2:
        return "third"
    elif position == 3:
        return "fourth"
    elif position == 4:
        return "fifth"
    elif position == 5:
        return "sixth"
    elif position == 6:
        return "seventh"
    elif position == 7:
        return "eigth"
    elif position == 8:
        return "ninth"
    elif position == 9:
        return "tenth"
    elif position == 10:
        return "eleventh"
    elif position == 11:
        return "twelth"
    elif position == 12:
        return "thirteenth"
    elif position == 13:
        return "fourteenth"
    elif position == 14:
        return "fifteenth"
    elif position == 15:
        return "sixteenth"
    else:
        return "you should probably go ahead and add more cases for your huge ass league"

if len(sys.argv) == 1:
    for num in range(0, len(managers)):
        orderedManager.append(raw_input("Who is " + getPlaceString(num) + "? "))
        while validateManager(orderedManager[num]) == 0:
            orderedManager[num] = raw_input("Who is " + getPlaceString(num) + "? ")
        orderedDescriptions.append(raw_input("Give Description: "))

elif len(sys.argv) == 2:
    lines = [line.rstrip('\n') for line in open(sys.argv[1])]
    lineCount = 0
    for line in lines:
        if lineCount % 2 == 0:
            orderedManager.append(line.strip())
        else:
            orderedDescriptions.append(line.strip())
        lineCount = lineCount + 1

def getRecord(manager):
    "Return Win Loss Ties for a Given Manager this year"
    c.execute('SELECT manager, year, week, winLoss FROM {tn} WHERE manager = "{mn}" AND year = "2016" ORDER BY year ASC, week ASC'.\
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
    return (wins, losses, ties)

def getLastWeekPosition(manager):
    "Return previous Power Ranking position for a given manager"
    if week == "Preseason":
        return getLastYearPosition(manager);
    else:
        previousWeek = int(week) - 1
        c.execute('SELECT ranking FROM {tn} WHERE manager = "{mn}" AND year = "2016" AND week = "{wk}"'.\
                format(tn=rankingData, mn=manager, wk=previousWeek))
        prevRanking = c.fetchone()
        if prevRanking is not None:
            return prevRanking[0]
        else:
            return 0

def getLastWeekPositionString(position):
    if week == "Preseason":
        return position
    elif position == 0:
        return "Last Week: "
    else:
        return "Last Week: " + str(position)

def getManager(position):
    return orderedManager[position - 1]

def getDescription(position):
    return orderedDescriptions[position - 1]

def getDeltaSymbolClass(delta):
    if delta < 0:
        return "up"
    elif delta > 0:
        return "down"
    else:
        return "no-change"

def getDeltaClass(delta):
    if delta < 0:
        return "delta-up"
    elif delta > 0:
        return "delta-down"
    else:
        return ""

def getDeltaString(delta):
    if delta > 0:
        return str(delta)
    elif delta < 0:
        return str(-delta)
    else:
        return "--"

def appendPosition(position, resultString):
    manager = getManager(position)
    record = getRecord(manager)
    recordString = str(record[0]) + "-" + str(record[1]) if record[2] == 0 else str(record[0]) + "-" + str(record[1]) + "-" + str(record[2])
    lastWeekPosition = getLastWeekPosition(manager)
    lastWeekPositionString = getLastWeekPositionString(lastWeekPosition)
    if week == "Preseason":
        delta = 0
    elif lastWeekPosition == 0:
        delta = 0
    else:
        delta = position - lastWeekPosition
    resultString = resultString + "<tr class='rank'> <td><div class='ranking'>" + str(position) + "</div></td><td class='teamPicture'><img src='" + getPicture(manager) + "'></img></td><td><div class='team-name'><a href='" + getClubHouseLink(manager) + "'>" + getShortenedName(manager) + "</a></div><div class='team-record'>" + recordString + "</div></td><td class='center'><div><div class='" + getDeltaSymbolClass(delta) + "'></div><div class='delta " + getDeltaClass(delta) + "'>" + getDeltaString(delta) + "</div></div><div class='last-weeks-position'>" + lastWeekPositionString + "</div></td><td class='center'>" + getDescription(position)+ "</td></tr>"
    return resultString

def printTitle(week):
    if isinstance(week, str):
        return week
    else:
        return "Week " + str(week)

print("")
print("")
print("")

resultString = "<div id='powerRanking'>"
resultString = resultString + "<table>"
resultString = resultString + "<tr> <th colspan='5'><h3>2016 Power Ranking: " + printTitle(week) + "</h3></th> </tr>"
resultString = resultString + "<tr> <td class='center'><b>Rank</b></td><td colspan='2' class='center'><b>Team / Record</b></td><td class='center'><b>Trending</b></td><td class='center'><b>Comments</b></td></tr>"
rowCount = 1
while rowCount <= len(managers):
    resultString = appendPosition(rowCount, resultString)
    rowCount = rowCount + 1
resultString = resultString + "</table></div>"
resultString = resultString + "<style>"
resultString = resultString + "#powerRanking {"
resultString = resultString + "  width:100%;"
resultString = resultString + "  position:relative;"
resultString = resultString + "  margin-left:auto;"
resultString = resultString + "  margin-right:auto;"
resultString = resultString + "  border: 1px solid white;"
resultString = resultString + "  border-radius: 3px;"
resultString = resultString + "}"
resultString = resultString + "#powerRanking table {"
resultString = resultString + "  border:0px solid black;"
resultString = resultString + "  font-size:12px;"
resultString = resultString + "  width:100%;"
resultString = resultString + "  border-collapse: collapse;"
resultString = resultString + "}"
resultString = resultString + "#powerRanking table tr {"
resultString = resultString + "  background-color:#F8F8F2;"
resultString = resultString + "}"
resultString = resultString + "#powerRanking table tr:nth-child(odd){"
resultString = resultString + "  background-color:#F2F2E8;"
resultString = resultString + "}"
resultString = resultString + "#powerRanking table tr:nth-child(2) {"
resultString = resultString + "  background-color:#6DBB75;"
resultString = resultString + "}"
resultString = resultString + "#powerRanking table tr:first-child {"
resultString = resultString + "  width:500px;"
resultString = resultString + "  background-color:#1D7225;"
resultString = resultString + "  color:white;"
resultString = resultString + "  text-align:center;"
resultString = resultString + "}"
resultString = resultString + "th {"
resultString = resultString + "  border-radius: 3px 3px 0px 0px;"
resultString = resultString + "}"
resultString = resultString + "tr.rank {"
resultString = resultString + "  height: 60px;"
resultString = resultString + "  vertical-align: middle;"
resultString = resultString + "}"
resultString = resultString + "tr.rank td:first-child {"
resultString = resultString + "  font-size: 20px;"
resultString = resultString + "  text-align: center;"
resultString = resultString + "  vertical-align: middle;"
resultString = resultString + "  width: 10%;"
resultString = resultString + "}"
resultString = resultString + ".ranking {"
resultString = resultString + "  border-radius: 50px;"
resultString = resultString + "  color: white;"
resultString = resultString + "  padding: 0px;"
resultString = resultString + "  margin: auto;"
resultString = resultString + "}"
circleWidth = 50
circleCount = 0
circleMid = len(managers) / 2
cicleChild = 3
for manager in managers:
    backgroundColor = "#1D7225;" if circleCount < circleMid else "firebrick;"
    resultString = resultString + "tr.rank:nth-child(" + str(cicleChild) + ") .ranking {"
    resultString = resultString + "  background: " + backgroundColor
    resultString = resultString + "  width: " + str(circleWidth) + "px;"
    resultString = resultString + "  height: " + str(circleWidth) + "px;"
    resultString = resultString + "  line-height: " + str(circleWidth) + "px;"
    resultString = resultString + "}"
    if circleCount == circleMid - 1:
        circleWidth = circleWidth
    elif circleCount < circleMid:
        circleWidth = circleWidth - 5
    else:
        circleWidth = circleWidth + 5
    circleCount = circleCount + 1
    cicleChild = cicleChild + 1
resultString = resultString + "tr.rank td:nth-child(2) {"
resultString = resultString + "  width: 10%;"
resultString = resultString + "  vertical-align:middle;"
resultString = resultString + "}"
resultString = resultString + "tr.rank td:nth-child(3) {"
resultString = resultString + "  width: 10%;"
resultString = resultString + "  vertical-align: middle;"
resultString = resultString + "}"
resultString = resultString + "tr.rank td:nth-child(4) {"
resultString = resultString + "  width: 15%;"
resultString = resultString + "  vertical-align: middle;"
resultString = resultString + "}"
resultString = resultString + "tr.rank td:nth-child(5) {"
resultString = resultString + "  width: 55%;"
resultString = resultString + "  vertical-align: middle;"
resultString = resultString + "  font-size: 10px;"
resultString = resultString + "}"
resultString = resultString + ".teamPicture img{"
resultString = resultString + "  position: relative;"
resultString = resultString + "  left: 7px;"
resultString = resultString + "  height: 55px;"
resultString = resultString + "  vertical-align: middle;"
resultString = resultString + "}"
resultString = resultString + ".team-name {"
resultString = resultString + "  font-size: 14px;"
resultString = resultString + "}"
resultString = resultString + ".team-name a {"
resultString = resultString + "  text-decoration: none !important;"
resultString = resultString + "  color: #225DB7 !important;"
resultString = resultString + "}"
resultString = resultString + ".team-record {"
resultString = resultString + "  color: #888;"
resultString = resultString + "}"
resultString = resultString + ".up {"
resultString = resultString + "  border-bottom: 8px solid green;"
resultString = resultString + "  border-left: 4px solid transparent;"
resultString = resultString + "  border-right: 4px solid transparent;"
resultString = resultString + "  width: 0px;"
resultString = resultString + "  position: relative;"
resultString = resultString + "  left: 17px;"
resultString = resultString + "  top: 6px;"
resultString = resultString + "}"
resultString = resultString + ".down {"
resultString = resultString + "  border-top: 8px solid red;"
resultString = resultString + "  border-left: 4px solid transparent;"
resultString = resultString + "  border-right: 4px solid transparent;"
resultString = resultString + "  width: 0px;"
resultString = resultString + "  position: relative;"
resultString = resultString + "  top: 7px;"
resultString = resultString + "  left: 17px;"
resultString = resultString + "}"
resultString = resultString + ".no-change {"
resultString = resultString + "  border-top: 8px solid transparent;"
resultString = resultString + "  border-left: 4px solid transparent;"
resultString = resultString + "  border-right: 4px solid transparent;"
resultString = resultString + "}"
resultString = resultString + ".delta {"
resultString = resultString + "  width: 20px;"
resultString = resultString + "  position: relative;"
resultString = resultString + "  font-size: 17px;"
resultString = resultString + "  line-height: 20px;"
resultString = resultString + "  top: -9px;"
resultString = resultString + "  left: 26px;"
resultString = resultString + "}"
resultString = resultString + ".delta-up {"
resultString = resultString + "  color: green;"
resultString = resultString + "}"
resultString = resultString + ".delta-down {"
resultString = resultString + "  color: red;"
resultString = resultString + "}"
resultString = resultString + ".last-weeks-position {"
resultString = resultString + "  color: #888;"
resultString = resultString + "  font-size: 10px;"
resultString = resultString + "  top: -5px;"
resultString = resultString + "  position: relative;"
resultString = resultString + "}"
resultString = resultString + ".center{"
resultString = resultString + "  text-align:center;"
resultString = resultString + "}"
resultString = resultString + "</style>"

print(resultString)

print("")
print("")
print("")

#SQL Insert statements to keep track of power rankings / show trends
weekString = "0" if isinstance(week, str) else str(week)
sqlCount = 1
for manager in managers:
    print('INSERT INTO rankings (manager, week, year, ranking, description) VALUES ("' + getManager(sqlCount) + '", ' + weekString + ', ' + str(year) + ', 1, "' + getDescription(sqlCount) + '");')
    sqlCount = sqlCount + 1

conn.commit()
conn.close()
