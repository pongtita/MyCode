# -*- coding: utf-8 -*-
"""
Title: San Francisco Hold'em
Description: A game based on the Texas Hold'em variant of poker.

Author: Marcus Rabe
Change Date: 10/15/2018
Version: 1.0
"""
###############################################################################
### Package import
###############################################################################

import random
import pandas as pd
#import logging
 
###############################################################################
### Definitions
###############################################################################

###############
## constants
###############

biddingRounds = ['PreFlop', 'Flop', 'Turn', 'River']
startBudget = 50
nPlayers = 4
humanPlayerNr = 1
numberStrings = ['first ', 'second', 'third ', 'fourth', 'fifth ' ]
bidRandMod = [-5,15]
bidCards = {'PreFlop': 2,
            'Flop': 5,
            'Turn': 6,
            'River': 7}
bidRaise = {'Low': 1,
            'Medium': 3,
            'High': 7}
# bid Strength per Card
bidStrength = {'Low': 5,
               'Medium': 15,
               'High': 25}
playersOrder = list(range(1,nPlayers+1))
random.shuffle(playersOrder)

###############
## data structures
###############

cards = {'Color':['Clubs']*13+['Diamonds']*13+['Hearts']*13+['Spades']*13,
         'Rank':[1,2,3,4,5,6,7,8,9,10,11,12,13]*4,
         'Rank_Name': ['2','3','4','5','6','7','8','9','10','Jack','Queen','King','Ace']*4,
         'Owner':[0]*52,
         'Draw':[0]*52}
cards_df = pd.DataFrame(cards)
cards_master = cards_df

## moneys
# Player: Integer - number of player
# Budget: Integer - current remaining budget
# BidAmount: Integer - amounts placed
# BidStatus:
    # -1: not bidded in round
    # 0: fold
    # 1: call
    # 2: raise
# BidTurn: Integer [1,2] - the round of the bid
moneys = {'Player': list(range(1,nPlayers+1)),
          'Budget': [startBudget]*nPlayers,
          'BidAmount': [0]*nPlayers,
          'BidStatus': [-1]*nPlayers,
          'BidTurn': [0]*nPlayers}
moneys_df = pd.DataFrame(moneys)
moneys_df = moneys_df.set_index('Player')

###############
## other
###############

gameOn_B = True
win = 0
#logging.basicConfig(filename='SFHE.log',
#                    filemode='w',
#                    level=logging.DEBUG,
#                    format='%(%(asctime)s - levelname)s - %(message)s')

###############################################################################
### Define utility functions
###############################################################################

def draw_card(df):
    """
    ###############
    ## draw_card
    ###############
        # returns a random card that has not already been taken
    # Input:
        # df: cards_df
    # Output:
        # choice: Integer - the number (in df) of the card chosen
    ###############
    """
    
    choice = random.randint(0,51)
    while df.iloc[choice]['Owner'] != 0:
        choice = random.randint(0,51)
    return choice
    
def set_player(df, player, card_ind, numDraw):
    """
    ###############
    ## set_player
    ###############
        # sets the ownership and the draw in df
    # Input:
        # df: cards_df
        # player: Integer - number of cardOwner
        # card_ind: Integer - index of the card to set
        # numDraw: Integer [1:7] - number of the round the card was drawn
    # Output:
        # df: cards_df
    ###############
    """
    
    df.loc[[card_ind],['Owner']] = player
    df.loc[[card_ind],['Draw']] = numDraw
    return df

def extractNames (df, draw, owner = humanPlayerNr):
    """
    ###############
    ## extractNames
    ###############
        # extracts card rank and color for a given draw and owner
    # Input:
        # df: cards_df
        # draw: Integer [1:7] - number of the round the card was drawn
        # owner: Integer (def: humanPlayerNr) - number of cardOwner
    # Output:
        # rank: String - the card rank
        # color: String - the card color
    ###############
    """
    
    card = df[((df.Owner == owner) & (df.Draw == draw))]
    rank = card.iloc[0]['Rank_Name']
    color = card.iloc[0]['Color']
    return rank, color

