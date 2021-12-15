import random
import sys
import copy

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
        while True:
            name = str(input('Name of player ' + str(id+1) + ': '))
            if name != '':
                players.append(name)
                print("Nice to meet you ", name,"!", sep="")
                break
            else:
                print('Please, tell me your name.')
    print("We are ready. Let's start!\n")
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
        print("For", players[h], "we have:")
        for repeat in range(2):
            card = drawCard(deck, 1)
            identifiers = cardVisualization(card)
            print('┌───────┐')
            print(f'| {identifiers[0]}     |')
            print('|       |')
            print(f'|   {identifiers[1]}   |')
            print('|       |')
            print(f'|    {identifiers[0]}  |')
            print('└───────┘') 
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

#This determines who is the winner based on every game round
def winner(scores):
    score = list(scores.values())
    people = list(scores.keys())
    max_score = 0
    dictionary = {}
    for i in range(len(score)):
        if score[i] <= 21 and score[i]>max_score:
            max_score = score[i]
            id = i
    max_people = people[id]
    for i in range(len(people)):
        d1 = {str(people[i]):0}
        dictionary.update(d1)
    return max_people, dictionary

def continues(): #It is like withdraw
    default = True
    print("Do you want to continue the game ?")
    choice = str(input("yes/no : "))
    while default == True:
        if choice == "no":
            default = False
            return False
        elif choice == "yes":
            default = False
            return True
        else:
            print("I dont understand your input. Please type if you wamnt to continue teh game")
            choice = str(input("yes/no : "))


def playerTurn(j, players):
    data = firstTurn(players) #data in position 0 is the dictionary with the scores. In position 1 we have the modified deck
    points = data[0][j]
    if points<21:
        print("It's", j, "turn. You have", points, "points.")
        choice = str(input("hit/stand?"))
        while True:
            if choice == "stand":
                return data[0], data[1]
                break
            elif choice == "hit": #Player continues
                print("OK, let's continue.")
                card = drawCard(data[1], 1)
                data[1].remove(card)
                print("Here is your next card:")
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
                    break
                else:
                    data[0][j] = res
                    return data[0], data[1]
                    break
            else:
                print("I don't understand.")
                choice = str(input("hit/stand? "))
    else:
        print("Unfortunately,", j,"lost since his/her points were", points)
        data[0].pop(j)
        return data[0], data[1] #1 is deck, 0 is players dictionary with scores.

def turn(j, players, deck):
    if players[j]<21:
        print("It's", j, "turn. You have", players[j], "points.")
        choice = str(input("hit/stand? "))
        while True:
            if choice == "stand":
                return players, deck
                break
            elif choice == "hit": #Player continues
                print("OK!")
                card = drawCard(deck, 1)
                deck.remove(card)
                print("Here is your next card:")
                value = valueCard(card[0])
                identifiers = cardVisualization(card)
                print('┌───────┐')
                print(f'| {identifiers[0]}     |')
                print('|       |')
                print(f'|   {identifiers[1]}   |')
                print('|       |')
                print(f'|    {identifiers[0]}  |')
                print('└───────┘') 
                res = players[j] + value
                if res > 21:
                    print("Unfortunately,", j,"lost since his/her points were", res)
                    players.pop(j)
                    return players, deck
                    break
                else:
                    players[j] = res 
                    return players, deck
                    break
            else:
                print("I don't understand.")
                choice = str(input("hit/stand? "))
    else:
        print("Unfortunately,", j,"lost since his/her points were", players[j])
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
    number = len(list(data.keys())) #SOS - There is a problem here
    if number >= 1: #One single player on the dictionary remains
        return True
    else:
        return False

def completeGame(data, players): #Receives the dictionary of players every time
        max = 0
        id = 2
        ids = 1
        print("Round no 1")
        play = gameTurn(data, players)
        over = gameOver(play[0])
        if over == False:
            print("Game over")
            print("No remaining players on the game.")
        elif over == True:
            continueing = continues()
            if continueing == True:
                win = winner(play[0])
                win[1][win[0]]= win[1][win[0]]+1
                updatedDeck = play[1]
                players = play[0]
                if len(list(players.keys())) > 1:
                    while id > 0:
                        print("Round no", ids + 1)
                        playing = copy.deepcopy(players)
                        for j, value in players.items():
                            newRound = turn(j, playing, updatedDeck)
                        over = gameOver(newRound[0])
                        if over == False:
                            print("Game over")
                            print("No remaining players on the game.")
                            sys.exit()
                        elif over == True:
                            win = winner(newRound[0])
                            win[1][win[0]]= win[1][win[0]]+1
                            updatedDeck = newRound[1]
                            players = newRound[0]
                            playing = players
                            id = id -1
                        continueing = continues()
                        if continueing == False:
                            print("We have played", ids,"rounds in total")
                            for g in range(len(list(win[1].keys()))):
                                if max < list(win[1].values())[g]:
                                    max = list(win[1].values())[g] 
                                    person = list(win[1].keys())[g]
                            print("From the remaining", len(list(newRound[0].keys())), "players, the winner is",person, "with", max, "total victories.")
                            print("\nThanks for playing our BlackJack game. See yoou soon, bye bye!")
                            break
                    print("We have played three rounds in total")
                    for g in range(len(list(win[1].keys()))):
                        if max < list(win[1].values())[g]:
                            max = list(win[1].values())[g] 
                            person = list(win[1].keys())[g]
                    print("From the remaining", len(list(newRound[0].keys())), "players, the winner is",person, "with", max, "total victories.")
                else:
                    print("We have a winner!")
                    if max < list(win[1].values())[0]:
                        max = list(win[1].values())[0]
                    print("The winner is", list(win[1].keys())[0], "with total victories", max)
            else:
                print("Alright. Bye bye!")
        



#Main Program
n = int(input("How many players ? "))
print("Let's personalize your game a little bit.") #Via object programming techniques, all the inializations are done automaticly
players = initPlayers(n)
newPlayers = copy.deepcopy(players)
data = initScores(players,v=0)
id = 1
while id > 0:
    completeGame(data, players)
    print("==========")
    choice = str(input("Do you want to play again ? yes/no: "))
    if choice == "no":
        id = -1
    elif choice == "yes":
        players = copy.deepcopy(newPlayers)
        data = initScores(players,v=0)
        id = id + 1
    else:
        print("I do not understand. Please type yes or no.")
        choice = str(input("yes/no:")) 
print("Game is terminated")