# import libary required to create simulation
import random

class Deck():
    def __init__(self):
        self.cards = []
        self.generate()
        random.shuffle(self.cards)
    
    # Generating the cards in the deck
    def generate(self):
        # ['spade','diamonds','hearts', 'clubs']
        for suit in range(4):
            for value in range(3,16):
                self.cards.append([value, suit])
                
    def show(self):
        print(self.cards)

class Player():
    def __init__(self, cards, advance):
        self.cards = cards
        self.advance = 0   

def play_lowest(player, prev_card):
    for card in player.cards:
        if card > prev_card:
            # remove card from player's hand
            player.cards.remove(card)
            return card
    return []

def play_highest(player, prev_card):
    card = player.cards[-1]
    if card > prev_card:
        # remove card from player's hand
        player.cards.remove(card)
        return card
    return []

def play_middle(player, prev_card):
    p_cards = player.cards
    card = p_cards[int(len(p_cards)/2)]
    if card > prev_card:
        # remove card from player's hand
        player.cards.remove(card)
        return card
    return []

def play_alternate(player, prev_card, alternate):
    if alternate == 1:
        for card in player.cards:
            if card > prev_card:
                # remove card from player's hand
                player.cards.remove(card)
                return card
        return []
    else:
        card = player.cards[-1]
        if card > prev_card:
            # remove card from player's hand
            player.cards.remove(card)
            return card
        return []

numberOfPlayers = 4 # Number of Players
numberOfGames = 10000 # Number of Games

# generating array to keep track of how many times each player wins
scores = []
for i in range(numberOfPlayers):
    scores.append(0)

for game in range(numberOfGames): ## Looping through the number of games
    
    # Generate deck
    deck = Deck()
    
    # Intialize players array
    players = []
    for i in range(numberOfPlayers):
        players.append(1)
        players[i] = Player([], 0)
    
    # initializing the cards within the players hand
    while len(deck.cards) > 0:
        for i in range(numberOfPlayers):
            card = deck.cards.pop()
            players[i].cards.append([card[0],card[1]])

    # sort each cards in the players hand
    for i in range(numberOfPlayers):
        players[i].cards = sorted(players[i].cards)
        
    # The player with the three of clubs always start
    for i in range(numberOfPlayers):
        if players[i].cards[0][0] == 3 and players[i].cards[0][1] == 0:
            currentPlayer = i
    
    # set the current card in play
    prevCard = [3, 0] 
    players[currentPlayer].cards.remove(prevCard) # remove that card from the player hand
    currentPlayer = (currentPlayer+1) % numberOfPlayers # move to the next player
    currCard = [] 
    passes = 0
    alternate = 1

    # while there is still card in the players hand
    while all(len(player.cards) > 0 for player in players):
        # Your strategy
        if (currentPlayer in [0]) and (players[currentPlayer].advance == 0):
            currCard = play_lowest(players[currentPlayer], prevCard)
            
        # Opponent strategy
        if (currentPlayer in [1,2,3]) and (players[currentPlayer].advance == 0):
            currCard = play_alternate(players[currentPlayer], prevCard, alternate)

        alternate *= -1
        
        if prevCard != currCard:
            prevCard = currCard
        else:
            # player passes
            if players[currentPlayer].advance != 1:
                passes +=1 
            players[currentPlayer].advance = 1

        if passes == 3:
            # reset round
            passes = 0
            prevCard = [-1, -1]
            currCard = []
            alternate = 1
            for i in range(numberOfPlayers):
                if players[i].advance == 0:
                    currentPlayer = i
                else:
                    players[i].advance = 0
        else: # continue round
            currentPlayer = (currentPlayer+1) % numberOfPlayers

        # show remaining hands
        for i in range(numberOfPlayers):
            if len(players[i].cards) == 0:
                scores[i] += 1
                break

print(scores[0]/numberOfGames)