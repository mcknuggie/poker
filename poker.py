from gettext import find
import random, copy
from re import L

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

reversed_ranks = {
    2: '2',
    3: '3',
    4: '4',
    5: '5',
    6: '6',
    7: '7',
    8: '8',
    9: '9',
    10: '10',
    11: 'J',
    12: 'Q',
    13: 'K',
    14: 'A'
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
        cardsToCheck = copy.deepcopy(faceUpCards)
        
        cardsToCheck.append(player.card1)
        cardsToCheck.append(player.card2)

        print(player.name, "Cards in play: ", cardsToCheck)

        highCard = findHighCard(cardsToCheck)

        print(player.name, "High Card: ", highCard)

        print(player.name, "Duplicate Ranks:")
        findDuplicateRanks(cardsToCheck)

        print(player.name, "Straight Cards: ", findStraights(cardsToCheck))

        print(player.name, "Flush Cards: ", findFlushes(cardsToCheck))

        print("\n")

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

# finds pairs, 3 of a kind, and 4 of a kind
def findDuplicateRanks (cards):
    uniqueRanks = {}
    for card in cards:       
        if card.rank in list(uniqueRanks):
            uniqueRanks[card.rank] = uniqueRanks[card.rank] + 1
        else:
            uniqueRanks[card.rank] = 1
    print(uniqueRanks)

# returns the array of cards that make up the straight, returns empty array "[]" if no straight is found
def findStraights (cards):

    straightCards = []

    for card in cards:
        startOfStraight = True
        if ranks[card.rank] > 10 and ranks[card.rank] != 14: # J, Q, K can't start straight
            startOfStraight = False
        else:
            cardsRanks = [myCard.rank for myCard in cards]

            consecutiveCards = 1
            increment = 1

            while consecutiveCards < 5:
                # handle case where corresponding rank value exceeds 14
                if ranks[card.rank] + increment > 14:
                    nextRank = ranks[card.rank] + increment - 13
                else:
                    nextRank = ranks[card.rank] + increment

                # if a card of the next sequential rank exists in list of 7 graded cards
                if reversed_ranks[nextRank] in cardsRanks:

                    for theCard in cards:
                        if theCard.rank == reversed_ranks[nextRank]:
                            nextSuit = theCard.suit

                    consecutiveCards += 1
                    increment += 1
                    straightCards.append(Card(reversed_ranks[nextRank], nextSuit))
                # card is not the start of a straight
                else :
                    startOfStraight = False
                    straightCards.clear()
                    break
        
        if straightCards: # if it's not empty, then there must be a straight
            straightCards.insert(0,card)
            return straightCards

    return straightCards # which can be [] if no straights were found

# returns array of cards that make up the flush, returns empty array "[]" if no flush is found
def findFlushes (cards):

    flushCards = []
    flushSuit = -1

    suitCounts = {
        "spades" : 0,
        "clubs" : 0,
        "hearts" : 0,
        "diamonds" : 0
    }

    for card in cards:
        suitCounts[card.suit] += 1

    for suit in suitCounts:
        if suitCounts[suit] >= 5:
            flushSuit = suit
            for card in cards:
                if card.suit == flushSuit:
                    flushCards.append(card)

    return flushCards

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
print("\n")

checkHands()