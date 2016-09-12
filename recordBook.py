import sqlite3
import operator

conn = sqlite3.connect("league.db")
c = conn.cursor()

playerData = 'history'  # breakdown by player data
matchupData = 'matchups'  # breakdown by matchup totals

def getMostPointsGame():
    "Return Most Points Scored in a Game by a Manager"
    c.execute('SELECT manager, score, year, week, vs FROM {tn} ORDER BY {cn} DESC LIMIT 1'.\
            format(tn=matchupData, cn='score'))
    top_game = c.fetchone()
    if top_game is None:
        return ("N/A",0,"N/A","N/A","N/A")
    else:
        return (str(top_game[0]), top_game[1], top_game[2], top_game[3], str(top_game[4]))

def getMostPointsSeason():
    "Return Most Points Scored in a Season by a Manager (excludes playoffs)"
    c.execute('SELECT manager, score, year, week FROM {tn}'.\
            format(tn=matchupData))
    all_rows = c.fetchall()
    pysMap = {}
    for game in all_rows:
        if(game[3] < 14):
            key = str(game[0]) + "-" + str(game[2]);
            if key in pysMap:
                pysMap[key] = pysMap[key] + game[1]
            else:
                pysMap[key] = game[1]
    if len(pysMap) > 0:
        score = pysMap[max(pysMap.iteritems(), key=operator.itemgetter(1))[0]]
        ownerYear = max(pysMap.iteritems(), key=operator.itemgetter(1))[0].split("-")
        owner = ownerYear[0]
        year = ownerYear[1]
        return (owner, year, score)
    else:
        return ("N/A","N/A",0)

def getMostPointsMatchup():
    "Return Most Points Scored in a Game between both Managers"
    c.execute('SELECT manager, matchupTotal, score, year, week, vs, winLoss, isHomeGame FROM {tn} ORDER BY {cn} DESC LIMIT 1'.\
            format(tn=matchupData, cn='matchupTotal'))
    top_game = c.fetchone()
    if top_game is None:
        return ("N/A",0,0,"N/A","N/A","N/A","N/A","N/A")
    else:
        return (str(top_game[0]), top_game[1], top_game[2], top_game[3], str(top_game[4]), str(top_game[5]), str(top_game[6]), top_game[7])

def getLeastPointsGame():
    "Return Least Points Scored in a Game by a Manager"
    c.execute('SELECT manager, score, year, week, vs FROM {tn} ORDER BY {cn} ASC LIMIT 1'.\
            format(tn=matchupData, cn='score'))
    top_game = c.fetchone()
    if top_game is None:
        return ("N/A",0,"N/A","N/A","N/A")
    else:
        return (str(top_game[0]), top_game[1], top_game[2], top_game[3], str(top_game[4]))

def getLeastPointsSeason():
    "Return Least Points Scored in a Season by a Manager (excludes playoffs)"
    c.execute('SELECT manager, score, year, week FROM {tn}'.\
            format(tn=matchupData))
    all_rows = c.fetchall()
    pysMap = {}
    for game in all_rows:
        if(game[3] < 14):
            key = str(game[0]) + "-" + str(game[2]);
            if key in pysMap:
                pysMap[key] = { 'name': str(game[0]), 'year': str(game[2]), 'count': pysMap[key].get('count') + game[1], 'numGames': pysMap[key].get('numGames') + 1 }
            else:
                pysMap[key] = { 'name': str(game[0]), 'year': str(game[2]), 'count': game[1], 'numGames': 1 }
    if len(pysMap) > 0:
        minSeason = { 'count': 9999, 'numGames': 13}
        for seasonKey in pysMap:
            if pysMap[seasonKey].get('numGames') == 13:
                if pysMap[seasonKey].get('count') < minSeason.get('count'):
                    minSeason = pysMap[seasonKey]
        score = minSeason.get('count')
        owner = minSeason.get('name')
        year = minSeason.get('year')
        return (owner, year, score)
    else:
        return ("N/A","N/A",0)

