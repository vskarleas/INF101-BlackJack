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
        choice = int(input('How do you want to value the ' + str(card[0]) + ' (1/11) :'))
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
    #I need some clarification
    return
    

def initPlayers(n):
    players = []
    id = 1
    for id in range(n):
        name = str(input('Name of player ' + str(id+1) + ': '))
        players.append(name)
    return players

def initScores(players,v):
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