#!/usr/bin/python2.7
import random
import math
import time
# Globals
MAP = [] # GRID OF MAP
# MAP LEXICON
GOLD = 'G' #Increase Money per Turn
IRON = 'I' #Better Army 
FOREST = 'F' #Better Workers

# generate MAP
def generateMap():
    global MAP
    global GOLD
    global IRON
    global FOREST
    for x in range (0,10):
        MAP.append([])
        for y in range (0,10):
            # Generate random map
            r = random.randrange(0,100)
            if r <= 45:
                MAP[x].append(' X ')
            elif r > 45 and r <= 60:
                MAP[x].append(' ' + GOLD + ' ')
            elif r > 60 and r <= 80:
                MAP[x].append(' ' + FOREST + ' ')
            elif r > 80 and r <= 100:
                MAP[x].append(' ' + IRON + ' ')

# Mark Map with Symbol
def markMap(x,y,s):
    global MAP
    MAP[x][y] =  s + MAP[x][y][1:]
    return MAP[x][y][1]
# print map, 10x10 grid
def printMap():
    global MAP
    print "~~~~~~~~~~~~~~~~~~~~\n\n"
    output = ''
    for x in MAP:
        for y in x:
            output += "  " + str(y) + "  " 
        output += "\n\n\n"
    print output
    print "~~~~~~~~~~~~~~~~~~~~"

def findClaims(s,claims):
    # takes symbol of empire and claims
    # returns the next best location for the empire
    global MAP 
    global FOREST
    global IRON
    global GOLD
    potClaims = [] 
    pot = 0
    for x,y in claims.iteritems():
        # top left
        for a in [[-1,0],[1,0],[0,-1],[0,1]]:
            if y[0] +a[0] >= 0 and y[1] + a[1] >=0 and y[0] + a[0] < 10 and y[1] + a[1] < 10:
                if s not in MAP[y[0]+a[0]][y[1]+a[1]]:
                    potClaims.append([y[0]+a[0],y[1]+a[1]])
    return potClaims

def valueClaim(claim,money,workers,forest,landInt, x=1,i=2,f=2,g=2,e=-5, pot=False,xp=0,ip=0,fp=0,gp=0,ep=0):
    # returns a value of how useful a piece of land is
    # changable for different bots
    global FOREST
    global GOLD
    global IRON
    # claim power, for every worker + forest, gain one power
    if forest - workers >= 0:
        power = workers
    elif forest - workers < 0:
        power = forest
    # extra cost for expansion
    landTax = int(math.floor(landInt/5))

    # PRICES
    forestPrice = 3 + landTax
    ironPrice = 4 + landTax
    goldPrice = 5 + landTax
    xPrice = 2 + landTax
    # set prices, return info
    if not pot:
        if claim[0] != ' ':
            # enemy!
            return [e,10000,False]
        elif FOREST in claim:
            if power + (money/5) >= forestPrice:
                return [f,forestPrice,True]
            else:
                return [f,forestPrice,False]
        elif GOLD in claim:
            if power + (money/5) >= goldPrice:
                return [g,goldPrice,True]
            else:
                return [g,goldPrice,False]
        elif IRON in claim:
            if power + (money/5) >= ironPrice:
                return [i,ironPrice,True]
            else:
                return [i,ironPrice, False]
        elif 'X' in claim: 
            if power + (money/5) >= xPrice:
                return [x,xPrice,True] 
            else:
                return [x,xPrice,False]
        else:
            return [-10000,1000]
    else:
        if claim[0] != ' ':
            # enemy!
            return ep
        elif FOREST in claim:
            return fp
        elif GOLD in claim:
            return gp
        elif IRON in claim:
            return ip
        elif 'X' in claim:
            return xp

