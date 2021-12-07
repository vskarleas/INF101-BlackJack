import random
import sys

Deck = {'Ace': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
        'Jack': 10, 'Queen': 10, 'King': 10}
Suit = ['of Clubs', 'of Spades', 'of Hearts', 'of Diamonds']
Croupier = {'Name': 'MAX', 'Deck1': [], 'c_values1': [], 'Play': True, 'Ace': False, 'BJ': False, 'Score1': 0}
Template = {'Name': '', 'Money': 0, 'Bet': 0, 'Active': True, 'Play': True, 'BJ': False, 'Double': False, 'Ace': False,
            'Score1': 0, 'insurance': False, 'half_bet': 0}
Players = {}
Config = {'Number of players': 0, 'Money': 100, 'Minimum_bet': 5, 'show': True, 'game': 0, 'deck_size': 0,
          'max_deck': 0}
used_cards = {}
Croupier_names = ['Max', 'Ilias', 'Joey', 'Jenk', 'Asher', 'Sophie', 'Johnny', 'Iris', 'Kennedy', 'Nike']

def startGame():
    Croupier['Name'] = random.choice(Croupier_names)
    print("Hello, my name is {}. I'll be your Croupier for this session.".format(Croupier['Name']))
    print('The prizes are:')
    print('- Blackjack pays 3 to 2.')
    print('- Wins pays 1 to 1.')
    print('- Insurance pays 2 to 1.')
    configuration()

def configuration():
    print('\nLets personalize your game a little bit')
    print('Do you prefer default rules, or would you rather have a custom set of rules?')
    while True:
        print('The default rules are: Minimum bet = {}¢; Funds available to each player = {}¢; Croupier show one card.'.format(
            Config['Minimum_bet'], Config['Money']))
        configurationuration = input("default/custom: ").lower() #In order to prevent any error, the lower() predefines for what we need to filter bellow
        if configurationuration not in ['default', 'custom']:
            print('Please, enter a valid input.')
        elif configurationuration == 'default':
            numberPlayers()
        else:
            while True:
                min_bet = input("How much should minimum bet be? ")
                if min_bet.isdigit() and 0 < int(min_bet) < 100: #We are not forced to have the <100 option here
                    Config['Minimum_bet'] = int(min_bet)
                    break
            while True:
                funds = input("How much funds should each player have? ")
                if funds.isdigit() and Config['Minimum_bet'] * 2 < int(funds): #Minimu_bet just changed above
                    Config['Money'] = int(funds)
                    break
            while True:
                print('Croupier should show you one card?')
                show = input("yes/no: ").lower()
                if show == 'yes':
                    Config['show'] = True
                    break
                if show == 'no':
                    Config['show'] = False
                    break
            numberPlayers()

def numberPlayers():
    n = input("How many players ? ")
    if n.isdigit() and 1 <= int(n):
        Config['Number of players'] = int(n)
        Config['max_deck'] = Config['Number of players']
        
        for x in range(1, Config['Number of players'] + 1):
            new_player = 'Player ' + str(x) #This will get personalized via the initPlayers() function
            template_new = dict(Template)
            Players.setdefault(new_player, template_new) #FRom python docs: The setdefault() method returns the value of the item with the specified key. If the key does not exist, insert the key, with the specified value
            Players[new_player].setdefault('Deck1', [])
            Players[new_player].setdefault('c_values1', [])
        initPlayers()
    else:
        print('Enter a valid input.')
        numberPlayers()

def initPlayers():
    for x in Players: #The players dictionary includes a dictionary created from the template dectionary as initiliazed from the numberPlayers function
        if Players[x]['Active']: #Safety valve that verifies that the players dictionary has elements or where it has to stop asking since the dictionary elemnts do not have IDs like the lists  
            while True:
                Players[x]['Name'] = input("Name of player " + list(x)[7] + ": ") #I can explain why I have added this seven here in this corresponding list
                if Players[x]['Name'] != '':
                    print('Nice to meet you {}!'.format(Players[x]['Name']))
                    Players[x]['Money'] = Config['Money']
                    break
                else:
                    print('Please, tell me your name.')
    print("We are ready. Let's start!")
    betting()

