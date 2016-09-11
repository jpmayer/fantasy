import sys
from conf import *

lines = [line.rstrip('\n') for line in open(str(sys.argv[1]))]
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
    if "D/ST" not in line:
        playerInfo = line.split(',')
        temp = playerInfo[0].split()
        temp.pop(0)
        player = (" ").join(temp);
        morePlayerInfo = playerInfo[1].strip().split()
        playerPos = morePlayerInfo[1].replace("Recent News",r"").replace("Breaking Video",r"").replace)("Breaking News",r"")
    else:
        playerInfo = line.split();
        player = playerInfo[1] + " " + playerInfo[2]
        playerPos = playerInfo[2].replace("Recent News",r"").replace("Breaking Video",r"").replace)("Breaking News",r"")
  count = count + 1
  trueCount = trueCount + 1
  if trueCount % 56 == 0:
      awayManager = ''
      homeManager = ''
      homeFieldAdvantage = homeFieldAdv if week < 14 else 0
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
      print("INSERT INTO matchups (manager, week, year, vs, isHomeGame, winLoss, score, matchupTotal, pointDiff) VALUES ('" + homeManager + "', " + str(week) + ", " + str(year) + ", '" + awayManager + "', '" + str(1) + "', '" + homeWinLoss + "', '" + str(homePlayerScore + homeFieldAdv) + "', '" + str(homePlayerScore + homeFieldAdv + awayPlayerScore) + "', '" + str(homePointDiff) + "');")
      #away
      print("INSERT INTO matchups (manager, week, year, vs, isHomeGame, winLoss, score, matchupTotal, pointDiff) VALUES ('" + awayManager + "', " + str(week) + ", " + str(year) + ", '" + homeManager + "', '" + str(0) + "', '" + awayWinLoss + "', '" + str(awayPlayerScore) + "', '" + str(homePlayerScore + homeFieldAdv + awayPlayerScore) + "', '" + str(awayPointDiff) + "');")
      awayPlayerScore = 0
      homePlayerScore = 0
