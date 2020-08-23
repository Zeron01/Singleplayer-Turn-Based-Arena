import random
import time
import sys
import os
import math
from doublelinecode import alphalinewriter
class player:
    def __init__(self,name,health = 100,level = 1, exp = 0,expMax = 100,defense = 0):
        self.name = name
        self.health = health
        self.level = level
        self.inventory = []
        self.exp = exp
        self.expMax = expMax
        self.maxHealth = self.health
        self.wins = 0
        self.defense = defense
        self.killer = "None"
        self.primary = item("Nothing",0,0)
    def levelup(self,noprint=False):
        while self.exp >= self.expMax:
            if noprint == False:
                print(f'\n{self.name} has leveled up to {formatComma(self.level+1)}') 
            self.level+=1
            self.health = self.level*100
            self.maxHealth = self.health
            self.exp -= self.expMax
            self.expMax+=50
            self.defense=round(((self.level**1.45)/2)*(10/self.level**1.2))*2
    def dodge(self):
        x = random.choice([True,False,False,False,False,False,False,False])
        return x
    def alive(self):
        if self.health <=0:
            self.health = 0
            return False
        return True
    def restorehealth(self):
        self.health = self.maxHealth
    def critical(self,other):
        x = [True,False,False,False,False,False,False,False]
        if self.level%other.level >= 10:
            x.pop(-1)
            x.pop(-1)
            x.pop(-1)
            x.pop(-1)
            x.pop(-1)
            x.pop(-1)
        x = random.choice(x)
        return x
    def canUse(self):
        if self.level>=self.primary.lvlReq and not self.primary.isBroken():
            return True
        return False
    def __str__(self):
        print("\n------------------------------")

        text = (f"Profile: {self.name}\n\nLevel: {formatComma(self.level)}\nHealth: {formatComma(self.health)}/{formatComma(self.maxHealth)}\nDefense: {formatComma(self.defense)}\nExp: {formatComma(self.exp)}/{formatComma(self.expMax)}\nWins: {formatComma(self.wins)}\n")
        if not self.alive():
            deadtext = (f"\nStatus: Dead, killed by Level {formatComma(self.killer.level)} {self.killer.name}")
            text+=deadtext
        else:
            alivetext = (f"\nStatus: Alive")
            text+=alivetext
        text+=("\n------------------------------")
        return text
    def hasItem(self):
        if self.inventory!=[]:
            self.primary = self.inventory[0]
            return True
        return False
    def addItem(self,item):
        self.inventory.append(item)
class item:
    def __init__(self,name="None",damage=0,durability=0,lvlReq=1):
        self.name = name
        self.damage = damage
        self.durability = durability
        self.lvlReq = lvlReq
        self.maxDurability = self.durability
    def use(self,user):
        if not self.isBroken() and user.level>=self.lvlReq:
            self.durability-=10
            if self.durability<=0:
                print(f'!!{self.name} has one use left!!')
            return self.damage
        return 0

        return self.damage
    def isBroken(self):
        if self.durability <=0:
            return True
        return False
    def repairItem(self):
        self.durability = self.maxDurability

#Level and General code
def recoverAll(aftermath):
    for players in aftermath:
        players.restorehealth()
def grindLvl(fighters):
    for fighter in fighters:
        while fighter.health > 0 and fighter.wins <1000:
            fighter.restorehealth()
            x = player("Dummy",100,10)
            # if len(fighters) ==2:
            #     x = player("Dummy",1300,13,550,700,1300)
            combat(fighter,x)
            # if fighter.health <= 0:
            #     print("LOL YOU DIED BEFORE TOURNEY STARTED")
            #     time.sleep(0.5)
            recoverAll([fighter])
    return fighters
def addExp(fighters,exp):
    for fighter in fighters:
        fighter.exp+=exp
        fighter.levelup(True)
def levelAdd(fighters,levelDesired):
    if levelDesired>=1:
        for fighter in fighters:
            x = round(50*(levelDesired*(levelDesired+1)/2))
            x-=50
            addExp([fighter],x)

def lineWriter(text,delay = 0.004):
    for letter in text:
        print(letter,end='')
        sys.stdout.flush()
        time.sleep(delay)
    print("")    
def printStats(fighters):
    for fighter in fighters:
        lineWriter(str(fighter))
def formatComma(number):
    return "{:,}".format(number)
