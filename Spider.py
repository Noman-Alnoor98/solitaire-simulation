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
    return deck[:54], deck[54:]

def deal_tableau(tableau):
    #Create base table for columns of cards
    columns, i = [], 0
    #Deal cards to each column from the non-stock deck
    for col in range(10):
        #First 4 columns are 6 cards, rest are 5 cards
        if col < 4:
            count = 6
        else:
            count = 5
        #Deal cards to column face down
        cards = []
        for c in tableau[i:i + count]:
            cards.append({'card': c, 'face_up': False})
        #Last card of column made face up
        cards[len(cards) - 1]['face_up'] = True
        columns.append(cards)
        i += count   
    return columns

def deal_stock(columns, stock):
    #Adds face up card from stock to each column
    for col in columns:
        card = stock.pop()
        col.append({'card': card, 'face_up': True})

def rank_value(card):
    return RANKS.index(card[0])

def show(columns):
    for i in range(len(columns)):
        col = columns[i]
        cards = []
        for c in col:
            if c['face_up']:
                #Face up cards
                rank = c['card'][0]
                suit = c['card'][1]
                cards.append(rank + suit)
            else:
                #Face down cards
                cards.append('##')
        #Print card columns
        print(i, ' '.join(cards))

def is_valid_run(cards):
    if len(cards) == 0 or not cards[0]['face_up']:
        return False
    #Compares each set of adjacent cards
    for i in range(len(cards) - 1):
        a = cards[i]
        b = cards[i + 1]
        if b['face_up'] == False:
            return False
        #Checks that suits are the same
        if a['card'][1] != b['card'][1]:                       
            return False
        #Checks that the next card has a rank one less than the current
        if rank_value(a['card']) != rank_value(b['card']) + 1:
            return False
    #Run is valid
    return True

def move(columns, src, start, dst):
    #Cannot move to same column
    if src == dst:
        return False
    #Selected run
    run = columns[src][start:]
    #Checks run is valid
    if not is_valid_run(run):
        return False
    target = columns[dst]
    #If last card of target column is not 1 less than first card of moving run
    if target and rank_value(target[-1]['card']) != rank_value(run[0]['card']) + 1:
        return False
    #Remove run from source column
    del columns[src][start:]
    #Append run to dest column
    for c in run:
        target.append(c)
    #Flip last card in column if cards still present
    if len(columns[src]) > 0:
        columns[src][-1]['face_up'] = True   
    return True

def play(num_suits):
    tableau, stock = create_deck(num_suits)
    columns = deal_tableau(tableau)
    while True:
        print()
        show(columns)
        print(f"stock: {len(stock)} cards")
        cmd = input("'src start dst', 'd' to deal, 'q' to quit: ").split()
        #Quit
        if cmd == ['q']:
            break
        #Deal
        if cmd == ['d']:
            if stock:
                deal_stock(columns, stock)
            else:
                print("Stock is empty.")
            continue
        try:
            src, start, dst = map(int, cmd)
            if move(columns, src, start, dst) == False:
                print("Invalid move.")
        except (ValueError, IndexError):
            print("Type three numbers, columns 0-9.")

play(4)