import math
import random

def deck():
    values = ['2','3','4','5','6','7','8','9','10','Jack','Queen','King','Ace']
    suites = ['Hearts', 'Clubs', 'Diamonds', 'Spades']
    deck = [[v + ' of ' + s] for s in suites for v in values] 
    return deck

def valueCard(card):
    value = list(card[0])
    if "2" in value:
        return 2
    elif "3" in value:
        return 3
    elif "4" in value:
        return 4
    elif "5" in value:
        return 5
    elif "10" in value:
        return 10
    elif "6" in value:
        return 6
    elif "7" in value:
        return 7
    elif "8" in value:
        return 8
    elif "9" in value:
        return 9
    elif "Q" in value or "K" in value or "J" in value:
        return 10
    elif "A" in value:
        return 1, 11
        choice = int(input('How do you want to value the ' + str(card[0]) + ' (1/11) :')) # Maybe do not decide here but in the beginning of the game
        if choice == 1:
            return 1
        if choice == 11:
            return 11

def initStack(n):
    finalDeck = []
    value = deck()
    for i in range(n):
        for k in range(len(value)):
            finalDeck.append(value[k])
    random.shuffle(finalDeck)
    return finalDeck

def drawCard(p,x):
    if len(p) == 1 or x=='':
        return p
    elif len(p) < x:
        return p
    elif x == 1:
        var =  p[0]
        p = list(var)
        return p
    else: 
        for i in range((len(p)-(x-1))-1):
            p.pop(x)
        return p

def initPlayers(n):
    players = []
    id = 1
    for id in range(n):
        name = str(input('Name of player ' + str(id+1) + ': '))
        players.append(name)
    return players

def initScores(players,v=0):
    if v != 0:
        dictionary = dict.fromkeys(players, v)
    else:
        dictionary = dict.fromkeys(players, 0)
    return dictionary

def firstTurn(players):
    v = 0
    scores = initScores(players,v)
    x = 2
    n = len(players)
    p = initStack(n)
    for i in range(n):
        res = 0
        xar = drawCard(p, x)
        for k in range(len(xar)):
            card = xar[k]
            res = res + valueCard(card)
        scores[players[i]] = res
    return scores #Var is the dictionary as we can see

def winner(scores):
    score = list(scores.values())
    people = list(scores.keys())
    max_score = 0
    for i in range(len(score)):
        if score[i] <= 21 and score[i]>max_score:
            max_score = score[i]
            id = i
    max_people = people[id]
    return max_people, max_score

def continues():
    default = True
    print("Do you want to continue the game or to stop ?")
    choice = str(input("go/stop ? "))
    while default == True:
        if choice == "stop":
            default = False
            return False
        elif choice == "go":
            default = False
            return True
        else:
            print("I dont understand your input. Please type go or stop")
            choice = str(input("go/stop ? "))
    return default

def playerTurn(j): #Needs to be continued
    play = 1
    while play > 0:
        #points and ids variables are not defined
        print("j, this is your", ids, "game. You have ", points, "total points.")
    return



def gameTurn():
    #I haven't written this function. After this function
    #do everything that the exercise expects, I want to return a
    #True or False depending on the active users' list
    #retruns False for empty list of players
    #and returns true for not empty as well as the list of current playing players
    return

def gameOver():
    var = gameTurn()
    if var == False:
        return True #Game is finished (no more players left)
    else:
        return False #Game hasn't finished yet

def completeGame():
    xar = gameOver()
    if xar == False:
        print("To be continued")
    #This function hasn't been completed yet.
    #I need gameTurn function complted in order to
    #know if the logique is correct and at gameOver
    #as well. In general, it requires the combination
    #of different functions.
    #
    #Make sure that somehow we are receivign a scores dictionary
    #or something that we can parse the data to the scores
    #dictionary like mentioned on the file:
    #This function must then update the players’ numbers of 
    #victories (in the corresponding dictionary). For the moment, 
    #the winner gets 1 point for the victory, and the other 
    #players get 0.


#B3 Main Program
n = int(input("Number of players ? "))
replay = True
id = 1
print("Let's personalize the game a little bit.")
players = initPlayers(n)
while replay == True:
    cardsDeck = initStack(n)
    print("Cards deck is generated. Here is your initial score")
    scores = (firstTurn(players))
    print(scores) #We will remove it once we finish with the set up. I just added as a verification that things work
    #The rest of the program to play a game one time goes here
    choice = str(input("Do you want to play again ? (yes/no) "))
    if choice == "no":
        replay = False
        id = id +1
    else:
        replay == True
print("==========")
print("You played in total ", id, "games")
print("The winner in all the games is the one with the biggest score (money gained).")
print("Winner: ", winner(scores)) #The scores dictionary is changing during the game though the functions. This section in the main program isn't created yet.