def characterCreation():
    creators = []
    x = ''
    print("Enter your fighters names (Type 'n' to stop)")
    while x != 'n' and len(creators)<4:
        x = input(">")
        if x =='tester':
            creators.append(player("Nirojan"))
            creators.append(player("Dev"))
            creators.append(player("Raghav"))
            creators.append(player("Slade"))
            # creators.append(player("Tashan"))
            # creators.append(player("Balraj"))
            # creators.append(player("Amit"))
            # creators.append(player("Vraj"))
            alphalinewriter(["Adding Nirojan","Adding Dev","Adding Raghav","Adding Slade"])
            print("")
            time.sleep(4)
            return creators
        else:
            if x !='n':
                x = player(x)
                creators.append(x)
                lineWriter(str(x))
    return creators

#Combat code

#Various quotes depending on the damage/death/dodge rates
def criticalQuotes(player):
    if player.name == 'Dio':
        return random.choice(["ZA WARUDO","ROAD A ROLLAR DAH","WRYYYYY","KISAMAAAAA","Ohoho, you dare approach me?","Hinjaku! Hinjaku!","It Was me, Dio!","Muda! Muda! Muda! Muda! Muda!","Good bye Jojo"])
    elif player.name == 'Jotaro':
        return random.choice(['Yare yare daze',"STAR PLATIUNUM","Here's your receipt","Your crime can't be paid with money"])
    dialogue = ["One of us has to die","I'll have your head","I'll keep it simple","Pick a god and pray...","I didn't want to do this...","You're already dead.","I promise you this will hurt","Don't waste my time.","I'll promise a swift death","Any last words?","Pay with your life","You're not worth my time","Start booking your funeral","Tell Satan I'm waiting","Just so you know, this isn't personal","Nothing personal kid","Don't take this personal","I'll make this quick","No one to save you now..."]
    return random.choice(dialogue)
def criticalCheck(check):
    if check == True:
        return ' critical'
    else:
        return ''
def deathQuotes(player):
    dialogue = ["Not like this","NOOOOOOOOOOO","Impossible....","I...I never thought you'd be this good...","To end... like this?","What? Huh? What's happening?","NO! No, no, no!","No, no, no... I can't die like this","I'm sorry...","Why now....?","I was so close","I failed my family...","Goodbye...","..."]
    return random.choice(dialogue)
def dodgeQuotes(player):
    dialogue = ["You fool","Not even close", "Too slow", "I saw that from a mile away","You think that was going to hit me??","Miss me with that?","PIKACHU USE DODGE","was that ur best?","even my grandma could dodge that","you call that an attack?","are you even trying to hurt me?","Please...like that would ever hit me"]
    return random.choice(dialogue)  
#Combat Code for specifically one person

def attack(player,other,turn):
    # if other.dodge():
    #     if other.name != 'Dummy' and player.name!= 'Dummy':
    #         lineWriter(f'{other.name}: {dodgeQuotes(other)}',0.0025)
    #         lineWriter(f'[{formatComma(other.health)}/{formatComma(other.maxHealth)} HP] {other.name} dodges a strike from {player.name} [{formatComma(player.health)}/{formatComma(player.maxHealth)} HP] ')
    #         time.sleep(0.5)
    #     return
    damage = 0
    criticalHit = False
    if player.hasItem():
        if player.canUse():
            if other.name != 'Dummy' and player.name!= 'Dummy':
                if turn == 1:

                    lineWriter(f'{player.name} equips {player.primary.name} (Damage: {formatComma(player.primary.damage)}, Durability: {formatComma(player.primary.durability)}/{formatComma(player.primary.maxDurability)})')
                    time.sleep(0.5)
            damage = player.primary.use(player)
    damage += ((player.level*30)-round(other.defense/4)) + (random.randint(0,10*player.level))
    if player.critical(other):
        if other.name != 'Dummy' and player.name!= 'Dummy':
            lineWriter(f'{player.name}: {criticalQuotes(player)}',0.05)
            #lineWriter(f"{player.name} begins charging his attack...",0.032)
            time.sleep(0.5)
        criticalHit = True
        damage = round(abs(damage*1.5))
    if other.dodge():
        if other.name != 'Dummy' and player.name!= 'Dummy':
            lineWriter(f'{other.name}: {dodgeQuotes(other)}',0.0025)
            #lineWriter(f'[{formatComma(other.health)}/{formatComma(other.maxHealth)} HP] {other.name} dodges a{criticalCheck(criticalHit)} strike from {player.name} [{formatComma(player.health)}/{formatComma(player.maxHealth)} HP] ')
            lineWriter(f'{other.name} dodges a{criticalCheck(criticalHit)} strike from {player.name}')
            time.sleep(0.5)
        return
    if damage < 0:
        damage = 1
    if other.name != 'Dummy' and player.name!= 'Dummy':
        lineWriter(f'[{formatComma(player.health)}/{formatComma(player.maxHealth)} HP] {player.name} deals {formatComma(damage)}{criticalCheck(criticalHit)} damage to {other.name} [{formatComma(other.health)}/{formatComma(other.maxHealth)} HP] ')

    other.health-=damage
    
    if (not other.alive()):
        player.exp+=other.level * 50
        if other.name != 'Dummy' and player.name!= 'Dummy':
            print("")
            lineWriter(f'{other.name}: {deathQuotes(other)}',0.05)
            time.sleep(0.25)
            lineWriter(f'{other.name} has fallen\n',0.1)
            lineWriter(f'{player.name} gains {formatComma(other.level*50)} exp!' )
        player.levelup()
        other.killer = player