def getLeastPointsMatchup():
    "Return Least Points Scored in a Game between both Managers"
    c.execute('SELECT manager, matchupTotal, score, year, week, vs, winLoss, isHomeGame FROM {tn} ORDER BY {cn} ASC LIMIT 1'.\
            format(tn=matchupData, cn='matchupTotal'))
    top_game = c.fetchone()
    if top_game is None:
        return ("N/A",0,0,"N/A","N/A","N/A","N/A","N/A")
    else:
        return (str(top_game[0]), top_game[1], top_game[2], top_game[3], str(top_game[4]), str(top_game[5]), str(top_game[6]), top_game[7])

def getMostPointsAllowedSeason():
    "Return Most Points Scored Against a Manager in a Season (excludes playoffs)"
    c.execute('SELECT vs, score, year, week FROM {tn}'.\
            format(tn=matchupData))
    all_rows = c.fetchall()
    pysMap = {}
    for game in all_rows:
        if(game[3] < 14):
            key = str(game[0]) + "-" + str(game[2]);
            if key in pysMap:
                pysMap[key] = { 'name': str(game[0]), 'year': str(game[2]), 'count': pysMap[key].get('count') + game[1], 'numGames': pysMap[key].get('numGames') + 1 }
            else:
                pysMap[key] = { 'name': str(game[0]), 'year': str(game[2]), 'count': game[1], 'numGames': 1 }
    if len(pysMap) > 0:
        maxSeason = { 'count': 0, 'numGames': 13}
        for seasonKey in pysMap:
            if pysMap[seasonKey].get('numGames') == 13:
                if pysMap[seasonKey].get('count') > maxSeason.get('count'):
                    maxSeason = pysMap[seasonKey]
        score = maxSeason.get('count')
        owner = maxSeason.get('name')
        year = maxSeason.get('year')
        return (owner, year, score)
    else:
        return ("N/A","N/A",0)

def getFewestPointsAllowedSeason():
    "Return Most Points Scored Against a Manager in a Season (excludes playoffs)"
    c.execute('SELECT vs, score, year, week FROM {tn}'.\
            format(tn=matchupData))
    all_rows = c.fetchall()
    pysMap = {}
    for game in all_rows:
        if(game[3] < 14):
            key = str(game[0]) + "-" + str(game[2]);
            if key in pysMap:
                pysMap[key] = { 'name': str(game[0]), 'year': str(game[2]), 'count': pysMap[key].get('count') + game[1], 'numGames': pysMap[key].get('numGames') + 1 }
            else:
                pysMap[key] = { 'name': str(game[0]), 'year': str(game[2]), 'count': game[1], 'numGames': 1 }
    if len(pysMap) > 0:
        minSeason = { 'count': 9999, 'numGames': 13}
        for seasonKey in pysMap:
            if pysMap[seasonKey].get('numGames') == 13:
                if pysMap[seasonKey].get('count') < minSeason.get('count'):
                    minSeason = pysMap[seasonKey]
        score = minSeason.get('count')
        owner = minSeason.get('name')
        year = minSeason.get('year')
        return (owner, year, score)
    return ("N/A","N/A",0)

def getLongestWinStreak():
    "Return Longest Win Streak(s) by a Manager"
    c.execute('SELECT manager, year, week, winLoss FROM {tn} ORDER BY manager ASC, year ASC, week ASC'.\
            format(tn=matchupData))
    all_rows = c.fetchall()
    if len(all_rows) == 0:
        return []
    else:
        topWinStreak = []
        winStreaks = []
        currentStreak = []
        isWinning = -1;
        currentManager = all_rows[0][0]
        for game in all_rows:
            if(game[0] != currentManager):
                currentStreak = []
                isWinning = -1
                currentManager = game[0]
            if game[3] == 'win':
                if isWinning == 1:
                    currentStreak.append(game)
                else:
                    currentStreak = [game]
                    isWinning = 1
            elif game[3] == 'loss':
                isWinning = 0
                currentStreak = []
            else:
                isWinning = 2
                currentStreak = []
            if len(currentStreak) == len(topWinStreak):
                if currentStreak not in winStreaks:
                    winStreaks.append(currentStreak)
            elif len(currentStreak) > len(topWinStreak):
                topWinStreak = currentStreak
                winStreaks = [topWinStreak]
        return winStreaks