def betting():
    Config['game'] = Config['game'] + 1 #The 
    print('\nGame number {}'.format(Config['game']))
    if Config['game'] % 10 == 0: #When the croupier has lost specific amount of times, we are channging croupier 
        while True:
            new_croupier = random.choice(Croupier_names)
            if new_croupier != Croupier['Name']:
                Croupier['Name'] = new_croupier
                print('My turn is over. I introduce you to your new croupier, {}'.format(Croupier['Name']))
                print('Have fun!\n')
                break
    print('\nTime to give your bets')
    for x in Players:
        if Players[x]['Active']:
            while True:
                print('\nPlease, {}. Place a bet! You can go up to {}'.format(Players[x]['Name'], Players[x]['Money']))
                bet = input("Your bet: ")
                if bet.isdigit() and Config['Minimum_bet'] <= int(bet) <= 500 and int(bet) <= Players[x]['Money']:
                    Players[x]['Bet'] = int(bet)
                    print("Your bet has been registered.")
                    break
    firstTurn()

def firstTurn():
    for x in Players:
        if Players[x]['Active']:
            drawCard(2, Players[x], 'Deck1', 'c_values1')
    drawCard(2, Croupier, 'Deck1', 'c_values1')
    for x in Players:
        if Players[x]['Active']:
            print(Players[x]['Name'] + ' these are your cards:')
            print_deck(Players[x], 'Deck1')
    if Config['show']:
        print("The croupier, {}, has {} and one hidden card.".format(Croupier['Name'], Croupier['Deck1'][0]))
    else:
        print("The croupier, {}, has two hidden cards.".format(Croupier['Name']))
    for x in Players:
        if Players[x]['Active'] and Players[x]['Play']:  # Check for Blackjack first on both sides
            player = Players[x]
            cards = player['c_values1']
            if (cards[0] == 'Ace' and Deck.get(cards[1]) == 10) or (Deck.get(cards[0]) == 10 and cards[1] == 'Ace'):
                player['BJ'] = True
                print("Congratulations {}! You have Blackjack!".format(player['Name']))
                player['Play'] = False
            cards = Croupier['c_values1']
            if (cards[0] == 'Ace' and Deck.get(cards[1]) == 10) or (Deck.get(cards[0]) == 10 and cards[1] == 'Ace'):
                Croupier['BJ'] = True
                print('I have Blackjack!')
                print_deck(Croupier, 'Deck1')
                winner()  # if Croupier has blackjack, no need to look more
    for n in Players:
        player = Players[n]
        hit_stand(Players[n], 'Deck1', 'c_values1', 'Score1', 'Play')
        if Players[n].get('Double'):
            hit_stand(Players[n], 'Deck2', 'c_values2', 'Score2', 'Double')
    croupier()

def croupier():
    print("\nIt's my turn.")
    while Croupier['Play']:
        val = valueCardSum(Croupier['c_values1'])
        for card_v in Croupier['c_values1']:
            if card_v == 'Ace':
                Croupier['Ace'] = True
        print('My cards are:')
        print_deck(Croupier, 'Deck1')
        if Croupier['Ace'] and (val + 10) <= 21:
            print('Hard value: {}'.format(val))
            print('Soft value: {}\n'.format((val + 10)))
        else:
            print("Its values is: {}\n".format(val))
        if val > 21:
            print('Bust! My hand is over 21.')
            Croupier['Play'] = False
            Croupier['Score1'] = val
        elif Croupier['Ace'] and 17 <= (val + 10) <= 21:
            print('I stand.')
            Croupier['Score1'] = val + 10
            Croupier['Play'] = False
        elif 17 <= val <= 21:
            Croupier['Score1'] = val
            print('I stand.')
            Croupier['Play'] = False
        elif Croupier['Ace'] and (val + 10) < 17:
            print('I hit for another card.')
            drawCard(1, Croupier, 'Deck1', 'c_values1')
        elif val < 17:
            print('I hit for another card.')
            drawCard(1, Croupier, 'Deck1', 'c_values1')
    winner()

