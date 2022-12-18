# Texas Hold-em
## Description
Python that simulates the general rules and scoring of Texas hold'em.

## Usage
Run poker.py, and it will randomly generate *numPlayers* poker hands, automatically score them, and declare a winner.

## Classes
We make use of classes and objects of those classes with the *Player*, *Card*, and *Hand* classes. I also have setup a *def \_\_repr\_\_* function for each of the three classes that allow for clearer printing.

## Global Variables
 - *ranks* : a dictionary that allows you to convert the "rank" of a card into a hierarchical structure that can compare whether a card's rank is less than, greater than, or equal to another.
 - *reversed_ranks* : a dictionary similar to *ranks*, except is allows conversion from the numerical value back to the original character
 - *suits* : a list that contains all possible card suits
 - *dealtCards* : a list (initially empty) containing every single *Card* already dealt from the deck this round
 - *faceUpCards* : a list containing every *Card* dealt "face up on the table"
 - *numPlayers* : an numerical value representing the number of two-*Card* pairings to be generated and appended to *dealtCards*
 - *players* : a list that contains every *Player* in the game.

## Functions

### *dealCard()*
- creates a new *Card* with a randomly selected rank from *ranks* and suit form *suits*.

### *dealFlop()* ; *dealTurn()* ; *dealRiver()*
- all three above functions simply deal a *Card* by calling *dealCard()* and append it to *faceUpCards*

### *dealHands()*
- generates two *Card*s to each of the *numPlayers* *Player*s
- also gives each *Player* a *name*, *bestHand* (initially empty), and *handScore* (initially 0).

### *checkHands()*
- following five cards being dealt faceup (appended to *faceUpCards*), this function "grades" each *Player*'s hand of 7 *Cards* (5 faceup, 2 dealt to the *Player*).
- the grading is done by using the real rules of Texas Hold-Em to give each *Player*'s *bestHand* a *type* (i.e. High Card, Pair, Two Pair, 3 of a Kind, Straight, Flush, Full House, 4 of a Kind, Striaght Flush, or Royal Flush) and a list of *Card*'s that makeup that type. Each *Player* is also given a *handScore*, which is a numerical value the gets higher the better the *Hand*.

### *findWinner()*
- compares the *handScore* of every *Player* and returns the *Player* with the largest *handScore*

### *findHighCard()*
- helper function that

### *findHighCard(cards)*
- 

### *findDuplicateRanks(cards)*
-

### *findStraights(cards)*
-

### *findFlushes(cards)*
-

