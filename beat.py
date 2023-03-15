from random import random
from colorama import init, Fore
from time import sleep
init(autoreset=True)
chase = 0
# last_hp_1st = 100
# last_hp_2nd = 100
class Person:
    def __init__(self, NAME:str):
        self.NAME:str = NAME
        self.hp:int = 100
        self.DAMAGE:int = 10

        self.CRIT_RATE:float = 0.4
        self.CRIT_DMG:int = 20
        self.CRIT_HEAL = 30

        self.VAMPIRE_RATE:float = 0.2
        self.VAMPIRE_HP_STEAL:int = 10
        
        self.alive:bool = True
        
        self.totem_of_immortality:int = 1

    def is_crit(self) -> bool:
        if random() <= self.CRIT_RATE:
            return True
        return False
    
    def is_vampirize(self) -> bool:
        if random() <= self.VAMPIRE_RATE:
            return True
        return False
    
    def printuwu(self, s, other):
        s = str(s)
        max_spaces = 28 + len(self.NAME) + len(other.NAME) + 5
        spaces = (max_spaces - len(s)) * ' '

        hp1st = self.hp
        hp2nd = other.hp

        if chase == 0:
            spaces_between_hp = (3 - len(str(hp1st))) * ' '
            print(f'{s}{spaces} | {Fore.LIGHTRED_EX} {hp1st}{spaces_between_hp} | {hp2nd}')
        else:
            spaces_between_hp = (3 - len(str(hp2nd))) * ' '
            print(f'{s}{spaces} | {Fore.LIGHTRED_EX} {hp2nd}{spaces_between_hp} | {hp1st}')

    def die(self):
        if self.totem_of_immortality:
            self.hp = 100
            self.totem_of_immortality -= 1
            print(f'{Fore.YELLOW}{self.NAME} использовал Тотем Бессмертия! Осталось: {self.totem_of_immortality}')
            return
        self.alive = False

    def damage_it(self, amount:int):
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0
    
    def __add__(self, other):
        if self.is_vampirize():
            other.damage_it(self.VAMPIRE_HP_STEAL)
            self.hp += self.VAMPIRE_HP_STEAL
            self.printuwu(f'{Fore.CYAN}{self.NAME} украл {self.VAMPIRE_HP_STEAL} здоровья у {other.NAME}', other)
        
        if self.is_crit():
            damage = self.CRIT_DMG
            other.damage_it(damage)
            self.printuwu(f'{Fore.LIGHTGREEN_EX}{self.NAME} нанёс {damage} крит урона игроку {other.NAME}', other)
            self.hp += self.CRIT_HEAL
            self.printuwu(f'{Fore.BLUE}{self.NAME} восстановил {self.CRIT_HEAL} хп', other)
        else:
            damage = self.DAMAGE
            other.damage_it(damage)
            self.printuwu(f'{Fore.LIGHTWHITE_EX}{self.NAME} нанёс {damage} урона игроку {other.NAME}', other)
        
        if other.hp <= 0:
            other.die()
        
        if not other.alive:
            self.printuwu(f"{Fore.YELLOW}{self.NAME} убил игрока {other.NAME}!", other)
            return 'finish'

        
me = Person('Котейка')    # 1st
nikita = Person('Никита') # 2nd
result = None

while not result == 'finish':
    if chase == 0:
        result = me + nikita
    else:
        result = nikita + me
    print()
    chase = 1 if chase == 0 else 0
    sleep(0.1)

    