def getLongestLosingStreak():
    "Return Longest Losing Streak(s) by a Manager"
    c.execute('SELECT manager, year, week, winLoss FROM {tn} ORDER BY manager ASC, year ASC, week ASC'.\
            format(tn=matchupData))
    all_rows = c.fetchall()
    if len(all_rows) == 0:
        return []
    else:
        topLosingStreak = []
        losingStreaks = []
        currentStreak = []
        isWinning = -1;
        currentManager = all_rows[0][0]
        for game in all_rows:
            if(game[0] != currentManager):
                currentStreak = []
                isWinning = -1
                currentManager = game[0]
            if game[3] == 'win':
                isWinning = 1
                currentStreak = []
            elif game[3] == 'loss':
                if isWinning == 0:
                    currentStreak.append(game)
                else:
                    currentStreak = [game]
                    isWinning = 0
            else:
                isWinning = 2
                currentStreak = []
            if len(currentStreak) == len(topLosingStreak):
                if currentStreak not in losingStreaks:
                    losingStreaks.append(currentStreak)
            elif len(currentStreak) > len(topLosingStreak):
                topLosingStreak = currentStreak
                losingStreaks = [topLosingStreak]
        return losingStreaks

def getMostPointsPlayerGame():
    "Return Most Points Scored in a Game by an NFL Player"
    c.execute('SELECT player, playerPosition, score, year, week, manager FROM {tn} ORDER BY {cn} DESC LIMIT 1'.\
            format(tn=playerData, cn='score'))
    top_game = c.fetchone()
    if top_game is None:
        return ("N/A","N/A",0,"N/A","N/A","N/A")
    else:
        return (str(top_game[0]), str(top_game[1]), top_game[2], top_game[3], top_game[4], str(top_game[5]))

def getMostPointsPlayerSeason():
    "Return Most Points Scored in a Season by an NFL Player (excludes playoffs)"
    c.execute('SELECT player, playerPosition, score, year, week, manager FROM {tn}'.\
            format(tn=playerData))
    all_rows = c.fetchall()
    pysMap = {}
    for game in all_rows:
        if(game[4] < 14):
            key = str(game[0]) + "-" + str(game[3]);
            if key in pysMap:
                pysMap[key] = pysMap[key] + game[2]
            else:
                pysMap[key] = game[2]
    if len(pysMap) > 0:
        score = pysMap[max(pysMap.iteritems(), key=operator.itemgetter(1))[0]]
        playerYear = max(pysMap.iteritems(), key=operator.itemgetter(1))[0].split("-")
        player = playerYear[0]
        year = playerYear[1]
        return (player, year, score)
    else:
        return ("N/A","N/A",0)

def generateStreakYearsString(streaks):
    stringResults = ""
    for streak in streaks:
        stringResults = stringResults + streak.get("start") + " to " + streak.get("end") + " / "
    return stringResults.strip()[:-1]

mPG = getMostPointsGame()
mPS = getMostPointsSeason()
mPM = getMostPointsMatchup()
matchupString = ""
matchupOppScore = mPM[1] - mPM[2];
if mPM[7] == 1:
    matchupString = str(mPM[5]) + " (" + str(matchupOppScore) + ") vs. " + str(mPM[0]) + " (" + str(mPM[2]) + ")"
else:
    matchupString = str(mPM[0]) + " (" + str(mPM[2]) + ") vs. " + str(mPM[5]) + " (" + str(matchupOppScore) + ")"
