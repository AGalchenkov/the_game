import asyncio
from asyncio.exceptions import CancelledError
import os
import sys
import random
import readline
from time import time
from typing import Awaitable

GAME_NAME = '''
##     ###### ##  ## ###### ##  ##  ####     ##     ###### ###### #####
##       ##   ##  ##   ##   ### ## ##        ##       ##   ##     ##   
##       ##   ##  ##   ##   ## ### ## ###    ##       ##   ####   #### 
##       ##    ####    ##   ##  ## ##  ##    ##       ##   ##     ##   
###### ######   ##   ###### ##  ##  ####     ###### ###### ##     #####
'''

BORN_MENU = '''
    1. Попытаться родиться
    2. Выход
    
'''
RUNNING_MENU = '''
    1. Сделать шаг
    2. Взять предмет
    3. Выбросить предмет
    4. Инвентарь
    5. Осмотреться в поисках предметов 
    6. Определить направление
    7. Изменить направление
    8. Выход
    
'''

class Item:
    item_assort = (
        'мяч',
        'крыса',
        'стеклянный глаз',
        'тапочек',
        'граната',
        'бутылка',
        'пирожок',
        'граната без чеки',
        'маленький желтый жетончик на метро',
        'iphone',
        'стакан',
        'каблук',
        'кнопка',
        'красная кнопка',
        'чемоданчик',
        'черный чемоданчик',
        'черный чемоданчик с красной кнопкой',
        'рельса',
        'шпала',
        'поезд запоздалый',
        'вишня',
        'куб',
        'шар',
        'шапочка из фольги',
    )
    def __init__(self,):
        self.x_coord = random.randint(0, 200)
        self.y_coord = random.randint(0, 200)
        i = random.randint(0, len(self.item_assort))
        self.inst = self.item_assort[i]
        self.dog_guard = random.choices([True, False], weights=[40, 60])[0]


class Head:
    def __init__(self):
        self.agle = random.randint(-1200, 1200)
        self.direction = 90
        self.wind_rose = {
            0: 'восток',
            90: 'север',
            180: 'запад',
            270: 'юг'
        }

    def switch_direction(self):
        self.direction += 90
        self.direction = self.direction if self.direction < 360 else 0
        self.last_state = f'Повернули на {self.wind_rose[self.direction]}.'

    def determine_direction(self):
        self.last_state = f'Движемся на {self.wind_rose[self.direction]}.'


class Leg:
    def __init__(self):
        self.leg_count = random.choices([0, 1, 2], weights=[15, 40, 45])[0]


class Hand:
    def __init__(self):
        self.hand_count = random.choices([0, 1, 2], weights=[5, 10, 85])[0]
        self.in_hand = []

    def get_item(self, item:Item):
        if self.hand_count > 0:
            if len(self.in_hand) < self.hand_count:
                if abs(item.x_coord - self.x_coord) > 5 or abs(item.y_coord - self.y_coord) > 5:
                    state = 'До предмета не дотянуться.'
                    return False, state
                else:
                    if not item.dog_guard:
                        self.in_hand.append(item.inst)
                        state = f'Поздравляю, ты поднял {item.inst}'
                        return True, state
                    else:
                        self.hand_count -= 1
                        if self.hand_count > len(self.in_hand):
                            state = f'Поздравляю, ты поднял {item.inst}, но его охраняла собака тебе откусили руку. Количество оставшихся рук {self.hand_count}'
                            return True, state
                        elif self.hand_count == len(self.in_hand) and len(self.in_hand) > 0:
                            state = 'Предмет охраняла собака. Тебе откусили руку, а вторая занята...'
                            return True, state
                        else:
                            state = 'Предмет охраняла собака. Тебе откусили руку, больше не чем поднимать предметы...'
                            return True, state
            else:
                state = 'Все руки заняты.'
                return False, state
        else:
            state = 'Без рук тяжело что-либо поднять'
            return False, state

    def drop_item(self):  
        if self.in_hand:
            droped_item = self.in_hand.pop()
            state = f'Выкинул {droped_item}'
        else:
            state = 'Было бы что выбрасывать...'
        return state


class Body(Leg, Hand):
    def __init__(self):
        Leg.__init__(self)
        Hand.__init__(self)
        self.limbs = self.hand_count + self.leg_count  #(+ Done) ToDo Не нашел использования данной переменной