# BOT WORK
class bot():
    # bot vars
    name = 'bot'
    symbol = 'X'
    # game vars
    money = 2
    workers = 0
    army = 0
    landInt = 1
    claims = {} 
    # WEIGHTS
    xW = 0
    fW = 0
    iW = 0
    gW = 0
    eW = 0
    xWP = 0
    fWP = 0
    iWP = 0
    gWP = 0
    eWP = 0
    # LAND CLAIMED
    cgold = 0
    cforest = 0
    ciron = 0
    # Supplies
    forest = 0
    iron = 0
    # set init variables
    def __init__(self,name, symbol, money,x,y):
        self.name = name
        self.symbol = symbol
        self.money = money
        self.claims = {}
        self.claims[0] = [x,y] 
        self.flag(markMap(x,y,symbol))
        self.xW = 0
        self.fW = 0
        self.iW = 0
        self.gW = 0
        self.eW = 0
        self.xWP = 0
        self.fWP = 0
        self.iWP = 0
        self.gWP = 0
        self.eWP = 0
        self.cgold = 0
        self.cforest = 0
        self.ciron = 0
        self.forest = 0
        self.iron = 0
    def setWeights(self, x,f,i,g,e,xp,fp,ip,gp,ep):
        # set weights for x, forest, iron, gold, enemy, and potentials
        self.xW = x
        self.fW = f
        self.iW = i
        self.gW = g
        self.eW = e
        self.xWP = xp
        self.fWP = fp
        self.iWP = ip
        self.gWP = gp
        self.eWP = ep
    def claim(self):
        # place mark on board
        global MAP
        # Figure Out BEST location to go to
        # can only claim Up Down Left Right
        # GET NEIGHBOORS
        neighs = findClaims(self.symbol,self.claims)
        topChoice = []
        top = -111111 
        trueCost = 0
        trueAble= False
        # CHOOSE CHOICE
        for x in neighs:
            target = MAP[x[0]][x[1]]
            # VALUE CLAIM (NEG claims if unaffordable?)
            value,cost,able = valueClaim(target,self.money,self.workers,self.forest,self.landInt,\
                    self.xW,self.fW,self.iW,self.gW,self.eW) 
            # potential
            dictNeigh = {}
            dictNeigh[0] =[x[0],x[1]] 
            potential = findClaims(self.symbol,dictNeigh)
            for y in potential:
                potTarget = MAP[y[0]][y[1]]
                value += valueClaim(potTarget,self.money,self.workers,self.forest,self.landInt,\
                        self.xW,self.fW,self.gW,self.eW,\
                        self.xWP,self.fWP,self.iWP,self.gWP,self.eWP,True)
            print self.name + "'s Potential Claim " + str(x) + " value: " + str(value) + ' cost: ' + str(cost)+' able: ' + str(able)
            if value > top:
                # store best choice
                top = value
                topChoice = [x[0],x[1]]
                trueCost = cost
                trueAble = able

        # MARK OUR TERRITORY
        if top > -30 and trueAble:
            print self.name + " Claimed [" + str(topChoice[0]) + ',' + str(topChoice[1]) + ']!' +\
                    "\nFor " + str(trueCost) + " Price!"
            self.flag(markMap(topChoice[0],topChoice[1],self.symbol))
            workerP = 0
            # calculate forest use
            if self.forest - self.workers >= 0:
                workerP = self.workers
            else:
                workerP = self.forest
            if trueCost - workerP > 0:
                trueCost = trueCost -workerP
                self.forest = self.forest-workerP
                # left over costs, covered by gold
                self.money = (self.money) - (trueCost * 5)
            elif trueCost - workerP == 0:
                trueCost = 0
                self.forest = 0
            elif trueCost - workerP < 0:
                self.forest = self.forest - trueCost
            self.claims[self.landInt] = [topChoice[0],topChoice[1]]
            self.landInt += 1

    def flag (self,resource):
        global IRON
        global GOLD
        global FOREST
        global MAP
        # increase our stats! Claimed Land
        if resource == FOREST:
            self.cforest += 1
        elif resource == GOLD:
            self.cgold += 1
        elif resource == IRON:
            self.ciron += 1
        
        
    def build(self):
        # Increases resources 
        self.money += 5 + self.cgold
        if self.forest < self.cforest:
            self.forest += 1
        if self.iron < self.ciron:
            self.iron += 1
        # create units (if money)
        if self.workers < self.cforest and self.money >= 4:
            self.money -= 4
            self.workers += 1

    def botStats(self):
        print "Empire " + self.name + " (" + self.symbol + "), Land: " + str(self.landInt)
        print "Money: " + str(self.money)
        print "Workers: " + str(self.workers)
        print "Army: " + str(self.army)
        print "Forest: " + str(self.forest) + '/' + str(self.cforest)
        print "Iron: " + str(self.iron) + '/' + str(self.ciron)
        print "Gold: " + str(self.cgold)
        print ""
# Main
if __name__ == "__main__":
    # generate map
    generateMap()

    # Generate Bot starting Locations
    # generate bots
    # weights are: x,forest,iron,gold,enemy,
    #... then the potentials
    usa = bot('USA','U',2,random.randrange(0,5),random.randrange(0,5))
    usa.setWeights(3,1,1,3,-10,4,1,1,3,-10)
    rus = bot('RUS','R',2,random.randrange(5,10),random.randrange(5,10))
    rus.setWeights(1,2,1,1,-1,1,2,1,1,0)
    # Start Simulation
    printMap()
    for turn in range(0,30):
        print "TURN " + str(turn+1)
        # CLAIM
        usa.claim()
        rus.claim()
        #BUILD
        usa.build()
        rus.build()
        # Show Map
        printMap()
        # Show Stats
        usa.botStats()
        rus.botStats()
        #sleep 1s
        time.sleep(.5)
