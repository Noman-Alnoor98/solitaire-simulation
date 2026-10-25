import random

SUITS = ['♠', '♥', '♦', '♣']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

#Creates the base deck of 104 total cards
def create_deck(num_suits):
    chosen_suits = SUITS[:num_suits]
    #Generate unique cards
    deck = [(rank, suit) for suit in chosen_suits for rank in RANKS]
    #Multiply deck to reach 104 cards
    deck *= (8 // num_suits)
    random.shuffle(deck)   
    #Split between table cards and stock
    return deck[:50], deck[50:]

def deal_tableau(tableau):
    #Create base table for columns of cards
    columns = [[] for _ in range(10)]
    i = 0
    #Deal cards to each column from the non-stock deck
    for col in range(10):
        #First 4 columns are 6 cards, rest are 5 cards
        count = 6 if col < 4 else 5
        #Deal cards to column face down
        for _ in range(count):
            columns[col].append({'card': tableau[i], 'visible': False})
            i += 1
        #Last card of column made face up
        columns[col][-1]['visible'] = True 
    return columns

def deal_stock(columns, stock):
    #Adds face up card from stock to each column
    for col in columns:
        card = stock.pop()
        col.append({'card': card, 'visible': True})