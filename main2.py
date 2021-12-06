import random
import sys

Deck = {'Ace': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10,
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
        pause()
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
    print('\nBetting round')
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
    # round_number = 1 draw 2 cards and check for Blackjack, doubles, deck value
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
        if Croupier['c_values1'][0] == 'Ace':  # Croupier might have Blackjack
            insurance()
    else:
        print("The croupier, {}, has two hidden cards.".format(Croupier['Name']))
    pause()
    for x in Players:
        if Players[x]['Active'] and Players[x]['Play']:  # Check for Blackjack first on both sides
            player = Players[x]
            cards = player['c_values1']
            if (cards[0] == 'Ace' and Deck.get(cards[1]) == 10) or (Deck.get(cards[0]) == 10 and cards[1] == 'Ace'):
                player['BJ'] = True
                print("Congratulations {}! You have Blackjack!".format(player['Name']))
                player['Play'] = False
                pause()
            cards = Croupier['c_values1']
            if (cards[0] == 'Ace' and Deck.get(cards[1]) == 10) or (Deck.get(cards[0]) == 10 and cards[1] == 'Ace'):
                Croupier['BJ'] = True
                print('I have Blackjack!')
                print_deck(Croupier, 'Deck1')
                pause()
                winner()  # if Croupier has blackjack, no need to look more
    for x in Players:
        if Players[x]['Active'] and Players[x]['Play']:
            player = Players[x]
            if player['c_values1'][0] == player['c_values1'][1] and valueCardSum(player['c_values1']) in [9, 10, 11]:
                print(
                    '\n{}. It seems you can double your bet and split your hand. Be wary, you can only do one!'.format(
                        player['Name']))
            if valueCardSum(player['c_values1']) in [9, 10, 11]:
                double_bet(Players[x])
    for n in Players:
        player = Players[n]
        if player['c_values1'][0] == player['c_values1'][1] and player['Play']:  # and len(player['c_values1']) == 2
            split_deck(player)
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
        pause()
    winner()


def winner():
    # Check if there is any blackjack, if not check for player closer to 21
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
    pause()
    goodbye()


def goodbye():  # Check funds available to players, ask if anyone would like to leave and reset the game
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
                pause()
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

#=====================



def valueCardSum(card_values):
    # Total value of player's deck
    sum_card = 0
    for y in card_values:
        sum_card += Deck.get(y)
    return sum_card


def drawCard(quantity, player, deck, deck_value):
    # draw x cards and add to a dict so can keep track of each card == no repeated card
    if Config['deck_size'] > (40 * Config['max_deck']):
        left = (12 * Config['max_deck'])
        print('\nOnly {} cards left in the deck!'.format(left))
        print('Time for reshuffling!')
        used_cards.clear()
        Config['deck_size'] = 0
        pause()
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














def insurance():
    print('\n{} has an Ace as first card.'.format(Croupier['Name']))
    for x in Players:
        while True:
            bet_half = Players[x]['Bet'] // 2
            if Players[x]['Money'] >= (Players[x]['Bet'] + bet_half):
                print("{} would you like adding insurance?".format(Players[x]['Name']))
                print("It can go from 0, up to {}¢.".format(bet_half))
                answer = input('#: ')
                if answer.isdigit() and 0 <= int(answer) <= bet_half:
                    Players[x]['half_bet'] = int(answer)
                    print('Bet updated')
                    Players[x]['insurance'] = True
                    break
                else:
                    print('Enter a valid input, between 0 and {}.'.format(bet_half))
            elif Players[x]['Money'] > Players[x]['Bet']:  # Player's bet + half will be over player's money
                print("{} would you like adding insurance?".format(Players[x]['Name']))
                rest = Players[x]['Money'] - Players[x]['Bet']
                print("It can go from 0, up to {}¢.".format(rest))
                answer = input('#: ')
                if answer.isdigit() and 0 <= int(answer) <= rest:
                    Players[x]['half_bet'] = int(answer)
                    print('Bet updated')
                    Players[x]['insurance'] = True
                    break
                else:
                    print('Enter a valid input, between 0 and {}.'.format(rest))
            else:
                print("{}. You don't have enough money for insurance.".format(Players[x]['Name']))
                pause()
                break


def pause():
    input('Press Enter when you are ready\n')


def double_bet(player):
    if player['Money'] >= (player['Bet'] * 2):
        val = valueCardSum(player['c_values1'])
        print('\n{}. Your hand is worth {}.'.format(player['Name'], val))
        print_deck(player, 'Deck1')
        print('You can double down your bet if you want. You will draw just one additional card if you agree.')
        while True:
            print('Do you want your bet to be {}?'.format((player['Bet'] * 2)))
            yes_no = input("y/n: ")
            if yes_no not in ['y', 'n']:
                print('Please, enter a valid input.')
            if yes_no == 'y':
                player['Bet'] = player['Bet'] * 2
                drawCard(1, player, 'Deck1', 'c_values1')
                print('Your cards are:')
                print_deck(player, 'Deck1')
                for card_v in player['c_values1']:
                    if card_v == 'Ace':
                        player['Ace'] = True
                player['Play'] = False
                val = valueCardSum(player['c_values1'])
                if player['Ace'] and (val + 10) <= 21:
                    player['Score1'] = val + 10
                    print('Its value is: {}'.format(val + 10))
                elif player['Ace'] and (val + 10) > 21:
                    player['Score1'] = val
                    print('Its value is: {}'.format(val))
                else:
                    player['Score1'] = val
                    print('Its value is: {}'.format(val))
                pause()
                break
            elif yes_no == 'n':
                break
    else:
        print("{}. You don't have enough funds for doubling down your bet.".format(player['Name']))
        pause()


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


def print_deck(player, deck):
    for card in player[deck]:
        print("- " + card)


def hit_stand(player, deck, deck_value, score, state):
    while player['Active'] and player[state]:
        val = valueCardSum(player[deck_value])
        print('\n{}, it is your turn.'.format(player['Name']))
        show_card_value(player, deck, deck_value)
        if val > 21:
            print("Bust! Your hand is over 21.")
            player[score] = val
            player[state] = False
            pause()
        elif val <= 21:
            while True:
                print("What do you want to do, hit or stand?")
                choice = input("h/s: ")
                if choice not in ['h', 's']:
                    print('Enter a valid input.')
                if choice == 's':
                    player[state] = False
                    if player['Ace'] and (val + 10) <= 21:
                        player[score] = val + 10
                    elif player['Ace'] and (val + 10) > 21:
                        player[score] = val
                    else:
                        player[score] = val
                    break
                elif choice == 'h':
                    drawCard(1, player, deck, deck_value)
                    break


def split_deck(player):
    if player['Money'] >= (player['Bet'] * 2):
        print('\n{}, you can split your pair in two different hands.'.format(player['Name']))
        show_card_value(player, 'Deck1', 'c_values1')
        while True:
            print('Do you want two hands to play with?')
            answer_double = input("y/n: ").lower()
            if answer_double not in ['y', 'n']:
                print('Enter a valid input')
            elif answer_double == 'y':
                player['Double'] = True
                player.setdefault('Deck2', [])
                player.setdefault('c_values2', [])
                player.setdefault('Score2', 0)
                player['c_values2'].append(player['c_values1'][1])
                player['c_values1'].pop()
                player['Deck2'].append(player['Deck1'][1])
                player['Deck1'].pop()
                if player['c_values1'][0] == 'Ace':
                    print('Since your hand contains an Ace, you can only draw one additional card.')
                    print('{}. This is hand #1:'.format(player['Name']))
                    double_ace(player, 'Deck1', 'c_values1', 'Score1')
                    print('{}. This is hand #2:'.format(player['Name']))
                    double_ace(player, 'Deck2', 'c_values2', 'Score2')
                    player['Play'] = False
                    player['Double'] = False
                    pause()
                break
            elif answer_double == 'n':
                break
    else:
        print("{}. You don't have enough funds for playing two hands.".format(player['Name']))
        pause()


def double_ace(player, deck, value, score):
    drawCard(1, player, deck, value)
    print_deck(player, deck)
    val = valueCardSum(player[deck])
    player[score] = val + 10





if __name__ == "__main__":
    startGame()