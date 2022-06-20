import random
from .ai import AiUser
from .table import Table

class tictactoe():
    players=0
    playersgo=None
    ai=None


    def __init__(self, players,firstgo=None):
        self.players = players
        self.table=Table()
        self.ai = AiUser(False)
        if firstgo==None:
            if randbool():
                self.playersgo="X"
            else:
                self.playersgo="O"
        else:
            self.playersgo=firstgo

    def getaimove(self):
        y,x=self.ai.getmove(self.table)
        self.table.play(x,y,False)   
        self.isX=not self.isX
        return response("update",self.table.grid,self.playersgo)

             
            
    
    def getplayersgo(self):
        return self.playersgo

    @property
    def isX(self):
        if self.playersgo=="X":
            return True
        else:
            return False
    
    @isX.setter
    def isX(self,value):
        if value:
            self.playersgo="X"
        else:
            self.playersgo="O"




    def clickevent(self,clicksquare):
        if self.players==2:
            return self.twoplayerclickevent(clicksquare)
        else:
            return self.oneplayerclickevent(clicksquare)

    def oneplayerclickevent(self,clicksquare):
        x=clicksquare%3
        y=clicksquare//3
        if not self.table.checkspacefree(x,y):
            return response("error","space already taken")
        self.table.play(x,y,self.isX)
        won,charac=self.table.checkwin()
        if won:
            if charac!="~":
                return response("win",self.table.grid,self.playersgo)
            else:
                return response("draw",self.table.grid)
        else:
            self.isX=not self.isX
            y,x=self.ai.getmove(self.table)
            self.table.play(x,y,self.isX)   
            won,charac=self.table.checkwin()
            if not won:
                self.isX=not self.isX
                return response("update",self.table.grid,self.playersgo)
            elif charac=="~":
                return response("draw",self.table.grid)
            else:
                return response("lose",self.table.grid,self.playersgo)



    def twoplayerclickevent(self,clicksquare):
        x=clicksquare%3
        y=clicksquare//3
        if not self.table.checkspacefree(x,y):
            return response("error","space already taken")
        self.table.play(x,y,self.isX)
        won,charac=self.table.checkwin()
        if not won:
            self.isX=not self.isX
            return response("update",self.table.grid,self.playersgo)
        elif charac=="~":
            return response("draw",self.table.grid)
        else:
            return response("win",self.table.grid,self.playersgo)

        
    
class response():
    type=None
    data=None
    secondarydata=None
    def __init__(self,type,data,secondarydata=None):
        self.type=type
        self.data=data
        self.secondarydata=secondarydata


def randbool():
    x = random.randint(0, 1)
    if x == 1:
        return True
    return False











  



     








    