def placeBid (df, amount, playerNumber):
    """
    ###############
    ## placeBid
    ###############
        # processes a player's bid and returns the success as well as a display string
    # inputs
        # df: moneys_df
        # amount: integer - amount of bid to place (-1 for fold)
        # playerNumber: integer the number of the player placing the bid
    # outputs
        # sucess: [0,1,2] - 0: no sucess - budget to low, 1: sucess, 2: folded, 3: bid to low
        # display: str - Displaystring
    ###############
    """
    
    if amount == -2:
        return df, 0, f"""
Please input a valid number (Integer) for your bid. If you want to fold input -1."""
    if amount == -9:
        df.loc[[playerNumber],["Budget"]] += 100
        return df, 0, f"""
You have been given $100."""
    # first bidding turn raise allowed
    if df.BidTurn[playerNumber] == 1:
        #not enough money
        if df.Budget[playerNumber] < amount:
            return df, 0, f"""
Your Budget of ${df.Budget[playerNumber]} does not cover the amount you are trying to bid. Please enter a valid amount or -1 to fold."""
        # fold
        if amount == -1:
            df.loc[[playerNumber],['BidStatus']] = 0
            return df, 2, f"""
You have folded. Your remaining budget is ${df.Budget[playerNumber]}."""
        # temp bid
        minBid = df['BidAmount'].max() - df.iloc[playerNumber-1]['BidAmount']
        maxBidAmount = df['BidAmount'].max()
        df.loc[[playerNumber],['BidAmount']] += amount
        if ((df['BidAmount'] > df.iloc[playerNumber-1]['BidAmount']).any()):
        #if (df['BidAmount'] <= minBid):
            # bid to low - revert bid
            df.loc[[playerNumber],['BidAmount']] -= amount
            minBid = df['BidAmount'].max() - df.iloc[playerNumber-1]['BidAmount']
            return df, 3, f"""
You have to bid a minimum of ${minBid} to call or raise. Bid -1 to fold."""
        else:
            if maxBidAmount == df.iloc[playerNumber-1]['BidAmount']:
                # call
                df.loc[[playerNumber],['BidStatus']] = 1
                df.loc[[playerNumber],['Budget']] -= amount
            else:
                df.loc[[playerNumber],['BidStatus']] = 2
                df.loc[[playerNumber],['Budget']] -= amount
            return df, 1, f"""Your bid was placed successfully."""
    # second bidding turn - only call allowed
    else:
        #not enough money
        if df.Budget[playerNumber-1] < amount:
            return df, 0, f"""
Your Budget of ${df.Budget[playerNumber]} does not cover the amount you are trying to bid. Please enter a valid amount or -1 to fold."""
        # fold
        if amount == -1:
            df.loc[[playerNumber],['BidStatus']] = 0
            return df, 2, f"""
You have folded. Your remaining budget is ${df.Budget[playerNumber]}."""
        # temp bid
        callBid = df['BidAmount'].max() - df.iloc[playerNumber-1]['BidAmount']
        df.loc[[playerNumber],['BidAmount']] += amount
        if not(amount == callBid):
            # bid to low - revert bid
            df.loc[[playerNumber],['BidAmount']] -= amount
            return df, 3, f"""You have to bid ${callBid} to call. Bid -1 to fold."""
        else:
            df.loc[[playerNumber],['BidStatus']] = 1
            df.loc[[playerNumber],['Budget']] -= amount
            return df, 1, f"""Your bid was placed successfully."""
        
def printBids (Bids, Players, playersStatus):
    """
    ###############
    ## printBids
    ###############
        # loops through the bids and displays them
    # Input:
        # Bids: list of Integers - bid values
        # Players: list of Integers - Player Numbers in bidding order
        # playersStatus:
            # -1: not bidded in round
            # 0: fold
            # 1: call
            # 2: raise
    ###############
    """
    
    print("            Bid      Status\n")
    #for i in range(1,len(Players)+1):
    for i in playersOrder:
        stat = ''
        if playersStatus[i-1] == 0:
            stat = 'folded'
        elif playersStatus[i-1] == 1:
            stat = 'called'
        elif playersStatus[i-1] == 2:
            stat = 'raised'
        else:
            stat = 'not bidded in this round'
        if i == 1:
            print(f"""You     :   ${Bids[i-1]}      {stat}""")
        else:
            print(f"""Player {i}:   ${Bids[i-1]}      {stat}""")

