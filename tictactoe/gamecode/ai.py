from .table import Table
from copy import deepcopy
class AiUser():
    charac = None
    isX = None
    wins = 0


    def __init__(self, isX):
        self.isX = isX
        if isX:
            self.charac = "X"
        else:
            self.charac = "O"

    def __checkcanwinrow(self, grid, charac):

        for row in range(len(grid)):
            characcount = 0
            blankcount = 0
            for item in grid[row]:
                if item == charac:
                    characcount += 1
                elif item == "~":
                    blankcount += 1
            if characcount == 2 and blankcount == 1:
                for item in range(len(grid[row])):
                    if grid[row][item] == "~":
                        return True, row, item
        return False, 1, 1

    def __checkrowwinslist(self, grid, charac):
        wins=[]
        for row in range(len(grid)):
            
            characcount = 0
            blankcount = 0
            for item in grid[row]:
                if item == charac:
                    characcount += 1
                elif item == "~":
                    blankcount += 1
            if characcount == 2 and blankcount == 1:
                for item in range(len(grid[row])):
                    if grid[row][item] == "~":
                        wins.append([row,item])
        return wins

    def __checkcanwincolumn(self, grid, charac):
        leng = len(grid[0])
        for i in range(leng):
            characcount = 0
            blankcount = 0
            blankpos = 0
            for row in range(len(grid)):
                if grid[row][i] == charac:
                    characcount += 1
                elif grid[row][i] == "~":
                    blankcount += 1
                    blankpos = row
            if characcount == 2 and blankcount == 1:
                return True, blankpos, i
        return False, 1, 1
    
    def __checkcolwinslist(self, grid, charac):
        wins=[]
        leng = len(grid[0])
        for i in range(leng):
            characcount = 0
            blankcount = 0
            blankpos = 0
            for row in range(len(grid)):
                if grid[row][i] == charac:
                    characcount += 1
                elif grid[row][i] == "~":
                    blankcount += 1
                    blankpos = row
            if characcount == 2 and blankcount == 1:
                wins.append([blankpos,i])
        return wins

    def __checkcanwindiagtl(self, grid, charac):
        characcount = 0
        blankcount = 0
        blankid = None
        for row in range(len(grid)):
            if grid[row][row] == charac:
                characcount += 1
            elif grid[row][row] == "~":
                blankcount += 1
                blankid = row
        if characcount == 2 and blankcount == 1:
            return True, blankid, blankid
        return False, 1, 1

    def __checkcanwindiagtr(self, grid, charac):
        leng = len(grid[0])
        leng -= 1
        characcount = 0
        blankcount = 0
        blankrow = None
        blankcol = None

        for row in range(len(grid)):
            if grid[row][leng - row] == charac:
                characcount += 1
            elif grid[row][leng - row] == "~":
                blankcount += 1
                blankrow = row
                blankcol = leng - row

        
        if characcount == 2 and blankcount == 1:
            return True, blankrow, blankcol
        return False, 1, 1

    def __getwinloc(self, gameTable, charac):
        canwinrow, moverow, movecol = self.__checkcanwinrow(
            gameTable.grid, charac)
        if canwinrow:
            return True, moverow, movecol
        canwincol, moverow, movecol = self.__checkcanwincolumn(
            gameTable.grid, charac)
        if canwincol:
            return True, moverow, movecol
        canwindiagtl, moverow, movecol = self.__checkcanwindiagtl(
            gameTable.grid, charac)
        if canwindiagtl:
            return True, moverow, movecol
        canwindiagtr, moverow, movecol = self.__checkcanwindiagtr(
            gameTable.grid, charac)
        if canwindiagtr:
            return True, moverow, movecol
        return False, 69, 420



    def __getwinloclist(self, gameTable, charac):
        wins=[]
        for item in self.__checkrowwinslist(gameTable.grid, charac):
            wins.append(item)
        for item in self.__checkcolwinslist(gameTable.grid,charac):
            wins.append(item)
        canwindiagtl, moverow, movecol = self.__checkcanwindiagtl(
            gameTable.grid, charac)
        if canwindiagtl:
            wins.append([moverow, movecol]) 
        canwindiagtr, moverow, movecol = self.__checkcanwindiagtr(
            gameTable.grid, charac)
        if canwindiagtr:
            wins.append([moverow,movecol])
        return wins

    def __blockwin(self, gameTable):
        charac = None
        if self.charac == "X":
            charac = "O"
        else:
            charac = "X"
        return self.__getwinloc(gameTable, charac)

    def __win(self, gameTable):
        return self.__getwinloc(gameTable, self.charac)

    def __checknumcanwinrow(self, grid, charac):
        rowsfound = 0
        for row in range(len(grid)):
            characcount = 0
            blankcount = 0
            for item in grid[row]:
                if item == charac:
                    characcount += 1
                elif item == "~":
                    blankcount += 1
            if characcount == 2 and blankcount == 1:
                rowsfound += 1
        return rowsfound

    def __checknumcanwincol(self, grid, charac):
        colwins = 0
        leng = len(grid[0])
        for i in range(leng):
            characcount = 0
            blankcount = 0
            blankpos = 0
            for row in range(len(grid)):
                if grid[row][i] == charac:
                    characcount += 1
                elif grid[row][i] == "~":
                    blankcount += 1
                    blankpos = row
            if characcount == 2 and blankcount == 1:
                colwins += 1

        return colwins

    def __doescreatefork(self, gametable, row, item, charac):
        totwins = 0
        secondarygametable = Table()
        secondarygametable.grid = deepcopy(gametable.grid)
        secondarygametable.grid[row][item] = charac
        rowwins=self.__checknumcanwinrow(secondarygametable.grid, charac)
        colwins=self.__checknumcanwincol(secondarygametable.grid, charac)
        totwins +=rowwins 
        totwins += colwins
        if (self.__checkcanwindiagtl(secondarygametable.grid, charac)[0]):
            totwins += 1
        if (self.__checkcanwindiagtr(secondarygametable.grid, charac)[0]):
            totwins += 1
        if totwins >= 2:
            return True
        return False

    def __getforkloc(self, gametable, charac):
        for row in range(len(gametable.grid)):
            for item in range(len(gametable.grid[row])):
                if gametable.grid[row][item] == "~":
                    createsfork = self.__doescreatefork(
                        gametable,row,item, charac)
                    if createsfork:

                        return True, row, item

        return False, 69, 420

    def __fork(self, gametable):
        return self.__getforkloc(gametable, self.charac)
    
    def __getforkstoblock(self,gametable,charac):
        forkstoblock=[]
        for row in range(len(gametable.grid)):
            for item in range(len(gametable.grid[row])):
                if gametable.grid[row][item] == "~":
                    createsfork = self.__doescreatefork(
                        gametable, row, item, charac)
                    if createsfork:
                        forkstoblock.append([row,item])
        return forkstoblock


    def __blockfork(self, gametable):
        if self.charac=="X":
            enemycharac="O"
        else:
            enemycharac="X"
        forkmoves=self.__getforkstoblock(gametable,enemycharac)
        if len(forkmoves)==0:
            return False,69,420
        elif len(forkmoves)==1:
            return True,forkmoves[0][0],forkmoves[0][1]
        else:
            #two in row while blocking both
            
            movepairs=[]
            for move in forkmoves:
                if self.isX:
                    oppcharac="O"
                else:
                    oppcharac="X"
                secondarygametable = Table()
                secondarygametable.grid=deepcopy(gametable.grid)
                secondarygametable.grid[move[0]][move[1]]=oppcharac
                for item in self.__getwinloclist(secondarygametable,oppcharac):
                    movepairs.append([move,item])
            for item in movepairs[0]:
                found=True
                for pair in movepairs:
                    if item not in movepairs:
                        found = False
                if found:
                    anothergametable=Table()
                    anothergametable.gird=deepcopy(gametable.grid)
                    anothergametable.grid[item[0]][item[1]]=self.charac
                    if self.__getwinloc(anothergametable,self.charac)[0]:
                        print("blockblock")
                        return True, item[0],item[1]
            for row in range(len(gametable.grid)):
                for item in range(len(gametable.grid[row])):
                    if gametable.grid[row][item]=="~":
                        notanothergametable = Table()
                        notanothergametable.grid=deepcopy(gametable.grid)
                        notanothergametable.grid[row][item]=self.charac
                        iswin,winrow,wincol=self.__getwinloc(notanothergametable,self.charac)
                        if iswin:
                            if [winrow,wincol] not in forkmoves:
                                return True, row,item
            raise ValueError

    def __cangocenter(self, gametable):
        if gametable.grid[1][1] == "~":
            return True
        return False

    def __gooppositecorner(self, gametable):
        if self.charac == "X":
            enemycharac = "O"
        else:
            enemycharac = "X"
        if gametable.grid[0][0] == enemycharac and gametable.grid[2][2] == "~":
            return True, 2, 2
        elif gametable.grid[2][2] == enemycharac and gametable.grid[0][
                0] == "~":
            return True, 0, 0
        elif gametable.grid[0][2] == enemycharac and gametable.grid[2][
                0] == "~":
            return True, 2, 0
        elif gametable.grid[2][0] == enemycharac and gametable.grid[0][
                2] == "~":
            return True, 0, 2
        return False, 69, 420

    def __gocorner(self, gametable):
        if gametable.grid[0][0] == "~":
            return True, 0, 0
        elif gametable.grid[0][2] == "~":
            return True, 0, 2
        elif gametable.grid[2][0] == "~":
            return True, 2, 0
        elif gametable.grid[2][2] == "~":
            return True, 2, 2
        return False, 69, 420

    def __edge(self, gametable):
        if gametable.grid[0][1] == "~":
            return 0, 1
        elif gametable.grid[1][0] == "~":
            return 1, 0
        elif gametable.grid[1][2] == "~":
            return 1, 2
        elif gametable.grid[2][1] == "~":
            return 2, 1

    def getmove(self, gameTable):
        canWin, moverow, movecol = self.__win(gameTable)
        if canWin:
            print("win")
            return moverow, movecol
        canblockwin, moverow, movecol = self.__blockwin(gameTable)
        if canblockwin:
            print("block")
            return moverow, movecol
        canfork, moverow, movecol = self.__fork(gameTable)
        if canfork:
            print("fork")
            return moverow, movecol
        canblockfork, moverow, movecol = self.__blockfork(gameTable)
        if canblockfork:
            print("blockfork")
            return moverow, movecol
        cangocenter = self.__cangocenter(gameTable)
        if cangocenter:
            print("center")
            return 1, 1
        cangoopcorner, moverow, movecol = self.__gooppositecorner(gameTable)
        if cangoopcorner:
            print("opcorner")
            return moverow, movecol
        cangocorner, moverow, movecol = self.__gocorner(gameTable)
        if cangocorner:
            print("corner")
            return moverow, movecol
        forever = gameTable
        print("bonk")
        moverow, movecol = self.__edge(forever)  #only edging in horny jail
        return moverow, movecol