lPG = getLeastPointsGame()
lPS = getLeastPointsSeason()
lPM = getLeastPointsMatchup()
leastMatchupString = ""
leastMatchupOppScore = lPM[1] - lPM[2];
if lPM[7] == 1:
    leastMatchupString = str(lPM[5]) + " (" + str(leastMatchupOppScore) + ") vs. " + str(lPM[0]) + " (" + str(lPM[2]) + ")"
else:
    leastMatchupString = str(lPM[0]) + " (" + str(lPM[2]) + ") vs. " + str(lPM[5]) + " (" + str(leastMatchupOppScore) + ")"
mPAS = getMostPointsAllowedSeason()
fPAS = getFewestPointsAllowedSeason()
streakWeeks = []
streakOwners = []
streakLength = 0;
lWS = getLongestWinStreak()
for streak in lWS:
    streakLength = len(streak)
    streakWeeks.append({ 'start': str(streak[0][1]) + " Week " + str(streak[0][2]), 'end': str(streak[-1][1]) + " Week " + str(streak[-1][2])})
    streakOwners.append(str(streak[0][0]))
winStreakYears = generateStreakYearsString(streakWeeks)
winStreakOwners = (" / ").join(streakOwners)

losingStreakWeeks = []
losingStreakOwners = []
losingStreakLength = 0;
lLS = getLongestLosingStreak()
for losingStreak in lLS:
    losingStreakLength = len(losingStreak)
    losingStreakWeeks.append({ 'start': str(losingStreak[0][1]) + " Week " + str(losingStreak[0][2]), 'end': str(losingStreak[-1][1]) + " Week " + str(losingStreak[-1][2])})
    losingStreakOwners.append(str(losingStreak[0][0]))
losingStreakYears = generateStreakYearsString(losingStreakWeeks)
losingStreakManagers = (" / ").join(losingStreakOwners)

mPPlG = getMostPointsPlayerGame()
mPPlS = getMostPointsPlayerSeason()

