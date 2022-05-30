from gettext import find
import random, copy

class Card:
  def __init__(self, rank, suit):
    self.rank = rank
    self.suit = suit

  def __repr__(self):
      return "%s of %s" % (self.rank, self.suit)

class Player:
    def __init__(self, name, card1, card2):
      self.name = name
      self.card1 = card1
      self.card2 = card2

    def __repr__(self): 
        return "%s: \ncard 1: %s \ncard 2: %s" % (self.name, self.card1, self.card2)

ranks = {
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    '10': 10,
    'J': 11,
    'Q': 12,
    'K': 13,
    'A': 14
}

suits = [
    "spades",
    "clubs",
    "hearts",
    "diamonds"
]
# ALL cards already dealt this round
dealtCards = []

# deal a card
def dealCard ():
    cardExistsAlready = True

    while (cardExistsAlready):
        cardRank = random.choice(list(ranks))
        cardSuit = random.choice(suits)
        dealtCard = Card(cardRank, cardSuit)

        # list of every used card's rank
        dealtCardRanks = [card.rank for card in dealtCards]

        if(dealtCard.rank not in dealtCardRanks):
            cardExistsAlready = False
        else :
            cardExistsAlready = False
            for card in dealtCards:
                if (card.rank == cardRank and card.suit == cardSuit):
                    cardExistsAlready = True


    dealtCards.append(dealtCard)
    return dealtCard



# cards face up that all players can see
faceUpCards = []

# burn one card, then deal three cards face up
def dealFlop ():
    dealCard() # burn a card
    for x in range(3):
        flopCard = dealCard()
        faceUpCards.append(flopCard)

# burn one card, then deal one card face up
def dealTurn ():
    dealCard() # burn a card
    turnCard = dealCard()
    faceUpCards.append(turnCard)

# burn one card, then deal one card face up
def dealRiver ():
    dealCard() # burn a card
    riverCard = dealCard()
    faceUpCards.append(riverCard)

# determines how many hands to deal
numPlayers = 3

# list representing players in poker game
players = []

# deal a pair of cards to each of the numPlayers Players
def dealHands ():
    for x in range(numPlayers):
        card1 = dealCard()
        card2 = dealCard()
        playerName = "Player " + str(x + 1)
        players.append(Player(playerName, card1, card2))

# score the end of the round to find out which player has the best hand
def checkHands ():
    for player in players:
        # cardsToCheck = []
        # cardsToCheck = cardsToCheck + faceUpCards

        cardsToCheck = copy.copy(faceUpCards)
        
        cardsToCheck.append(player.card1)
        cardsToCheck.append(player.card2)

        highCard = findHighCard(cardsToCheck)
        print(player.name, "High Card: ", highCard)

# return the card within "cards" that has the highest rank
def findHighCard (cards):
    highCard = cards[0]
    highCardValue = ranks[cards[0].rank]

    for card in cards:
        cardValue = ranks[card.rank]
        if(cardValue > highCardValue):
            highCardValue = cardValue
            highCard = card
    return highCard

# deal hands to all players
dealHands()

# print all player hands
for player in players:
    print(player)

# deal a flop
dealFlop()

# deal a turn
dealTurn()

# deal a river
dealRiver()

print("\nFace Up Cards:")
for card in faceUpCards:
    print(card)



# print("\nDealt Cards:")
# for card in dealtCards:
#     print(card)

checkHands()