import random
import time
import sys
import os
import math

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
    def levelup(self,addlevel=1,display = True):
        if addlevel!=1:
            self.expMax = 50 *(addlevel+1)
            self.level = addlevel
            self.health = self.level*100
            self.maxHealth = self.health
            self.exp = 0
            self.defense=5*self.level
            return
        while self.exp >= self.expMax:
            if display == True:
                lineWriter(f'\n{self.name} has leveled up to {formatComma(self.level+1)}') 
            self.level+=1
            self.health = self.level*100
            self.maxHealth = self.health
            self.exp -= self.expMax
            self.expMax+=50
            self.defense+=5
    def attack(self,other,turn=1,speed=False):
        player = self
        lineWriter(f'->[{player.name}\'s turn]<-\n')
        if(speed == False):
            time.sleep(0.45)
        
        damage = 0
        criticalHit = False
        used = False
        if player.hasItem():
            if player.canUse():
                if player.primary.durability==player.primary.maxDurability or turn == 1:
                    lineWriter(f'{player.name} equips {player.primary.name} (Damage: {formatComma(player.primary.damage)}, Durability: {formatComma(player.primary.durability)}/{formatComma(player.primary.maxDurability)})')
                    if(speed == False):
                        time.sleep(0.5)
                damage = round(player.primary.use(player)*(player.level)*0.25)
                used = True
        damage += ((player.level*15)-other.defense) + (random.randint(1,5*player.level))
        if player.critical(other):
            lineWriter(f'{player.name}: {criticalQuotes()}',0.035)
            if(speed == False):
                time.sleep(0.5)
            criticalHit = True
            damage = round(abs(damage*2))
        if other.dodge():
            lineWriter(f'{other.name}: {dodgeQuotes()}',0.017)
            lineWriter(f'{other.name} dodges a{criticalCheck(criticalHit)} strike from {player.name}')
            if(speed == False):
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
            lineWriter(f'\n{other.name}: {deathQuotes()}',0.05)
            if(speed == False):
                time.sleep(0.25)
            lineWriter(f'{other.name} has fallen\n',0.1)
            lineWriter(f'{player.name} gains {formatComma(other.level*50+50)} exp!' )
            player.levelup()
            other.killer = player
    def critical(self,other):
        x = [True,False,False,False,False,False,False,False] #1/8 chance of landing a critical
        if self.level-other.level >= 10:
            return True #If the difference of level is greater than/equal to 10, 100% critical chance
        x = random.choice(x)
        return x 
    def dodge(self):
        x = random.choice([True,False,False,False,False,False,False,False]) #1/8 chance of dodging
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
        text=("------------------------------\n")

        text += (f"Profile: {self.name}\n\nLevel: {formatComma(self.level)}\nHealth: {formatComma(self.health)}/{formatComma(self.maxHealth)}\nDefense: {formatComma(self.defense)}\nExp: {formatComma(self.exp)}/{formatComma(self.expMax)}\nWins: {formatComma(self.wins)}\nInventory: [")
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

def lineWriter(text,delay = 0.006,noLine = False):
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
    #lvl 5 at least to try these weapons
    items = [
        item("Steel Sword", 80, 150, 5),
        item("Legendary Sword", 120, 200, 5), 
        item("Shotgun",95,150,5),
        item("Legendary Sniper",120,150,5),
    ]
    x = ''
    print("Enter your fighters names (Type 'stop' to stop)")
    while x != 'stop':
        x = input(">")
        if(len(x) == 0):
            lineWriter("Please enter something")
            continue
        else:
            if x !='stop' and x!=' ':
                x = player(x)
                x.addItem(random.choice(items))
                creators.append(x)
                continue
        if((len(creators)<=1)):
            lineWriter(f"[Need at least 2 players] ")
            x = 0
    return creators
def teamCreation(name,fighters):
    levels = 0
    for x in fighters:
        levels+=x.level
    return player(name,100*levels,levels,0,0,5*levels)
#Combat code

#Various quotes depending on the damage/death/dodge rates
def criticalQuotes():
    dialogue = [
        "One of us has to die...",
        "You will not live to see another day",
        "I'll keep it simple",
        "Pick a god and pray...",
        "I didn't want to do this...",
        "You're already dead.",
        "I promise you won't leave in one piece",
        "Don't waste my time.",
        "I'll promise a swift death",
        "Any last words?",
        "Pay with your life",
        "You're not worth my time",
        "Start booking your funeral",
        "I'll send you to hell",
        "Just so you know, this isn't personal",
        "Nothing personal kid",
        "Don't take this personal",
        "I'll make this quick",
        "No one to save you now",
        "Losing my patience",
        "Pathetic",
        "It didn't have to be this way"
        ]
    return random.choice(dialogue)
