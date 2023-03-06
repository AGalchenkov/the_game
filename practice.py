import random
import os
from time import sleep

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
        self.agle = random.randint(-120, 120)
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
        self.leg_count = random.choices([0, 1, 2], weights=[15, 20, 65])[0]


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
            print(self.last_state)
            self.live = True
            self.x_coord = random.randint(0, 200)
            self.y_coord = random.randint(0, 200)
        else:
            self.last_state = 'Мертворожденный'
            print(self.last_state)
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

def history_and_clear(history, man):
    history += man.last_state + '\r\n'
    os.system('cls||clear')
    return history

def bye():
    print('\r\nРано сдался...\r\n')
    exit()

def finish():
    history += man.last_state + '\r\n\r\n\r\n'
    del man
    os.system('cls||clear')

history = ''
banner = '''
##     ###### ##  ## ###### ##  ##  ####     ##     ###### ###### #####
##       ##   ##  ##   ##   ### ## ##        ##       ##   ##     ##   
##       ##   ##  ##   ##   ## ### ## ###    ##       ##   ####   #### 
##       ##    ####    ##   ##  ## ##  ##    ##       ##   ##     ##   
###### ######   ##   ###### ##  ##  ####     ###### ###### ##     #####
'''
born_menu = '''
    1. Попытаться родиться
    2. Выход
'''
second_menu = '''
    1. Сделать шаг
    2. Взять предмет
    3. Выбросить предмет
    4. Инвентарь
    5. Осмотреться в поисках предметов 
    6. Определить направление
    7. Изменить направление
    8. Выход
'''
os.system('cls||clear')
stage = 0
item = Item()
while True:
    print(banner)
    print(history)
    if stage > 0:
        if man.limbs < 2:
            man.last_state = 'C таким количеством конечностей не выживают... R.I.P'
            finish()
            stage = 0
            continue
        if man.psyhologic == 0:
            man.last_state = 'Ты выгорел... R.I.P'
            finish()
            stage = 0
            continue
        print(second_menu)
    else:
        print(born_menu)
        r = input('Что делаем?\r\n-> ')
        if r == '1':
            name = input('Имя: ')
            man = Man(name)
            if not man.live:
                print('Увы... через 5 сек. попробуем снова!')
                sleep(5)
                os.system('cls||clear')
                continue
            else:
                stage += 1
                history = history_and_clear(history, man)
                continue
        elif r == '2':
            bye()
    r = input('Что делаем?\r\n-> ')
    if r == '1':
        man.get_step()
        history = history_and_clear(history, man)
        continue
    elif r == '2':
        result, state = man.get_item(item)
        man.last_state = state
        if result:
            del item
            item = Item()
        history = history_and_clear(history, man)
        continue
    elif r == '3':
        man.last_state = man.drop_item()
        history = history_and_clear(history, man)
        continue
    elif r == '4':
        man.inventory()
        history = history_and_clear(history, man)
        continue
    elif r == '5':
        man.look_around(item)
        history = history_and_clear(history, man)
        continue
    elif r == '6':
        man.determine_direction()
        history = history_and_clear(history, man)
        continue
    elif r == '7':
        man.switch_direction()
        history = history_and_clear(history, man)
        continue
    elif r == '8':
        bye()