class Man(Head, Body):
    virus = False

    def __init__(self, name):
        Head.__init__(self)
        Body.__init__(self)
        self.physical = True   
        self.psyhologic = 100  
        self.name = name       
        self.last_state = 'Пытается родиться...'  
        if -90 < self.agle < 90:
            self.last_state = f'Родился {self.name}! С {self.hand_count} руками и {self.leg_count} ногами.'
            self.live = True
            self.x_coord = random.randint(0, 200)
            self.y_coord = random.randint(0, 200)
        else:
            self.last_state = 'Мертворожденный'
            self.live = False

    def get_step(self):                                
        if self.leg_count > 1:
            if self.direction == 0:
                self.x_coord += 5
                if self.x_coord >= 400:
                    self.last_state = 'Дальше стена.'
                    self.x_coord -= 5
                    return
            elif self.direction == 90:
                self.y_coord += 5
                if self.y_coord >= 400:
                    self.last_state = 'Дальше стена.'
                    self.y_coord -= 5
                    return
            elif self.direction == 180:
                self.x_coord -= 5
                if self.x_coord <= 0:
                    self.last_state = 'Дальше стена.'
                    self.x_coord += 5
                    return
            elif self.direction == 270:
                self.y_coord -= 5
                if self.y_coord <= 0:
                    self.last_state = 'Дальше стена.'
                    self.x_coord += 5
                    return
            self.last_state = f'Человек сделал шаг. Теперь он здесь х = {self.x_coord} ; y = {self.y_coord}'
        else:
            self.psyhologic -= 10
            msg = 'Без ног ' if self.leg_count < 1 else 'С одной ногой '
            self.last_state = msg + 'тяжело длать шаги. Ты упал. Ты подавлен. Псих.здоровье -10. Береги себя.'

    def look_around(self, item):
        dist = abs(item.x_coord - self.x_coord) // 5 + abs(item.y_coord - self.y_coord) // 5
        self.last_state = f'Предмет находится в {dist} шагах x = {item.x_coord} ; y = {item.y_coord}.'

    def inventory(self):
        if not self.in_hand:
            self.last_state = 'Ты ни чем не обладаешь.'
            return
        self.last_state = 'Инвентарь:\r\n'
        for i in self.in_hand:
            self.last_state += '- ' + i + '\r\n'
        self.last_state = self.last_state[:-2]


class TheGame:

    def __init__(self) -> None:
        self.start_time = time()
        self.history = ""
        self.banner = ""
        self.stage = 0
        self.clear_release = True
        self.prompt = 'what? : '
        
        self.STARTING_ACTIONS = {
            '1': (self.try_born, "Попытаться родиться"),
            '2': (self.bye, "Выход"),
        }
    
        self.RUNNING_ACTIONS = {
            '1': (self.make_step, "Сделать шаг"),
        }
    
    async def try_born(self):
        self.history += "Как назовем первинца?\r\n"
        self.clear_task.cancel()
        await asyncio.sleep(.1)
        self.prompt = "Имя? : "
        self.clear_task = asyncio.create_task(self.clear_screen(prompt=self.prompt))
    
    def make_step(self):
        pass
    
    async def wait_input(self):
        loop = asyncio.get_running_loop()
        while True:
            user_input = await loop.run_in_executor(None, input)
            if self.stage:
                action = (
                    self.RUNNING_ACTIONS.get(user_input)[0] if \
                        self.RUNNING_ACTIONS.get(user_input) else None
                )
                if action:
                    if asyncio.iscoroutinefunction(action):
                        task = asyncio.create_task(action())
                    else:
                        action()
                else:
                    self.history += "\r\nА нука, попробуй еще раз..."
            else:
                action = (
                    self.STARTING_ACTIONS.get(user_input)[0] if \
                        self.STARTING_ACTIONS.get(user_input) else None
                )
                if action:
                    if asyncio.iscoroutinefunction(action):
                        task = asyncio.create_task(action())
                    else:
                        action()
                else:
                    if 'Имя' in self.prompt:
                        man = Man(user_input)
                        self.history += man.last_state + '\r\n'
                        if not man.live:
                            self.history += "Увы... давай попробуем снова\r\n"
                        else:
                            self.stage = 1
                    else:
                        self.history += "А нука, попробуй еще раз...\r\n"
            
    async def clear_screen(self, prompt="Что делаем? : "):
        try:
            while self.clear_release:
                os.system('cls||clear')
                self.banner = ""
                self.banner += GAME_NAME + '\r\n'
                self.banner += self.history + '\r\n'
                ellepsed = time() - self.start_time
                self.banner += (
                    f"{'Игра длится: ':>65}{str(int(ellepsed)):>5}s\r\n"
                )
                if self.stage:
                    self.banner += RUNNING_MENU
                else:
                    self.banner += BORN_MENU
                line_buff = readline.get_line_buffer()
                self.banner += prompt + line_buff
                print(self.banner, end="")
                await asyncio.sleep(1)
        except CancelledError:
            pass
        
    def bye(self):
        print('\r\nРано сдался...\r\n')
        sys.exit(0)
    
    async def main_loop(self):
        
        self.input_task = asyncio.create_task(self.wait_input())
        self.clear_task = asyncio.create_task(self.clear_screen())
        await asyncio.gather(self.input_task, self.clear_task) 
    
    def run_the_game(self):
        try:
            asyncio.run(self.main_loop())
        except KeyboardInterrupt:
            self.bye()
        except SystemExit:
            pass


g = TheGame()
g.run_the_game()