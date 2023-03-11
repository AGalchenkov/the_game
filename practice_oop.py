import asyncio
import os
import sys
from time import time

GAME_NAME = '''
##     ###### ##  ## ###### ##  ##  ####     ##     ###### ###### #####
##       ##   ##  ##   ##   ### ## ##        ##       ##   ##     ##   
##       ##   ##  ##   ##   ## ### ## ###    ##       ##   ####   #### 
##       ##    ####    ##   ##  ## ##  ##    ##       ##   ##     ##   
###### ######   ##   ###### ##  ##  ####     ###### ###### ##     #####
'''

class TheGame:

    def __init__(self) -> None:
        self.start_time = time()
        self.history = "input history: "
        self.banner = ""
    
    async def wait_input(self):
        loop = asyncio.get_running_loop()
        while True:
            user_input = await loop.run_in_executor(None, input)
            self.history += " " + user_input
            
    async def clear_screen(self):
        while True:
            os.system('cls||clear')
            self.banner = ""
            self.banner += GAME_NAME
            ellepsed = time() - self.start_time
            self.banner += str(int(ellepsed)) + 's\r\n'
            self.banner += self.history + '\r\n'
            self.banner += 'what? :'
            print(self.banner, end="")
            await asyncio.sleep(1)
        
    
    async def main_loop(self):
        
        input_task = asyncio.create_task(self.wait_input())
        clear_task = asyncio.create_task(self.clear_screen())
        await asyncio.gather(input_task, clear_task) 
    
    def run_the_game(self):
        try:
            asyncio.run(self.main_loop())
        except KeyboardInterrupt:
            print('\r\nBye!')
            sys.exit(0)

class Man:
    ...


class Leg:
    ...
    

class Arm:
    ...

class Body:
    ...
    
class Head:
    ...

g = TheGame()
g.run_the_game()