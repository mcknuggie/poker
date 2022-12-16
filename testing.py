from gettext import find
import random, copy
from re import L

class Card:
  def __init__(self, rank, suit):
    self.rank = rank
    self.suit = suit

  def __repr__(self):
      return "%s of %s" % (self.rank, self.suit)

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

cards = []

cards.append(Card("4", "hearts"))
cards.append(Card("J", "hearts"))
cards.append(Card("3", "clubs"))
cards.append(Card("5", "diamonds"))
cards.append(Card("7", "clubs"))
cards.append(Card("Q", "spades"))
cards.append(Card("2", "hearts"))


print("cards: ", cards)

# cardRanks = [card.rank for card in cards]
# print(cardRanks)

# highCardValue = ranks[cards[0].rank]
# print(highCardValue)

# ranksDict = {}
# ranksDict['A'] = 2
# ranksDict['J'] = 1

# ranksDict['J'] += 1

# print(ranksDict)



def findStraights (cards):

    straightCards = []
    highestStraightCards = []

    for card in cards:
        startOfStraight = True
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
                    startOfStraight = False
                    straightCards.clear()
                    break
        
        if straightCards: # if it's not empty, then there must be a straight
            straightCards.insert(0,card)
            print("found a straight!", straightCards)

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


print("straight found: ", findStraights(cards))