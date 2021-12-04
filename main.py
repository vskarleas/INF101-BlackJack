import random

#This creates the deck
def deck():
    values = ['2','3','4','5','6','7','8','9','10','Jack','Queen','King','Ace']
    suites = ['Hearts', 'Clubs', 'Diamonds', 'Spades']
    deck = [[v + ' of ' + s] for s in suites for v in values] 
    return deck

#This give value to the cards
def valueCard(card):
    if "2" in card:
        return 2
    elif "3" in card:
        return 3
    elif "4" in card:
        return 4
    elif "5" in card:
        return 5
    elif "10" in card:
        return 10
    elif "6" in card:
        return 6
    elif "7" in card:
        return 7
    elif "8" in card:
        return 8
    elif "9" in card:
        return 9
    elif "Q" in card or "K" in card or "J" in card:
        return 10
    elif "A" in card: #User is asked in the UI to select the final value for Ace
        return 11

#This creates the overal final deck that will be used to the whole game
def initStack(n):
    finalDeck = []
    value = deck()
    for i in range(n):
        for k in range(len(value)):
            finalDeck.append(value[k])
    random.shuffle(finalDeck)
    return finalDeck

#This takes the coresponding number of cards from the predefined final deck (p here) and return this list of card/s
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

#This is used to initilize the players names and personalize the game
def initPlayers(n):
    players = []
    id = 1
    for id in range(n):
        name = str(input('Name of player ' + str(id+1) + ': '))
        players.append(name)
    return players

#This creates the dictionary that we are using in all the functions below
def initScores(players,v=0):
    if v != 0:
        dictionary = dict.fromkeys(players, v)
    else:
        dictionary = dict.fromkeys(players, 0)
    return dictionary #usually mentioned scores on the other functions below

def cardVisualization(card):
    cardOutput = card[0]
    elem = []
    if "Hearts" in card:
        elem.append("♥")
    elif "Diamonds" in card:
        elem.append("♦")
    elif "Spades" in card:
        elem.append("♠")
    else:
        elem.append("♣")
    if "2" in cardOutput:
        elem.append("2")
    elif "3" in cardOutput:
        elem.append("3")
    elif "4" in cardOutput:
        elem.append("4")
    elif "5" in cardOutput:
        elem.append("5")
    elif "6" in cardOutput:
        elem.append("6")
    elif "7" in cardOutput:
        elem.append("7")
    elif "8" in cardOutput:
        elem.append("8")
    elif "9" in cardOutput:
        elem.append("9")
    elif "10" in cardOutput:
        elem.append("10")
    elif "Jack" in cardOutput:
        elem.append("J")
    elif "Queen" in cardOutput:
        elem.append("Q")
    elif "Ace" in cardOutput:
        elem.append("A")
    elif "King" in cardOutput:
        elem.append("K")
    return elem

#This creates the first view of players points
def firstTurn(players):
    scores = initScores(players, v=0)
    n = len(players)
    deck = initStack(n)
    for h in range(len(players)):
        res = 0
        #print("For", players[h], "we have:")
        for repeat in range(2):
            card = drawCard(deck, 1)
            #identifiers = cardVisualization(card)
            #print('┌───────┐')
            #print(f'| {identifiers[0]}     |')
            #print('|       |')
            #print(f'|   {identifiers[1]}   |')
            #print('|       |')
            #print(f'|    {identifiers[0]}  |')
            #print('└───────┘') 
            deck.remove(card)
            if valueCard(card[0]) == 1:
                print("Your card is ",card[0], "and you need to select its value")
                choice = int(input("11 or 1 ? "))
                if choice == 1:
                    res = res + 1
                else:
                    res = res + 11
            else:
                res = res + valueCard(card[0])
        scores[players[h]] = res
    return scores, deck

#This determines who is the winner based on the plays
def winner(scores): #The argumnet needs to be modified once I have finished the completeGame function
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


def playerTurn(j, players):
    data = firstTurn(players) #data in position 0 is the dictionary with the scores. In position 1 we have the modified deck
    points = data[0][j]
    if points<21:
        print("It's", j, "turn. You have", points, "points.")
        save = continues()
        if save == False:
            data[0].pop(j)
            return data[0], data[1]
        else: #Player continues
            print("OK, let's continue.")
            card = drawCard(data[1], 1)
            data[1].remove(card)
            print("Here is the next card:")
            value = valueCard(card[0])
            identifiers = cardVisualization(card)
            print('┌───────┐')
            print(f'| {identifiers[0]}     |')
            print('|       |')
            print(f'|   {identifiers[1]}   |')
            print('|       |')
            print(f'|    {identifiers[0]}  |')
            print('└───────┘') 
            res = points + value
            if res > 21:
                print("Unfortunately,", j,"lost since his/her points were", res)
                data[0].pop(j)
                return data[0], data[1]
            else:
                data[0][j] = res
                return data[0], data[1]
    else:
        print("Unfortunately,", j,"lost since his/her points were", points)
        data[0].pop(j)
        return data[0], data[1]

def gameTurn(data, players): #Receives the dictionary of players every time
    for i in range(len(list(data.keys()))):
        lamda = list(data.keys())
        j = lamda[i]
        save = playerTurn(j, players)
        players = list(save[0].keys())
    return save


def gameOver(data): #Receives the dictionary of players every time
    number = list(data.keys()) #SOS - There is a problem here
    if number == 1: #One single player on the dictionary remains
        return True
    else:
        return False

def completeGame(data, players): #Receives the dictionary of players every time
    default = False
    while default == False:
        klm = gameTurn(data, players)
        over = gameOver(klm)
        if over == True:
            default = True
        else:
            default = False
    print("The game is completed, we have a winner")
    print("The winner is", klm[0].keys())

#Main Program
n = int(input("How many players ? "))
print("Let's personalize your game a little bit.") #Via object programming techniques, all the inializations are done automaticly
players = initPlayers(n)
data = initScores(players,v=0)
gameTurn(data, players)