def winner():
    for x in Players:
        if Players[x]['Active']:
            player = Players[x]
            if Croupier['BJ']:
                if player['BJ']:
                    print('{}. You recover your bet of {}¢.'.format(player['Name'], player['Bet']))
                if player['insurance'] and 0 < player.get('half_bet', 0):
                    print("{} your insurance covers your bet and you win {}¢".format(player['Name'],
                                                                                     player['half_bet'] * 2))
                    player['Money'] += player['half_bet'] * 2
                else:
                    player['Money'] -= player['Bet']
                    print("Sorry, {}. You lost {}¢.".format(player['Name'], player['Bet'], ))
            else:  # Croupier['BJ'] is False
                if player['BJ']:
                    player['Money'] += (player['Bet'] * 3) // 2
                    print(
                        "{}. You got Blackjack and receive {}¢!".format(player['Name'], ((player['Bet'] * 3) // 2) +
                                                                        player['Bet']))
                if player['insurance'] and 0 < player.get('half_bet', 0):
                    print("{} You lost your insurance bet".format(player['Name']))
                    player['Money'] -= player['half_bet']
                elif Croupier['Score1'] > 21 and player['BJ'] is False:
                    if player['Score1'] <= 21:
                        player['Money'] += player['Bet']
                        print('{}. You win! You get {}¢.'.format(player['Name'], player['Bet'] * 2))
                    if player.get('Score2', 22) <= 21:
                        player['Money'] += player['Bet']
                        print('{}. You win! You get {}¢ from hand #2.'.format(player['Name'], player['Bet'] * 2))
                    if player['Score1'] > 21:
                        player['Money'] -= player['Bet']
                        print("Sorry, {}. You lost {}¢.".format(player['Name'], player['Bet'], ))
                    if player.get('Score2', 0) > 21:
                        player['Money'] -= player['Bet']
                        print("Sorry, {}. You lost {}¢ from hand #2.".format(player['Name'], player['Bet'], ))
                elif Croupier['Score1'] <= 21 and player['BJ'] is False:
                    if Croupier['Score1'] < player['Score1'] <= 21:
                        player['Money'] += player['Bet']
                        print('{}. You win! You get {}¢.'.format(player['Name'], player['Bet'] * 2))
                    if Croupier['Score1'] < player.get('Score2', 0) <= 21:
                        player['Money'] += player['Bet']
                        print('{}. You win! You get {}¢.'.format(player['Name'], player['Bet'] * 2))
                    if Croupier['Score1'] == player['Score1']:
                        print("{}. It's a tie, you recover your bet.".format(player['Name']))
                    if Croupier['Score1'] == player.get('Score2', 0):
                        print("{}. It's a tie, you recover your bet from hand #2.".format(player['Name']))
                    if player['Score1'] < Croupier['Score1']:
                        player['Money'] -= player['Bet']
                        print("Sorry, {}. You lost {}¢.".format(player['Name'], player['Bet'], ))
                    if player.get('Score2', Croupier['Score1']) < Croupier['Score1']:
                        player['Money'] -= player['Bet']
                        print("Sorry, {}. You lost {}¢ from hand #2.".format(player['Name'], player['Bet'], ))
                    if player['Score1'] > 21:
                        player['Money'] -= player['Bet']
                        print("Sorry, {}. You lost {}¢.".format(player['Name'], player['Bet'], ))
                    if player.get('Score2', 0) > 21:
                        player['Money'] -= player['Bet']
                        print("Sorry, {}. You lost {}¢ from hand #2.".format(player['Name'], player['Bet'], ))
    goodbye()

def goodbye():
    for x in Players:
        if Players[x]['Money'] < Config['Minimum_bet'] and Players[x]['Active']:
            print("Sorry, {}. You don't have enough funds to cover minimum bet. You only have left {}¢.".format(
                Players[x]['Name'], Players[x]['Money']))
            Players[x]['Active'] = False
            print('Thanks for playing! Come back another day!')
    inactive = 0
    for n in Players:  # Reset all markers to default
        if Players[n]['Active'] is False:
            inactive += 1
            if inactive == Config['Number of players']:
                print('No active players left. Thanks for playing!')
                sys.exit()
    print('If any player would like to withdraw, please type your name. Leave it blank and we will continue with the '
          'next game.')
    out = input("Player: ")
    for x in range(1, Config['Number of players'] + 1):
        new_player = 'Player ' + str(x)
        if out == Players[new_player].get('Name') and Players[new_player]['Active']:
            print('Farewell {}.'.format(Players[new_player]['Name']))
            net = Players[new_player]['Money'] - Config['Money']
            print('Net worth: {}¢'.format(net))
            Players[new_player]['Active'] = False
            goodbye()
    if out == '':
        for n in Players:  # Reset all markers to default
            if Players[n]['Active']:  # If any player is Active, it will reset its markers
                Players[n]['Deck1'].clear()
                Players[n]['c_values1'].clear()
                Players[n]['Play'] = True
                Players[n]['Double'] = False
                Players[n]['Ace'] = False
                Players[n]['BJ'] = False
                Players[n]['insurance'] = False
                if Players[n].get('Deck2'):
                    Players[n].pop('Deck2')
                    Players[n].pop('c_values2')
                    Players[n].pop('Score2')
        Croupier['Deck1'].clear()
        Croupier['c_values1'].clear()
        Croupier['Play'] = True
        Croupier['BJ'] = False
        Croupier['Ace'] = False
        betting()
    else:
        print('No player found with the name {}.'.format(out))
        goodbye()


def drawCard(quantity, player, deck, deck_value):  # draw x cards and add to a dict so can keep track of each card in ordr no to have repeated card
    if Config['deck_size'] > (40 * Config['max_deck']):
        left = (12 * Config['max_deck'])
        print('\nOnly {} cards left in the deck!'.format(left))
        print('Time for reshuffling!')
        used_cards.clear()
        Config['deck_size'] = 0
    for x in range(quantity):
        while True:
            card_value = random.choice(list(Deck.keys()))
            card = card_value + ' ' + random.choice(Suit)
            if used_cards.get(card, 0) < Config['max_deck']:  # If card doesn't exit .get(card) = 0
                used_cards.setdefault(card, 0)  # Create card in dict used_cards with value = 0
                used_cards[card] += 1
                player[deck].append(card)
                player[deck_value].append(card_value)
                Config['deck_size'] += 1
                break

#=====================
#Graphical Design Interface UI

def cardVisualization(card):
    cardOutput = card[0]
    elem = []
    elem.clear()
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
    elif "Jack" in card:
        elem.append("J")
    elif "Queen" in card:
        elem.append("Q")
    elif "Ace" in card:
        elem.append("A")
    elif "King" in card:
        elem.append("K")
    else:
        elem.append("?")
    return elem

def print_deck(player, deck):
    for card in player[deck]:
        identifiers = cardVisualization(card)
        print('┌───────┐')
        print(f'| {identifiers[0]}     |')
        print('|       |')
        print(f'|   {identifiers[1]}   |')
        print('|       |')
        print(f'|    {identifiers[0]}  |')
        print('└───────┘') 

#===========
#Essential callable functions that determine the game

def valueCardSum(card_values): #Total value of player's deck
    sum_card = 0
    for y in card_values:
        sum_card += Deck.get(y)
    return sum_card

def show_card_value(player, deck, deck_value):
    print('Your cards are:')
    print_deck(player, deck)
    val = valueCardSum(player[deck_value])
    for card_v in player[deck_value]:
        if card_v == 'Ace':
            player['Ace'] = True
    if player['Ace'] and (val + 10) <= 21:
        print('There is an Ace. Possible values are:')
        print('Hard value: ' + str(val))
        print('Soft value: ' + str(val + 10))
    else:
        print('Its value is: {}'.format(val))


def hit_stand(player, deck, deck_value, score, state):
    while player['Active'] and player[state]:
        val = valueCardSum(player[deck_value])
        print('\n{}, it is your turn.'.format(player['Name']))
        show_card_value(player, deck, deck_value)
        if val > 21:
            print("Bust! Your hand is over 21.")
            player[score] = val
            player[state] = False
        elif val <= 21:
            while True:
                choice = input("What do you want to do, hit or stand? ")
                if choice not in ['hit', 'stand']:
                    print('Enter a valid input.')
                if choice == 'stand':
                    player[state] = False
                    if player['Ace'] and (val + 10) <= 21:
                        player[score] = val + 10
                    elif player['Ace'] and (val + 10) > 21:
                        player[score] = val
                    else:
                        player[score] = val
                    break
                elif choice == 'hit':
                    drawCard(1, player, deck, deck_value)
                    break

#Inspired by the program on Caseine and TP 5 that we show this
#It activates the object-ariented function that handles the flow of the game
if __name__ == "__main__":
    startGame() #Very important