def generateBid (moneys_df, cards_df, player, bidRound):
    """
    ###############
    ## generateBid
    ###############
        # generates bids for computer players
    # Input:
        # moneys_df: moneys_df
        # cards_df: cards_df
        # player: Integer - number of player to generate for
        # bidRound: String [bidCards] - the current bidding round
    # Output:
        # bid: Integer
    ###############
    """
    
    DeckStrength = calculateStrength(cards_df, player)
    numCards = bidCards[bidRound]
    modifier = random.randint(bidRandMod[0],bidRandMod[1])
    totalStrength = (sum(DeckStrength)/numCards)+ modifier
    currentMaxBid = max(moneys_df.BidAmount)
    currentOwnBid = moneys_df.iloc[player-1]['BidAmount']
    callBid = currentMaxBid - currentOwnBid
    if totalStrength < bidStrength['Low']:
        # fold
        return -1
    elif totalStrength < bidStrength['Medium']:
        if callBid == 0:
            # raise if no-one raised so far
            return bidRaise['Low']
        elif callBid <= bidRaise['Medium']:
            # call if not to much
            return callBid
        else:
            #fold
            return -1
    elif totalStrength < bidStrength['High']:
        if callBid == 0:
            # raise if no-one raised so far
            return bidRaise['Medium']
        elif callBid <= bidRaise['High']:
            # call if not to much
            return callBid
        else:
            #fold
            return -1
    else:
        if callBid == 0:
            # raise if no-one raised so far
            return bidRaise['High']
        elif callBid <= moneys_df.iloc[player-1]['Budget']:
            # call if affordable
            return callBid
        else:
            #fold
            return -1

def calculateStrength (cards_df, player):
    """
    ###############
    ## calculateStrength
    ###############
        #calculates tbe strength of a hand's cards based on the card
        # rank multiplied by the number of same colors held
    # Input:
        # cards_df
        # player: the number of the player for whom to calculate
    # Output:
        # DeckStrength: list of Integers - Strength values for the individual cards
    ###############
    """
    
    ownCards = cards_df[((cards_df.Owner == player )| (cards_df.Owner == 5))]
    colorCounts = ownCards.Color.value_counts()
    DeckStrength = [0]*ownCards.count().max()
    for i in range(ownCards.count().max()):
        DeckStrength[i] = ownCards.iloc[i]['Rank']*colorCounts[ownCards.iloc[i]['Color']] 
    return DeckStrength


def bidding (df, biddingRound, playersOrder, cards_df, nPlayers):
    """
    ###############
    ## bidding
    ###############
        # control for a round of bidding
    # Input:
        # df: moneys_df
        # bidding_round = String of biddingRounds
        # playersOrder: List of Integer - player numbers i order
        # cards_df: cards_df
    # Output:
        # df: moneys_df
    ###############
    """
    
    win = 0
    # reset bid status for round (for the ones that are still in the game)
    for ind, row in moneys_df.iterrows():
        if moneys_df.iloc[ind-1]['BidStatus'] != 0:
            moneys_df.loc[[ind],['BidStatus']] = -1
    for turn in [1,2]:
        # turn 1
        for i in playersOrder:
            # if not folded
            if not moneys_df.iloc[i-1]['BidStatus'] == 0:
                df.loc[[i],['BidTurn']] = turn
                currentBids = list(df['BidAmount'])
                playersStatus = list(df['BidStatus'])
                if not((turn == 2) and (moneys_df.iloc[i-1]['BidAmount'] == max(currentBids))):
                    # on the second turn only alow calls
                    # human player?
                    if i == humanPlayerNr:
                        print(f"""The current bids for the {biddingRound} are:""")
                        printBids(currentBids, playersOrder, playersStatus)
                        print('\n')
                        print(f"""Your remaining budget is: ${df.Budget[i]}""")
                        bidInp = input('Please input your bid: ')
                        bidInp = checkBidInput(bidInp)
                        df, success, display = placeBid(df, amount=bidInp, playerNumber=i)
                        while not(success == 1 or success == 2):
                            print(display)
                            bidInp = input('\nPlease input a valid bid: ')
                            bidInp = checkBidInput(bidInp)
                            df, success, display = placeBid(df, amount=bidInp, playerNumber=i)
                        print(display)
                        print("\nPress any key to continue")
                        input("< ")
                    # computer player
                    else:
                        bidInp = generateBid(df, cards_df, i, biddingRound)
                        df, success, display = placeBid(df, amount=bidInp, playerNumber=i)
                        while not(success == 1 or success ==2):
                            bidInp = generateBid(df, cards_df, i, biddingRound)
                            df, success, display = placeBid(df, amount=bidInp, playerNumber=i)
            win = checkWin(df, biddingRound='Flop', nPlayers = nPlayers, cards_df = cards_df)
            if win != 0:
                # someone has already one - stop bidding
                return df, win
    return df, win

def checkBidInput(inp):
    """
    ###############
    ## checkBidInput
    ###############
        # checks the input for validity
    # Input:
        # inp: String
    # Output:
        # int
            # 0:inf - amount to be bid
            # -1:   - key for fold
            # -2:   - error - reprompt user
            # -9:   - cheat mode - add 100
    ###############
    """
    if inp == "cheat":
        return -9
    try:
        x = int(inp)
    except Exception:
        return -2
    if x >= -1:
        return x
    else:
        return -2