#Combat between two people
def combat(fighter1,fighter2):
    x = 0
    if (fighter1 == fighter2):
        return
    turn = 1
    if fighter1.name != 'Dummy' and fighter2.name!= 'Dummy':
        x = 0.5
        lineWriter(f'[{fighter1.name} vs. {fighter2.name}]')

    while fighter1.health > 0 and fighter2.health > 0:
        if fighter1.name != 'Dummy' and fighter2.name!= 'Dummy':
            lineWriter(f'\n>Turn {turn}\n')
        attack(fighter1,fighter2,turn)
        print("")
        time.sleep(x)
        if fighter2.health <= 0:
            #print(f"\n{fighter1.name} has won")
            fighter1.wins+=1
            # if fighter1.name != 'Dummy' and fighter2.name!= 'Dummy':
            #     print("\n")
            return fighter1
        attack(fighter2,fighter1,turn)
        print("")
        time.sleep(x)
        if fighter1.health <= 0:
            #print(f"\n{fighter2.name} has won")
            fighter2.wins+=1
            # if fighter1.name != 'Dummy' and fighter2.name!= 'Dummy':
            #     print("\n")
            return fighter2
        # if fighter1.name != 'Dummy' and fighter2.name!= 'Dummy':
        #     print("\n")
        turn+=1
    return
#Tournament Code in powers of 2 only
def tournament(fighters):
    if not math.log(len(fighters), 2).is_integer():
        print("Currently not compatiable with numbers that are not of the second power")
        return 0
    winners = []
    y = 0
    rounds = 1
    eliminated = []
    while True:
        lineWriter(f"Round {rounds}\n")
        x = 0
        start = rounds
        while start == rounds:
            fighter1 = fighters[x]
            fighter2 = fighters[x+1]
            winner = combat(fighter1,fighter2)
            winners.append(winner)
            if fighter1 != winner:
                eliminated.append(fighter1)
            else:
                eliminated.append(fighter2)
            fighters.pop(x)
            fighters.pop(x)
            if len(fighters) == 0 and len(winners) >= 2:
                for fighter in winners:
                    fighters.append(fighter)
                winners = []
                recoverAll(fighters)
                rounds+=1
            elif len(winners) == 1 and len(fighters) == 0:
                lineWriter(f"Winner of tournmanet is: {winner.name}")
                eliminated.append(winners[0])
                return eliminated
            lineWriter(f"Up next: Level {formatComma(fighters[x].level)} {fighters[x].name} vs Level {formatComma(fighters[x+1].level)} {fighters[x+1].name}\n")
            time.sleep(5)

#Main function
def main():
    os.system('cls')
    time.sleep(0.25)
    fighters = characterCreation()
    if len(fighters) <= 1:
        lineWriter("Please add more than one player you doofus",0.016)
        time.sleep(0.5)
        os.system('cls')
        main()
        return
    else:
        while True:
            lineWriter('What level would you like to start the fighters?')
            try:
                startingLevel = int(input(">"))
                if startingLevel <1:
                    print("Please enter a valid input")
                else:
                    levelAdd(fighters,startingLevel)
                    break
            except:
                lineWriter("Please enter a valid input")
            
    os.system('cls')
    lineWriter("The real game will now begin (Correct Q3 on final)")
    time.sleep(2)
    os.system('cls')
    standings = tournament(fighters)
    if standings != 0:
        printStats(standings)
    return


main()