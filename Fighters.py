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
    def levelup(self,addlevel=1):
        if addlevel!=1:
            self.expMax = 50 *(addlevel+1)
            self.level = addlevel
            self.health = self.level*100
            self.maxHealth = self.health
            self.exp = 0
            self.defense=5*self.level
            return
        while self.exp >= self.expMax:
            print(f'\n{self.name} has leveled up to {formatComma(self.level+1)}') 
            self.level+=1
            self.health = self.level*100
            self.maxHealth = self.health
            self.exp -= self.expMax
            self.expMax+=50
            self.defense+=5
    def attack(self,other,turn):
        player = self
        lineWriter(f'->[{player.name}\'s turn]<-\n')
        time.sleep(0.45)
        
        damage = 0
        criticalHit = False
        used = False
        if player.hasItem():
            if player.canUse():
                if player.primary.durability==player.primary.maxDurability or turn == 1:
                    lineWriter(f'{player.name} equips {player.primary.name} (Damage: {formatComma(player.primary.damage)}, Durability: {formatComma(player.primary.durability)}/{formatComma(player.primary.maxDurability)})')
                    time.sleep(0.5)
                damage = player.primary.use(player)
                used = True
        damage += ((player.level*15)-other.defense) + (random.randint(1,5*player.level))
        if player.critical(other):
            lineWriter(f'{player.name}: {criticalQuotes(player)}',0.035)
            time.sleep(0.5)
            criticalHit = True
            damage = round(abs(damage*2))
        if other.dodge():
            lineWriter(f'{other.name}: {dodgeQuotes(other)}',0.017)
            lineWriter(f'{other.name} dodges a{criticalCheck(criticalHit)} strike from {player.name}')
            time.sleep(0.5)
            if used == True and player.primary.durability<=0:
                lineWriter(f'{self.name}\'s {self.primary.name} has been broken...',0.032)
            return
        if damage < 0:
            damage = 1
        lineWriter(f'[{formatComma(player.health)}/{formatComma(player.maxHealth)} HP] {player.name} deals {formatComma(damage)}{criticalCheck(criticalHit)} damage to {other.name} [{formatComma(other.health)}/{formatComma(other.maxHealth)} HP] ')

        other.health-=damage
        if used == True and player.primary.durability<=0:
            lineWriter(f'{self.name}\'s {self.primary.name} has been broken...',0.032)   
        if (not other.alive()):
            player.exp+=other.level * 50+50
            print("")
            lineWriter(f'{other.name}: {deathQuotes(other)}',0.05)
            time.sleep(0.25)
            lineWriter(f'{other.name} has fallen\n',0.1)
            lineWriter(f'{player.name} gains {formatComma(other.level*50+50)} exp!' )
            player.levelup()
            other.killer = player
    def critical(self,other):
        x = [True,False,False,False,False,False,False,False]
        if self.level-other.level >= 10:
            return True
        x = random.choice(x)
        return x 
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
    def canUse(self):
        if self.level>=self.primary.lvlReq and not self.primary.isBroken():
            return True
        return False
    def hasItem(self):
        if self.inventory!=[]:
            for x in self.inventory:
                if not x.isBroken():
                    self.primary=x
                    return True
            return True
        return False
    def addItem(self,item):
        self.inventory.append(item)
    def listItems(self):
        listofItems = ''
        for x in self.inventory:
            listofItems+=x.isBroken(True)+x.name+', '
        return listofItems[0:len(listofItems)-2]
    def __str__(self):
        print("\n------------------------------")

        text = (f"Profile: {self.name}\n\nLevel: {formatComma(self.level)}\nHealth: {formatComma(self.health)}/{formatComma(self.maxHealth)}\nDefense: {formatComma(self.defense)}\nExp: {formatComma(self.exp)}/{formatComma(self.expMax)}\nWins: {formatComma(self.wins)}\nInventory: [")
        if self.hasItem():
            text+=self.listItems()
        text+=']\n'
        if not self.alive():
            deadtext = (f"\nStatus: Dead, killed by Level {formatComma(self.killer.level)} {self.killer.name}")
            text+=deadtext
        else:
            alivetext = (f"\nStatus: Alive")
            text+=alivetext
        text+=("\n------------------------------")
        return text
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
            return self.damage
        return 0

        return self.damage
    def isBroken(self,display = False):
        if self.durability <=0:
            if display == True:
                return 'Broken '
            return True
        if display == True:
            return ''
        return False
    def repairItem(self):
        self.durability = self.maxDurability

#Level and General code
def recoverAll(aftermath):
    for players in aftermath:
        players.restorehealth()
def levelAdd(fighters,levelDesired):
    if levelDesired>=1:
        for fighter in fighters:
            x = round(50*(levelDesired*(levelDesired+1)/2))
            x-=50
            fighter.exp+=x
            fighter.levelup(levelDesired)

def lineWriter(text,delay = 0.012,noLine = False):
    for letter in text:
        print(letter,end='')
        sys.stdout.flush()
        time.sleep(delay)
    if noLine ==False:
        print("")    
def printStats(fighters):
    for fighter in fighters:
        lineWriter(str(fighter),0.006)
def formatComma(number):
    return "{:,}".format(number)