resultString = "<div id='recordBook'>"
resultString = resultString + "<table>"
resultString = resultString + "<tr>"
resultString = resultString + "<th colspan='3' class='header'><h3>League Record Book</h3></th>"
resultString = resultString + "</tr>"
resultString = resultString + "<tr> <td class='column1'><b>Category</b></td><td class='column2'><b>Record</b></td><td class='column3'><b>Holder</b></td></tr>"
resultString = resultString + "<tr> <td class='recordType odd'>Most Points (Game) </td><td class='center odd'>" + str(mPG[1]) + "</td><td class='center odd' title='" + str(mPG[2]) + " - Week " + str(mPG[3]) + "'>" + str(mPG[0]) + "</td></tr>"
resultString = resultString + "<tr> <td class='recordType even'>Most Points (Season) </td><td class='center even'>" + str(mPS[2]) + "</td><td class='center even' >" + str(mPS[0]) + " - " + str(mPS[1]) + "</td></tr>"
resultString = resultString + "<tr> <td class='recordType odd'>Most Points (Matchup) </td><td class='center odd'>" + str(mPM[1]) + "</td><td class='center odd' title='" + str(mPM[3]) + " - Week " + str(mPM[4]) + "'>" + matchupString + "</td></tr>"
resultString = resultString + "<tr> <td class='recordType even'>Fewest Points (G) </td><td class='center even'>" + str(lPG[1]) + "</td><td class='center even' title='" + str(lPG[2]) + " - Week " + str(lPG[3]) + "'>" + str(lPG[0]) + "</td></tr>"
resultString = resultString + "<tr> <td class='recordType odd'>Fewest Points (S) </td><td class='center odd'>" + str(lPS[2]) + "</td><td class='center odd' >" + str(lPS[0]) + " - " + str(lPS[1]) + "</td></tr>"
resultString = resultString + "<tr> <td class='recordType even'>Fewest Points (M) </td><td class='center even'>" + str(lPM[1]) + "</td><td class='center even' title='" + str(lPM[3]) + " - Week " + str(lPM[4]) + "'>" + leastMatchupString + "</td></tr>"
resultString = resultString + "<tr> <td class='recordType odd'>Most Points Allowed (S) </td><td class='center even'>" + str(mPAS[2]) + "</td><td class='center even' >" + str(mPAS[0]) + " - " + str(mPAS[1]) + "</td></tr>"
resultString = resultString + "<tr> <td class='recordType even'>Fewest Points Allowed (S) </td><td class='center even'>" + str(fPAS[2]) + "</td><td class='center even' >" + str(fPAS[0]) + " - " + str(fPAS[1]) + "</td></tr>"
resultString = resultString + "<tr> <td class='recordType odd'>Longest Win Streak </td><td class='center odd'>" + str(streakLength) + "</td><td class='center odd' title='" + str(winStreakYears) + "'>" + str(winStreakOwners) + "</td></tr>"
resultString = resultString + "<tr> <td class='recordType even'>Longest Losing Streak </td><td class='center even'>" + str(losingStreakLength) + "</td><td class='center even' title='" + str(losingStreakYears) + "'>" + str(losingStreakManagers) + "</td></tr>"
resultString = resultString + "<tr> <td class='recordType odd'>Most Points-Player (G) </td><td class='center odd'>" + str(mPPlG[2]) + "</td><td class='center odd' title='" + str(mPPlG[3]) + " - Week " + str(mPPlG[4]) + "; Owner: " + str(mPPlG[5]) + "'>" + str(mPPlG[0]) + "</td></tr>"
resultString = resultString + "<tr> <td class='recordType even'>Most Points-Player (S) </td><td class='center even'>" + str(mPPlS[2]) + "</td><td class='center even'>" + str(mPPlS[0]) + " - " + str(mPPlS[1]) + "</td></tr>"
resultString = resultString + "</table></div>"
resultString = resultString + "<style>"
resultString = resultString + ".header {"
resultString = resultString + "  width:500px;"
resultString = resultString + "  background-color:#1D7225;"
resultString = resultString + "  color:white;"
resultString = resultString + "  text-align:center;"
resultString = resultString + "  border-radius: 3px 3px 0px 0px;"
resultString = resultString + "}"
resultString = resultString + ".column1 {"
resultString = resultString + "width:250px;"
resultString = resultString + "padding-left:5px;"
resultString = resultString + "background-color:#6DBB75;"
resultString = resultString + "text-align:left;"
resultString = resultString + "}"
resultString = resultString + ".column2 {"
resultString = resultString + "  background-color:#6DBB75;"
resultString = resultString + "  text-align:center;"
resultString = resultString + "  width:75px"
resultString = resultString + "}"
resultString = resultString + ".column3 {"
resultString = resultString + "  background-color:#6DBB75;"
resultString = resultString + "  text-align:center;"
resultString = resultString + "  padding-left:5px"
resultString = resultString + "}"
resultString = resultString + ".odd{"
resultString = resultString + "background-color:#F2F2E8;"
resultString = resultString + "}"
resultString = resultString + ".even{"
resultString = resultString + "background-color:#F8F8F2;"
resultString = resultString + "}"
resultString = resultString + ".center{"
resultString = resultString + "text-align:center;"
resultString = resultString + "}"
resultString = resultString + ".recordType{"
resultString = resultString + "width:250px;"
resultString = resultString + "padding-left:5px;"
resultString = resultString + "padding-top:5px;"
resultString = resultString + "}"
resultString = resultString + "#recordBook{"
resultString = resultString + "width:100%;"
resultString = resultString + "position:relative;"
resultString = resultString + "margin-left:auto;"
resultString = resultString + "margin-right:auto;"
resultString = resultString + "}"
resultString = resultString + "#recordBook table {"
resultString = resultString + "border:0px solid black;"
resultString = resultString + "font-size:12px;"
resultString = resultString + "width:100%;"
resultString = resultString + "}"
resultString = resultString + "</style>"

print(resultString)

conn.commit()
conn.close()