def checkWin (df, biddingRound, nPlayers, cards_df):
    """
    ###############
    ## checkWin
    ###############
        # check if a player has won
    # Input:
        # df: moneys_df
        # bidding_round: String of biddingRounds
        # nPlayers: nPlayers
        # cards_df: cards_df
    # Output:
        # int
            # 0 - no win
            # other - player number of winner
    ###############
    """
    
    if biddingRound == 'River':
        # End reached - evaluate win by points
        winVal = [0]*(nPlayers+1) # create empty array
        for i in range(1, nPlayers+1):
            # go through players and retrieve card strength value
            winVal[i] = sum(calculateStrength(cards_df, i))
        return winVal.index(max(winVal)) # return index of player with highest score
    
    else:
        # Still in bidding - can only win through folding opponents
        counts = df.BidStatus.value_counts()
        if counts.index.contains(0):
            if counts[0] == nPlayers -1:
                # someone has one by opponents folding
                return int((df.index[df.BidStatus != 0]).values)
            else:
                # no win
                return 0
        else:
            # no win
            return 0

def calculatePotSize (moneys_df):
    """
    ###############
    ## calculatePotSize
    ###############
        # calculates the money in the pot
    # Input:
        # moneys_df: moneys_df
    # Output:
        # int - money won
    ###############
    """
    return sum(moneys_df.BidAmount)

def askForNewGame():
    """
    ###############
    ## askForNewGame
    ###############
        # askes the user if the game shall be continued
    # Input:
    # Output:
        # bool
            # True: carry on
            # False: stop game
    ###############
    """
    print("\f")
    print("Do you want to play another round?\n")
    print("Enter Y for Yes or N for No:")
    answer = input("< ")
    answer = answer.upper()
    while not(answer == "Y" or answer == "N"):
        answer = input("Enter Y for Yes or N for No")
        answer = answer.upper()
    if answer == "Y":
        return True
    else:
        return False
    
def displayHelp():
    """
    ###############
    ## displayHelp
    ###############
        # Displays the Help text to the user
    # Input:
    # Output:
    ###############
    """
    print(f"""
\f\n\n
San Francisco Hold'em is based on the Texas Hold'em variant of poker.

The game follows the same sequence of getting cards and bidding on them.
There are 4 bidding rounds:
    1. Pre-Flop - Players only know the two cards they are not sharing.
    2. Flop     - Players can see their own cards plus 3 community cards which
                  are shared by all players.
    3. River    - Another community card is added.
    4. Turn     - The last community card is added.
In each round each player can either:
    Raise - Bid a higher amount than the current highest.
    Call  - Bid to match the current highest amount.
    Fold  - Don't bid. If you fold you have no chance to win this pot. Bid -1 to fold.
There are two ways in which a player can win the game:
    1. If all other players fold.
    2. If there are still at least two players in the game after the 4th bidding
       round the player with the best cards will win.
The value of the cards is calculated as follows:
    Multiply the number of cards you own (including the community cards) in the
    card's color by the value of the individual card (the number value on the
    card or Jack=10, Queen=11, King=12, Ace=13) for each card and sum them up.
    E.g. you have the following deck:
        9 of Clubs         - 3 * 9 = 27
        5 of Diamonds      - 2 * 5 = 10
        3 of Clubs         - 3 * 3 =  9
        Queen of Diamonds  - 1 *11 = 11
        5 of Clubs         - 3 * 5 = 15
        Ace of Spades      - 1 *13 = 13
        2 of Hearts        - 1 * 2 =  2
        Total                      = 87
    
You are starting the game with a start budget of ${startBudget}.
There will be {nPlayers-1} computer opponents playing against you.

Be careful - the computer opponents seem to have drunken a fair bit already
and are not always making rational decisions. Also they have been seen to cheat
from time to time.

Enjoy the game!
""")
    
def displayIntro():
    """
    ###############
    ## displayIntro
    ###############
        # Displays the introduction text to the user
    # Input:
    # Output:
    ###############
    """
    print(f"""
\f\n\n
Hello player\n\nYou are about to embark onto a game of
SanFrancisco Hold'em.\n
You are playing against {nPlayers-1} opponents.\n
Everybody is starting with a budget of ${startBudget}.\n""")


###############################################################################
### Main flow
###############################################################################
    
## Introduction

displayIntro()

print("Press 'h' for help or any other key to start the game.")
if input('< ').upper() == 'H':
    displayHelp()
    print("\n\nPress any key to start the game.")
    input('< ')