def characterCreation():
    creators = []
    x = ''
    print("Enter your fighters names (Type 'stop' to stop)")
    while x != 'stop' and len(creators)<32:
        x = input(">")
        if x =='tester':
            creators.append(player("Nirojan"))
            creators.append(player("Navneet"))
            creators.append(player("Himanshu"))
            creators.append(player("Anantbir"))
            creators.append(player("Manav"))
            creators.append(player("Liam"))
            creators.append(player("Inder"))
            creators.append(player("Daksham"))
            alphalinewriter(["Adding Nirojan","Adding Navneet","Adding Himanshu","Adding Anantbir","Adding Manav","Adding Liam","Adding Inder","Adding Daksham"])
            for x in creators:
                x.addItem(item("Phoenix Slayer",50,50,1))
                x.addItem(item("Shotgun",20,50,1))
                x.addItem(item("Excalibur",100,100,1))
                x.addItem(item("Sniper",200,60,1))
            print("")
            return creators
        else:
            if x !='stop' and x!=' ':
                x = player(x)
                creators.append(x)
                #lineWriter(str(x),0.0001)
    return creators
def teamCreation(name,fighters):
    levels = 0
    for x in fighters:
        levels+=x.level
    return player(name,100*levels,levels,0,0,5*levels)
#Combat code

#Various quotes depending on the damage/death/dodge rates
def criticalQuotes(player):
    if player.name == 'Dio':
        return random.choice(["ZA WARUDO","ROAD A ROLLAR DAH","WRYYYYY","KISAMAAAAA","Ohoho, you dare approach me?","Hinjaku! Hinjaku!","It Was me, Dio!","Muda! Muda! Muda! Muda! Muda!","Good bye Jojo"])
    elif player.name == 'Jotaro':
        return random.choice(['Yare yare daze',"STAR PLATIUNUM","Here's your receipt","Your crime can't be paid with money","JAGARS"])
    dialogue = [
    "One of us has to die...","You will not live to see another day","I'll keep it simple",
    "Pick a god and pray...","I didn't want to do this...","You're already dead.","I promise you won't leave in one piece",
    "Don't waste my time.","I'll promise a swift death","Any last words?","Pay with your life","You're not worth my time",
    "Start booking your funeral","I'll send you to hell","Just so you know, this isn't personal",
    "Nothing personal kid","Don't take this personal","I'll make this quick","No one to save you now","Losing my patience",
    "Pathetic","It didn't have to be this way"]
    return random.choice(dialogue)
def criticalCheck(check):
    if check == True:
        return ' critical'
    else:
        return ''
def deathQuotes(player):
    dialogue = ["Not like this","NOOOOOOOOOOO","Impossible....","I...I never thought you'd be this good...","To end... like this?","What? Huh? What's happening?","NO! No, no, no!","No, no, no... I can't die like this",f"I'm sorry{random.choice([' mother...',' father...'])}","Why now....?","I was so close","I failed my family...","Goodbye...","..."]
    return random.choice(dialogue)
def dodgeQuotes(player):
    dialogue = ["You fool","Not even close", "Too slow", "I saw that from a mile away","You think that was going to hit me??","Miss me with that?","PIKACHU USE DODGE","was that ur best?","even my grandma could dodge that","you call that an attack?","are you even trying to hurt me?","Please...like that would ever hit me",f"I can be {random.choice(['sleeping','blind','crippled','disabled','knocked out','drunk','chained'])} and you still can't hit me"]
    return random.choice(dialogue)  
#Combat between two people
def combat(fighter1,fighter2):
    if (fighter1 == fighter2):
        return
    turn = 1
    lineWriter(f'[{fighter1.name} vs. {fighter2.name}]')
    while fighter1.health > 0 and fighter2.health > 0:
        lineWriter(f'\nTurn {turn}\n')
        fighter1.attack(fighter2,turn)
        print("")
        time.sleep(0.5)
        if fighter2.health <= 0:
            fighter1.wins+=1
            return fighter1
        fighter2.attack(fighter1,turn)
        print("")
        time.sleep(0.5)
        if fighter1.health <= 0:
            fighter2.wins+=1
            return fighter2
        turn+=1
    return
#Tournament Code in powers of 2 only
def tournament(fighters):
    if not math.log(len(fighters), 2).is_integer():
        print("Currently not compatiable with numbers that are not of the second power")
        return 0
    winners = []
    matches = 1
    rounds = 1
    eliminated = []
    while True:
        start = rounds
        if rounds == 1:
            for y in fighters:
                lineWriter(str(y),0.006)
            time.sleep(1)
            lineWriter("Let the games begin...\n",0.064)
            time.sleep(2)
            os.system('cls')
        lineWriter(f"Round {rounds}\n")
        matches+=standings(fighters,matches)
        while start == rounds:
            fighter1 = fighters[0]
            fighter2 = fighters[1]
            winner = combat(fighter1,fighter2)
            winners.append(winner)
            if fighter1 != winner:
                eliminated.append(fighter1)
            else:
                eliminated.append(fighter2)
            fighters.pop(0)
            fighters.pop(0)
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
            lineWriter(f"Up next: Level {formatComma(fighters[0].level)} {fighters[0].name} vs Level {formatComma(fighters[1].level)} {fighters[1].name}\n")
            time.sleep(5)
def standings(fighters,matches):
    x=0
    while x<=len(fighters)-1:
        lineWriter(f'|Match {matches}: {fighters[x].name} vs. {fighters[x+1].name}|')
        time.sleep(0.5)
        x+=2
        matches+=1
    time.sleep(2)
    print("\n")
    return matches-1

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
    standings = tournament(fighters)
    if standings != 0:
        printStats(standings)
    return
main()