#!/usr/bin/python2.7
import random

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
    for x in range (0,5):
        MAP.append([])
        for y in range (0,5):
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
            if y[0] +a[0] >= 0 and y[1] + a[1] >=0 and y[0] + a[0] < 5 and y[1] + a[1] < 5:
                if s not in MAP[y[0]+a[0]][y[1]+a[1]]:
                    potClaims.append([y[0]+a[0],y[1]+a[1]])
    return potClaims

def valueClaim(claim, x=1,i=2,f=2,g=3,e=-5):
    # returns a value of how useful a piece of land is
    # changable for different bots
    global FOREST
    global GOLD
    global IRON
    value = 0
    if claim[0] != ' ':
        # enemy!
        return e
    elif FOREST in claim:
        return f
    elif GOLD in claim:
        return g
    elif IRON in claim:
        return i
    elif 'X' in claim:
        return x

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
    # LAND CLAIMED
    cgold = 0
    cforest = 0
    ciron = 0
    # Supplies
    forest = 0
    iron = 0
    # set init variables
    def __init__(self,name, symbol, money,x,y):
        global MAP
        self.name = name
        self.symbol = symbol
        self.money = money
        self.claims[0] = [x,y] 
        self.flag(markMap(x,y,symbol))
    def claim(self):
        # place mark on board
        global MAP
        # Figure Out BEST location to go to
        # can only claim Up Down Left Right
        # GET NEIGHBOORS
        neighs = findClaims(self.symbol,self.claims)
        topChoice = []
        top = 0 
        # CHOOSE CHOICE
        for x in neighs:
            target = MAP[x[0]][x[1]]
            value = valueClaim(target) 
            # potential
            dictNeigh = {}
            dictNeigh[0] =[x[0],x[1]] 
            potential = findClaims(self.symbol,dictNeigh)
            for y in potential:
                potTarget = MAP[y[0]][y[1]]
                value += valueClaim(potTarget,0,1,1,2,-10)
            print "Potential Claim " + str(x) + " value: " + str(value)
            if value > top:
                # store best choice
                top = value
                topChoice = [x[0],x[1]]

        # MARK OUR TERRITORY
        self.flag(markMap(topChoice[0],topChoice[1],self.symbol))
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
        self.money += 1 + self.cgold
        if self.forest < self.cforest:
            self.forest += 1
        if self.iron < self.ciron:
            self.iron += 1
        # create units (if money)

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
    usa = bot('usa','U',2,random.randrange(0,5),random.randrange(0,5))

    # Start Simulation
    printMap()
    for turn in range(0,10):
        print "TURN " + str(turn+1)
        # CLAIM
        usa.claim()
        #BUILD
        usa.build()
        # Show Map
        printMap()
        # Show Stats
        usa.botStats()
        #sleep 1s
