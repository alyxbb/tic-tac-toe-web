import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .gamecode import tictactoegame
import asyncio



class TicTacToeConsumer(AsyncWebsocketConsumer):
    game=None
    firstgo=None
    players=None
    async def connect(self):
        await self.accept()


    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        command = text_data_json['command']
        if command=="startgame":
            players = text_data_json['players']
            if players!=0 and players<3:
                self.players=players
                self.game = tictactoegame.tictactoe(players)
                playergo=self.game.getplayersgo()
                self.firstgo=playergo
                await self.send(text_data=json.dumps({
                    "command":"startgame",
                    "go": self.game.getplayersgo(),
                    "players":players
                }))
                if playergo=="O" and players==1:
                    response=self.game.getaimove()
                    await self.send(text_data=json.dumps({
                        "command":"update",
                        "table":response.data,
                        "go":response.secondarydata
                    }))
                
                
            else:
                await self.send(text_data=json.dumps({
                    "command":"popup",
                    "message":"please select a number of players"
                }))
        elif command=="playermove":
            response=self.game.clickevent(text_data_json['move'])
            if response.type=="error":
                await self.send(text_data=json.dumps({
                    "command":"popup",
                    "message":response.data
                }))
            elif response.type=="update":
                await self.send(text_data=json.dumps({
                    "command":"update",
                    "table":response.data,
                    "go":response.secondarydata
                }))
                
            elif response.type=="win":
                if self.players==1:
                    print("--------------------------")
                    print("computer lost")
                await self.send(text_data=json.dumps({
                    "command":"update",
                    "table":response.data,
                    "go":response.secondarydata
                }))
                winmsg="winner winner chicken dinner! "+response.secondarydata+" wins!"
                await asyncio.sleep(0.5)
                await self.send(text_data=json.dumps({
                    "command":"popup",
                    "message":winmsg
                }))
                await asyncio.sleep(2)
                await self.restartgame()
                await self.send(text_data=json.dumps({
                    "command":"scoreboard",
                    "value":response.secondarydata
                }))



            elif response.type=="lose":
                await self.send(text_data=json.dumps({
                    "command":"update",
                    "table":response.data,
                    "go":response.secondarydata
                }))
                await asyncio.sleep(0.5)
                await self.send(text_data=json.dumps({
                    "command":"popup",
                    "message":"imaging being bad. you lost"
                }))
                await asyncio.sleep(2)
                await self.restartgame()
                await self.send(text_data=json.dumps({
                    "command":"scoreboard",
                    "value":"O"
                }))


            elif response.type=="draw":
                await self.send(text_data=json.dumps({
                    "command":"update",
                    "table":response.data,
                    "go":"no one"
                }))
                await asyncio.sleep(0.5)
                await self.send(text_data=json.dumps({
                    "command":"popup",
                    "message":"its a draw, get good"
                }))
                await asyncio.sleep(2)
                await self.restartgame()
                await self.send(text_data=json.dumps({
                    "command":"scoreboard",
                    "value":"D"
                }))


    async def restartgame(self):
        if self.firstgo=="O":
            go="X"
        else:
            go="O"
        self.game = tictactoegame.tictactoe(self.players,go)
        await self.send(text_data=json.dumps({
            "command":"refresh",
            "go": self.game.getplayersgo(),
            "players":self.players
        }))
        playergo=self.game.getplayersgo()
        self.firstgo=go
        if playergo=="O" and self.players==1:
            response=self.game.getaimove()
            await self.send(text_data=json.dumps({
                "command":"update",
                "table":response.data,
                "go":response.secondarydata
            }))
    


                
        