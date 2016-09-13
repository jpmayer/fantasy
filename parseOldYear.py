import sys
from conf import *

if len(sys.argv) == 2:
    year = sys.argv[1]
    lines = [line.rstrip('\n') for line in open(str(sys.argv[1]) + '.txt')]
    count = 0
    trueCount = 0
    manager = ""
    managerOpp = ""
    player = ""
    playerPos = ""
    playerTeam = ""
    playerScore = 0
    playerOpp = ""
    playerIsAway = False;
    homePlayers = []
    awayPlayers = []
    homePlayerScore = 0;
    awayPlayerScore = 0;
    isAway = True
    week = 1
    for line in lines:
      if count == 0:
        manager = line
        if isAway == True:
          managerOpp = lines[(trueCount + 28)]
        else:
          managerOpp = lines[(trueCount - 28)]
      elif count % 3 == 0:
        playerScore = line.split('\t')[1]
        print("INSERT INTO history (manager, week, year, vs, player, playerPosition, score, isHomeGame) VALUES ('" + manager + "', " + str(week) + ", " + str(year) + ", '" + managerOpp + "', '" + player.replace("'", r"") + "', '" + playerPos + "', '" + str(playerScore) + "', '" + str(int(not isAway)) + "');")
        if isAway == True:
            awayPlayerScore = awayPlayerScore + int(playerScore)
        else:
            homePlayerScore = homePlayerScore + int(playerScore)
        if count == 27:
          count = -1
          isAway = not isAway
      elif count % 3 == 1:
        playerInfo = line.split(',')
        player = playerInfo[0]
        morePlayerInfo = playerInfo[1].strip().split()
        playerPos = morePlayerInfo[1]
      count = count + 1
      trueCount = trueCount + 1
      if trueCount % 56 == 0:
          awayManager = ''
          homeManager = ''
          homeFieldAdvantage = 2 if week < 14 else 0
          awayPointDiff = awayPlayerScore - (homePlayerScore + homeFieldAdvantage)
          homePointDiff = -awayPointDiff
          if isAway == True:
              awayManager = managerOpp
              homeManager = manager
          else:
              awayManager = manager
              homeManager = managerOpp
          awayWinLoss = 'win'
          homeWinLoss = 'loss'
          if awayPointDiff == 0:
              awayWinLoss = 'tie'
              homeWinLoss = 'tie'
          elif awayPointDiff < 0:
              awayWinLoss = 'loss'
              homeWinLoss = 'win'
          #home
          print("INSERT INTO matchups (manager, week, year, vs, isHomeGame, winLoss, score, matchupTotal, pointDiff) VALUES ('" + homeManager + "', " + str(week) + ", " + str(year) + ", '" + awayManager + "', '" + str(1) + "', '" + homeWinLoss + "', '" + str(homePlayerScore + homeFieldAdvantage) + "', '" + str(homePlayerScore + homeFieldAdvantage + awayPlayerScore) + "', '" + str(homePointDiff) + "');")
          #away
          print("INSERT INTO matchups (manager, week, year, vs, isHomeGame, winLoss, score, matchupTotal, pointDiff) VALUES ('" + awayManager + "', " + str(week) + ", " + str(year) + ", '" + homeManager + "', '" + str(0) + "', '" + awayWinLoss + "', '" + str(awayPlayerScore) + "', '" + str(homePlayerScore + homeFieldAdvantage + awayPlayerScore) + "', '" + str(awayPointDiff) + "');")
          awayPlayerScore = 0
          homePlayerScore = 0
      if trueCount % ( (1 + 3 * numOfPlayers) * numberOfTeams ) == 0:
          week = week + 1
      if week == 16 and trueCount % ( (1 + 3 * numOfPlayers) * 2 ) == 0:
          week = week + 1
      elif week == 15 and trueCount % ( (1 + 3 * numOfPlayers) * 4 ) == 0:
          week = week + 1
      elif week == 14 and trueCount % ( ( (1 + 3 * numOfPlayers) * numberOfTeams ) + (1 + 3 * numOfPlayers) * getNumTeamsInRoundOneOfPlayoffs() ) == 0:
          week = week + 1
else:
    print("Wrong Arguments. Please input year")