## Main Loop
while gameOn_B:
    
    if win != 0:
        # someone has one the game
        moneyWon = calculatePotSize(moneys_df)
        moneys_df.loc[[win],['Budget']] += moneyWon
        if win == 1:
            print(f"""\f\nYou have won ${moneyWon}.""")
        else:
            print(f"""\f\nPlayer {win} has won ${moneyWon}.""")
        print("Press any key to continue.\n")
        input('< ')
        gameOn_B = askForNewGame()
        # reset the game
        win = 0
        cards_df = cards_master
        moneys_df.BidAmount = 0
        moneys_df.BidStatus = -1
        moneys_df.BidTurn = 0
    if not gameOn_B:
        # end game
        break
    
    ##### Pre Flop
    # Assign cards to players
    print("\f\n")
    for player in playersOrder:
        # Assign two cards each
        for i in [1,2]:
            cards_df = set_player(cards_df, player, draw_card(cards_df), i)
            if player == humanPlayerNr:
                # Tell player about his cards
                cardRank, cardColor = extractNames(cards_df, draw=i)
                print(f"""Your {numberStrings[i-1]} card is:            {cardRank} of {cardColor}""")
    print('\n')
    # Start bidding round
    moneys_df, win = bidding(moneys_df, 'PreFlop', playersOrder, cards_df, nPlayers)
    if win != 0:
        continue
    
    ##### Flop
    # Draw community cards
    print("\f")
    for i in [1,2]:
        cardRank, cardColor = extractNames(cards_df, draw=i, owner=humanPlayerNr)
        print(f"""Your {numberStrings[i-1]} card is:            {cardRank} of {cardColor}""")
    for i in [3,4,5]:
        cards_df = set_player(cards_df, nPlayers+1, draw_card(cards_df), i)
        # Tell player about the community cards
        cardRank, cardColor = extractNames(cards_df, draw=i, owner=5)
        print(f"""The  {numberStrings[i-3]} community card is:  {cardRank} of {cardColor}""")
    print('\n')
    # Start bidding round
    moneys_df, win = bidding(moneys_df, 'Flop', playersOrder, cards_df, nPlayers)
    if win != 0:
        continue
    
    ##### Turn
    # Draw community card
    cards_df = set_player(cards_df, nPlayers+1, draw_card(cards_df), 6)
    # Tell player about the community cards
    
    print("\f")
    for i in [1,2]:
        cardRank, cardColor = extractNames(cards_df, draw=i, owner=humanPlayerNr)
        print(f"""Your {numberStrings[i-1]} card is:            {cardRank} of {cardColor}""")
    for i in [3,4,5]:
        cardRank, cardColor = extractNames(cards_df, draw=i, owner=5)
        print(f"""The  {numberStrings[i-3]} community card is:  {cardRank} of {cardColor}""")
    cardRank, cardColor = extractNames(cards_df, draw=6, owner=5)
    print(f"""The  {numberStrings[6-3]} community card is:  {cardRank} of {cardColor}""")
    print('\n')
    # Start bidding round
    moneys_df, win = bidding(moneys_df, 'Turn', playersOrder, cards_df, nPlayers)
    if win != 0:
        continue
    
    ##### River
    # Draw community card
    cards_df = set_player(cards_df, nPlayers+1, draw_card(cards_df), 7)
    # Tell player about the community cards
    
    print("\f")
    for i in [1,2]:
        cardRank, cardColor = extractNames(cards_df, draw=i, owner=humanPlayerNr)
        print(f"""Your {numberStrings[i-1]} card is:            {cardRank} of {cardColor}""")
    for i in [3,4,5]:
        cardRank, cardColor = extractNames(cards_df, draw=i, owner=5)
        print(f"""The  {numberStrings[i-3]} community card is:  {cardRank} of {cardColor}""")
    cardRank, cardColor = extractNames(cards_df, draw=6, owner=5)
    print(f"""The  {numberStrings[6-3]} community card is:  {cardRank} of {cardColor}""")
    cardRank, cardColor = extractNames(cards_df, draw=7, owner=5)
    print(f"""The  {numberStrings[7-3]} community card is:  {cardRank} of {cardColor}""")
    print('\n')
    # Start bidding round
    moneys_df, win = bidding(moneys_df, 'River', playersOrder, cards_df, nPlayers)
    if win != 0:
        continue
    
    win = checkWin (moneys_df, 'River', nPlayers, cards_df)

print("\f")
print("Thanks for playing SanFrancisco Hold'em.")