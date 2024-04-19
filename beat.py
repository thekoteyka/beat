from random import random
from time import sleep

# Может работать без colorama (Не рекомендую)
try:
    from colorama import init, Fore
    init(autoreset=True)
    max_spaces_fore = 31
except:
    class EmergencyFore():
        YELLOW          = ''
        BLUE            = ''
        CYAN            = ''
        LIGHTRED_EX     = ''
        LIGHTGREEN_EX   = ''
        LIGHTWHITE_EX   = ''
        LIGHTCYAN_EX    = ''
    Fore = EmergencyFore()
    max_spaces_fore = 26
    print('\n\n\n\n\nНе удалось подключить модуль colorama для цветново вывода, весь текст будет просто белым\nРекомендую \
установить модуль для красивого вывода.\nОтличать хп от щита также неудобно! Я предупредил\n\n\n')
    print('Продолжение через 10 секунд')
    sleep(10)

chase = 0
moves = 0


class Person:
    def __init__(self, NAME:str):
        self.NAME:str = NAME   # Имя персонажа
        self.MAX_HP =     100  # Максимальное здоровье, после которого пойдут щиты
        self.DEFAULT_HP = 100  # Здоровье по умолчанию (при старте игры либо после использования тоттема)
        self.hp:int = self.DEFAULT_HP  # Здоровье в текущий момент времени
        self.shield:int = 50   # Щит в начале игры и в текущий момент времени
        self.DAMAGE:int = 10   # Стандартный урон

        self.CRIT_RATE:float = 0.4 # Шанс критического попадания
        self.CRIT_DMG:int =    20  # Урон при критическом попадании
        self.CRIT_HEAL =       30  # Лечение при нанесении критического урона

        self.VAMPIRE_RATE:float =   0.1 # Шанс на кражу здоровья у дрогого игрока
        self.VAMPIRE_HP_STEAL:int = 10  # Количество украденого здоровья 

        self.BREAKDOWN_RATE:float = 0.1 # Шанс на разрушительную атаку
        
        self.alive:bool = True  # Жив ли игрок
        self.breakdowned:bool = False 
        
        self.totem_of_immortality:int = 1  # Количество Тотемов Бессметрия (Позволяет возродиться 1 раз)

    def is_crit(self) -> bool:  # Кританул ли
        if random() <= self.CRIT_RATE:
            return True
        return False
    
    def is_vampirize(self) -> bool:  # Украл здоровье ли
        if random() <= self.VAMPIRE_RATE:
            return True
        return False
    
    def is_breakdown(self) -> bool:
        if random() <= self.BREAKDOWN_RATE:
            return True
        return False 
    
    def printuwu(self, s, other):  # Особый вывод с показом здоровья справа
        s = str(s) # На всякий случай
        max_spaces = max_spaces_fore + len(self.NAME) + len(other.NAME) + 5 # Максимальная длинна строки
        spaces = (max_spaces - len(s)) * ' ' # Сколько осталось пробелов до макс длинны

        hp1st = self.hp  # Хп первого игрока
        hp2nd = other.hp # Хп второго игрока
        shield1st = self.shield
        shield2nd = other.shield


        # Даже не пытайся разобраться что тут происходит

        if chase == 0: # Чей ход
            spaces_between_hp = (3 - len(str(hp1st))) * ' '

            first = f'{Fore.LIGHTCYAN_EX} {shield1st}' if shield1st else f'{Fore.LIGHTRED_EX} {hp1st}'
            second = f'{Fore.LIGHTCYAN_EX} {shield2nd}' if shield2nd else f'{Fore.LIGHTRED_EX} {hp2nd}'
            print(f'{s}{spaces} | {first}{spaces_between_hp} | {second}')
        else:
            spaces_between_hp = (3 - len(str(hp2nd))) * ' '

            second = f'{Fore.LIGHTCYAN_EX} {shield1st}' if shield1st else f'{Fore.LIGHTRED_EX} {hp1st}'
            first = f'{Fore.LIGHTCYAN_EX} {shield2nd}' if shield2nd else f'{Fore.LIGHTRED_EX} {hp2nd}'
            print(f'{s}{spaces} | {first}{spaces_between_hp} | {second}')


    def die(self):  # Попробовать умереть
        if self.totem_of_immortality: # Если есть тоттем
            self.hp = self.DEFAULT_HP
            self.totem_of_immortality -= 1 # Забираем один тоттем
            print(f'{Fore.YELLOW}{self.NAME} использовал Тотем Бессмертия! Осталось: {self.totem_of_immortality}')
            return
        self.alive = False # Иначе персонаж погибает

    def damage_me(self, amount:int): # Нанести урон
        if self.shield:
            self.shield -= amount
            if self.shield < 0:
                self.hp -= abs(self.shield)
                self.shield = 0
            return
        self.hp -= amount
        if self.hp < 0: # Чтобы не было отрицательного хп
            self.hp = 0

    def heal_me(self, amount:int):
        if self.shield < 0:
            self.damage_me(abs(self.shield))
            self.shield = 0
        self.hp += amount
        if self.hp > self.MAX_HP:
            self.shield += self.hp - self.MAX_HP
            self.hp = self.MAX_HP
    
    def __add__(self, other): # персонаж (атакующий) + персонаж
        if self.breakdowned:
            self.printuwu(f'{Fore.CYAN}{self.NAME} поднялся с земли', other)
            self.breakdowned = False
            return
        
        if self.is_vampirize():
            other.damage_me(self.VAMPIRE_HP_STEAL)
            self.heal_me(self.VAMPIRE_HP_STEAL)
            self.printuwu(f'{Fore.CYAN}{self.NAME} украл {self.VAMPIRE_HP_STEAL} здоровья у {other.NAME}', other)
        
        if self.is_crit(): # Если кританул
            damage = self.CRIT_DMG
            other.damage_me(damage)
            self.printuwu(f'{Fore.LIGHTGREEN_EX}{self.NAME} нанёс {damage} крит урона игроку {other.NAME}', other)
            self.heal_me(self.CRIT_HEAL)
            self.printuwu(f'{Fore.BLUE}{self.NAME} восстановил {self.CRIT_HEAL} хп', other)
        else: # Если не кританул
            damage = self.DAMAGE
            other.damage_me(damage)
            self.printuwu(f'{Fore.LIGHTWHITE_EX}{self.NAME} нанёс {damage} урона игроку {other.NAME}', other)

        if self.is_breakdown():
            other.breakdowned = True
            self.printuwu(f'{Fore.CYAN}{self.NAME} нанёс пробивающий удар игроку {other.NAME}', other)
        
        if other.hp <= 0:
            other.die()
        
        if not other.alive: # Если противник не жив (то есть мёртв)
            self.printuwu(f"{Fore.YELLOW}{self.NAME} убил игрока {other.NAME} за {moves} ходов!", other)
            return 'finish'

        
firstPlayer = Person('Котейка')    # 1st
secondPlayer = Person('АЛИК')      # 2nd
result = None

while not result == 'finish':
    moves += 1
    if chase == 0:
        result = firstPlayer + secondPlayer
    else:
        result = secondPlayer + firstPlayer
    
    print()
    chase = 1 if chase == 0 else 0 # Смена хода
    sleep(2)

#test
