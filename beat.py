from random import random
from colorama import init, Fore
init(autoreset=True)

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

    def is_crit(self) -> bool:
        if random() <= self.CRIT_RATE:
            return True
        return False
    
    def is_vampirize(self) -> bool:
        if random() <= self.VAMPIRE_RATE:
            return True
        return False
    
    def printuwu(self, s, other):
        spaces = (41 - len(s)) * ' '
        hp1st = self.hp
        hp2nd = other.hp
        print(f'{s}{spaces} | {Fore.LIGHTRED_EX} {hp1st} | {hp2nd}')

    def __add__(self, other):
        if not other.alive:
            return 'finish'

        if self.is_vampirize():
            other.hp -= self.VAMPIRE_HP_STEAL
            self.hp += self.VAMPIRE_HP_STEAL
            print(f'{Fore.CYAN}{self.NAME} украл {self.VAMPIRE_HP_STEAL} здоровья у {other.NAME} |{Fore.LIGHTRED_EX} {self.hp} | {other.hp}')
        
        if self.is_crit():
            damage = self.CRIT_DMG
            other.hp -= damage
            print(f'{Fore.LIGHTGREEN_EX}{self.NAME} нанёс {damage} крит урона игроку {other.NAME} |{Fore.LIGHTRED_EX} {self.hp} | {other.hp}')
            self.hp += self.CRIT_HEAL
            print(f'{Fore.BLUE}{self.NAME} восстановил {self.CRIT_HEAL} хп')
        else:
            damage = self.DAMAGE
            other.hp -= damage
            print(f'{self.NAME} нанёс {damage} урона игроку {other.NAME} |{Fore.LIGHTRED_EX} {self.hp} | {other.hp}')
        
        
        if not other.alive:
            print(f"{Fore.YELLOW}{self.NAME} убил игрока {other.NAME}! |{Fore.LIGHTRED_EX} {self.hp}")

        
me = Person('Котейка')
nikita = Person('Никита')
me + nikita