def criticalCheck(check):
    if check == True:
        return ' critical'
    else:
        return ''
def deathQuotes():
    dialogue = [
        "Not like this",
        "NOOOOOOOOOOO",
        "Impossible....",
        "I...I never thought you'd be this good...",
        "To end... like this?",
        "What? Huh? What's happening?",
        "NO! No, no, no!",
        "No, no, no... I can't die like this",
        f"I'm sorry{random.choice([' mother...',' father...'])}",
        "Why now....?",
        "I was so close",
        "I failed my family...",
        "Goodbye...",
        "..."
        ]
    return random.choice(dialogue)
def dodgeQuotes():
    dialogue = [
        "You fool",
        "Not even close", 
        "Too slow", 
        "I saw that from a mile away",
        "You think that was going to hit me??",
        "Miss me with that?",
        "PIKACHU USE DODGE",
        "was that ur best?",
        "even my grandma could dodge that",
        "you call that an attack?",
        "are you even trying to hurt me?",
        "Please...like that would ever hit me",
        f"I can be {random.choice(['sleeping','knocked out','chained'])} and you still can't hit me"
        ]
    return random.choice(dialogue)  
#Combat between two people
def combat(fighter1,fighter2,fast = False):
    if(fast == False):
        speed = 0.45
    else:
        speed=0
    if (fighter1 == fighter2):
        return
    turn = 1
    lineWriter(f'[{fighter1.name} vs. {fighter2.name}]')
    while fighter1.health > 0 and fighter2.health > 0:
        lineWriter(f'\nTurn {turn}\n')
        fighter1.attack(fighter2,turn,fast)
        print("")
        time.sleep(speed)
        if fighter2.health <= 0:
            fighter1.wins+=1
            return fighter1
        fighter2.attack(fighter1,turn,fast)
        print("")
        time.sleep(speed)
        if fighter1.health <= 0:
            fighter2.wins+=1
            return fighter2
        turn+=1
    return
#Tournament Code
def tournament(fighters,fast=False):
    winners = []
    matches = 1
    rounds = 1
    eliminated = []
    while True:
        start = rounds
        if rounds == 1:
            if((len(fighters)<=1 or not math.log(len(fighters), 2).is_integer())):
                names = ""
                x = 2
                while(len(fighters)>=x):
                    x*=2
                byes = x - len(fighters)
                for _ in range(0,byes):
                    ahead = (fighters.pop(0))
                    ahead.exp = ahead.expMax #This will make sure it will be a fair battle for those in the 2nd round
                    ahead.levelup(1,False)
                    names+=ahead.name+", "
                    winners.append(ahead)
                names+="will progress to round two due to byes"
                lineWriter(names)
            time.sleep(1)
            lineWriter("Players will start with all the stats similar to this player")
            lineWriter(str(fighters[0]))
            lineWriter("\nLet the games begin...\n",0.064)
            time.sleep(2)
            os.system('cls')
        lineWriter(f"Round {rounds}\n")
        if(fast == True):
            speed = 0
        else:
            speed = 0.5
        matches+=standings(fighters,matches,speed)
        while start == rounds:
            fighter1 = fighters[0]
            fighter2 = fighters[1]
            #You can change speed by changing true for speed, false for default
            winner = combat(fighter1,fighter2,fast)
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
            if (fast==False):
                time.sleep(3)
def standings(fighters,matches,speed = 0.5):
    x=0
    while x<=len(fighters)-1:
        lineWriter(f'|Match {matches}: {fighters[x].name} vs. {fighters[x+1].name}|')
        x+=2
        matches+=1
    speed*=4
    time.sleep(speed)
    print("\n")
    return matches-1
def levelChoose(fighters):
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
def speedUpGame():
    while True:
        lineWriter('Would you like to speed up the games? (y/n)')
        try:
            speed = input(">")
            if speed =="y":
                return True
            elif speed=="n":
                return False
            else:
                lineWriter('Enter valid choice please')
        except Exception:
            lineWriter("Please enter a valid input")

#Main function
def main():
    os.system('cls')
    time.sleep(0.25)
    fighters = characterCreation()
    levelChoose(fighters)
    speed = speedUpGame()
    os.system('cls')
    standings = tournament(fighters, speed)
    printStats(standings)
    return
main()




