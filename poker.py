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
    def __init__(self, name, card1, card2, bestHand, handScore):
      self.name = name
      self.card1 = card1
      self.card2 = card2
      self.bestHand = bestHand
      self.handScore = handScore

    def __repr__(self): 
        return "%s: \ncard 1: %s \ncard 2: %s. \nBest Hand: %s" % (self.name, self.card1, self.card2, self.bestHand)

class Hand:
    def __init__(self, type, cards):
        self.type = type
        self.cards = cards

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
        playerHand = Hand("", []) # create hand for every player, but intialize them to nothing b/c we don't know their hand yet
        handScore = 0
        players.append(Player(playerName, card1, card2, playerHand, handScore))

# score the end of the round to find out which player has the best hand
"""
Hand-Ranking Hierarchy:

9 : Royal Flush
8 : Straight Flush
7 : 4 of a kind
6 : Full House
5 : Flush
4 : Straight
3 : 3 of a kind
2 : 2 Pair
1 : Pair
0 : High Card

"""


def checkHands ():
    for player in players:
        cardsToCheck = copy.deepcopy(faceUpCards)
        
        cardsToCheck.append(player.card1)
        cardsToCheck.append(player.card2)

        print(player.name, "Cards in play: ", cardsToCheck)


        duplicateRanks = findDuplicateRanks(cardsToCheck)
        print(player.name, "Duplicate Ranks:", duplicateRanks)

        if 4 in list(duplicateRanks.values()): # if there is four of a kind
            player.handScore = 7
            cardRank = list(duplicateRanks.keys())[list(duplicateRanks.values()).index(4)]
            player.bestHand.cards = [Card(cardRank, "spades"), Card(cardRank, "clubs"), Card(cardRank, "hearts"), Card(cardRank, "diamonds")]
            player.bestHand.type = "Four of a Kind"
        elif 3 in list(duplicateRanks.values()): # if there is three of a kind
            player.handScore = 3
            threeOfAKindRank = list(duplicateRanks.keys())[list(duplicateRanks.values()).index(3)]
            player.bestHand.cards.clear()
            for card in cardsToCheck:
                if card.rank == threeOfAKindRank:
                    player.bestHand.cards.append(card)  
            player.bestHand.type = "Three of a Kind"
            if 2 in list(duplicateRanks.values()): # if there is a full house
                player.handScore = 6
                player.bestHand.type = "Full House"
                maxRank = '2'
                if list(duplicateRanks.values()).count(2) == 2: # if there are two pairs within the full house
                    for currRank, count in duplicateRanks.items():
                        if count == 2:
                            if ranks[currRank] > ranks[maxRank]:
                                maxRank = currRank
                    for card in cardsToCheck:
                        if card.rank == maxRank:
                            player.bestHand.cards.append(card)
                else: # if there is only one pair within the full house
                    # first find the rank of the pair and store in pairRank
                    for currRank, count in duplicateRanks.items():
                        if count == 2:
                            pairRank = currRank
                    # then store all cards in cardsToCheck into the player's bestHand
                    for card in cardsToCheck:
                        if card.rank == pairRank:
                            player.bestHand.cards.append(card)

        elif 2 in list(duplicateRanks.values()): # if there is a pair
            player.handScore = 1
            player.bestHand.type = "Pair"
            # iterate through dictionary and count how many pairs there are
            pairRanks = []
            for rank, count in duplicateRanks.items():
                if count == 2:
                    pairRanks.append(rank)

            if len(pairRanks) == 2: # if there are exactly 2 pairs
                player.handScore = 2
                player.bestHand.type = "Two Pair"
                for card in cardsToCheck:
                    for rank in pairRanks:
                        if rank == card.rank:
                            player.bestHand.cards.append(card)

            elif len(pairRanks) == 3: # if there are exactly 3 pairs
                player.handScore = 2
                player.bestHand.type = "Two Pair"

                minRank = pairRanks[0]
                for currRank in pairRanks:
                    if ranks[currRank] < ranks[minRank]:
                        minRank = currRank
                # now remove the smallest rank
                pairRanks.remove(minRank)
                # now that we have only 2 ranks, we can find that two-pair in cardsToCheck
                for card in cardsToCheck:
                    for rank in pairRanks:
                        if rank == card.rank:
                            player.bestHand.cards.append(card)

            else: # if there is really only one pair
                player.bestHand.cards.clear()
                for card in cardsToCheck:
                    if card.rank == pairRanks[0]:
                        player.bestHand.cards.append(card)

        straightCards = findStraights(cardsToCheck)
        print(player.name, "Straight Cards: ", straightCards)
        hasStraight = False

        if len(straightCards) == 5 and player.handScore < 4: # if there is a straight
                player.handScore = 4
                player.bestHand.cards = straightCards
                player.bestHand.type = "Straight"
                hasStraight = True




        flushCards = findFlushes(cardsToCheck)
        print(player.name, "Flush Cards: ", flushCards)

        if len(flushCards) == 5 and player.handScore < 5: # if there is a flush
            player.handScore = 5
            player.bestHand.cards = flushCards
            player.bestHand.type = "Flush"
            if hasStraight == True:
                # now need to check is straight cards are the same as the flush cards
                if set(flushCards) == set(straightCards): # if there is a straight flush
                    player.handScore = 8
                    player.bestHand.type = "Straight Flush"
                    for straightFlushCard in straightCards:
                        player.bestHand.cards.append(straightFlushCard)

                    flushRanks = []
                    for card in flushCards:
                        flushRanks.append(card.rank)
                    if set(['10', 'J', 'Q', 'K', 'A']).issubset(flushRanks): # if there is a royal flush
                        player.handScore = 9
                        player.bestHand.type = "Royal Flush"

        if player.handScore == 0:
            player.bestHand.type = "High Card"
            highCard = findHighCard(cardsToCheck)
            player.bestHand.cards.clear()
            player.bestHand.cards.append(highCard)
            # print(player.name, "High Card: ", highCard)
                

        print("Hand Score: ", player.handScore)
        print("Best Hand Type: ", player.bestHand.type)
        print("Best Hand Cards: ", player.bestHand.cards)
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
    return uniqueRanks



# returns the array of cards that make up the straight, returns empty array "[]" if no straight is found
def findStraights (cards):

    straightCards = []
    highestStraightCards = []

    for card in cards:
        if ranks[card.rank] > 10 and ranks[card.rank] != 14: # J, Q, K can't start straight
            continue
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
                    straightCards.clear()
                    break
        
        if straightCards: # if it's not empty, then there must be a straight
            straightCards.insert(0,card)

            # if highestStraightCards is empty
            if not highestStraightCards:
                highestStraightCards = copy.deepcopy(straightCards)
                straightCards.clear()

            # compare the highest value in the straight
            elif ranks[straightCards[4].rank] > ranks[highestStraightCards[4].rank]:
                highestStraightCards.clear()
                highestStraightCards = copy.deepcopy(straightCards)
                straightCards.clear()

    return highestStraightCards # which can be [] if no straights were found

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


# FUNCTION CALLS

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