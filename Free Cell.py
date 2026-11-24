import random

suits = ["♠", "♥", "♦", "♣"]
ranks = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
def create_deck():
    deck = []

    for i in suits:
        for j in ranks:
            deck.append((j,i))
    return deck

deck = create_deck()


def shuffle_deck(deck , seed = None):
    deck_copy = deck.copy()
    rng = random.Random(seed)
    rng.shuffle(deck_copy)
    return deck_copy

def deal_freecell(deck):
    deck_copy = deck.copy()
    tableau = [[],[],[],[],[],[],[],[]]
    for i in range(len(deck_copy)):
        card = deck_copy.pop()
        tableau[i%8].append({"card":card,"face_up": True})
    return tableau



def new_game(seed = None):
    deck = create_deck()
    shuffled = shuffle_deck(deck,seed = seed)
    columns = deal_freecell(shuffled)
    free_cells = [None]*4
    
    foundations = {s:[] for s in suits}

    return {
        "columns": columns,
        "free_cells": free_cells,
        "foundations": foundations,
    }


def move_to_freecell(game,column_index,cell_index):
    columns = game["columns"]
    free_cells = game["free_cells"]
    if not (0<=column_index<len(columns)):
        print("Index is Invalid")
        return False
    if len(columns[column_index]) == 0:
        print("Column is Empty")
        return False
    if not (0 <= cell_index < len(free_cells)):
        print("free cell index is invalid")
        return False
    if free_cells[cell_index] is not None :
        print("Free Cell is not Empty")
        return False

    card = columns[column_index].pop()
    free_cells[cell_index] = card
    return True

def rank_value(card):
    return ranks.index(card[0]) +1


colors = {
    "♠":"Black",
     "♥":"Red",
    "♦":"Red",
     "♣":"Black"
}

def can_be_placed(card,column):
    if len(column) == 0 :
        return True
    else:
        moving = card["card"]
        target = column[-1]["card"]
        if rank_value(target) != (rank_value(moving)+1):
            return False
        if colors[moving[1]] == colors[target[1]]:
            return False
        
    return True

def move_across_cols(game,source_index,destination_index):
    columns = game["columns"]
    if not (0<=source_index<len(columns) and (0<=destination_index<len(columns))):
        print("Index is Invalid")
        return False
    if source_index == destination_index:
        return False
    if len(columns[source_index]) == 0:
        return False
    card = columns[source_index][-1]
    if not can_be_placed(card,columns[destination_index]):
        return False
    moving_card = columns[source_index].pop()
    columns[destination_index].append(moving_card)
    return True


def move_from_freecell(game,cell_index,column_index):
    columns = game["columns"]
    free_cells = game["free_cells"]
    if not (0<=column_index<len(columns)):
        print("Index is Invalid")
        return False
    if not (0 <= cell_index < len(free_cells)):
        print("free cell index is invalid")
        return False
    if free_cells[cell_index] is  None:
        print("Free Cell is Empty")
        return False

    card = free_cells[cell_index]
    if not can_be_placed(card,columns[column_index]):
        return False
    columns[column_index].append(card)
    free_cells[cell_index] = None
    return  True


def foundation_move_check(card,foundation):
    moving = card["card"]
    foundation_empty = True
    if len(foundation) != 0:
        foundation_empty = False
    if foundation_empty:
        if moving[0] == "A":
            return True
    else:
        target = foundation[-1]["card"]
        if moving[1] == target[1] and rank_value(moving) == rank_value(target) + 1:
            return True
    return False


def move_column_to_foundation(game,column_index):
    columns = game["columns"]
    foundations = game["foundations"]

    if not (0 <= column_index < len(columns)):
        return False

    if len(columns[column_index]) == 0:
        return False
    
    card = columns[column_index][-1]
    suit = card["card"][1]
    foundation = foundations[suit]
    if  foundation_move_check(card,foundation):
         moving_card = columns[column_index].pop()
         foundation.append(moving_card)
         return True
    return False



def move_freecell_to_foundation(game,freecell_index):
    freecells = game["free_cells"]
    foundations = game["foundations"]

    if not (0 <= freecell_index < len(freecells)):
        return False

    if freecells[freecell_index] is None:
        return False

    card = freecells[freecell_index]
    suit = card["card"][1]
    foundation = foundations[suit]
    if  foundation_move_check(card,foundation):
         freecells[freecell_index] = None
         foundation.append(card)
         return True
    return False


def game_won(game):
    foundations = game["foundations"]
    while True:
        for foundation in foundations.values():
            if len(foundation) != 13:
                return False
        break
    return True


def legal_move(game):
    columns = game["columns"]
    free_cells = game["free_cells"]
    foundations = game["foundations"]
    moves = []
    for i in range(len(columns)):
        if len(columns[i]) == 0:
            continue
        source_card = columns[i][-1]
        suit = source_card["card"][1]
        foundation = foundations[suit]

        if foundation_move_check(source_card, foundation):
            moves.append({
                            "type": "column_to_foundation",
                            "source": i,
                            "destination": suit
            })
        for j in range(len(columns)):
            if i == j:
                continue
            if can_be_placed(source_card,columns[j]):
                moves.append(
                    {"type" : "column_to_column",
                    "source": i,
                    "destination":j
                    }
                )
        for j in range(len(free_cells)):
            if free_cells[j] is None:
                moves.append({
                    "type": "column_to_freecell",
                    "source": i,
                    "destination":j
                })
    for i in range(len(free_cells)):
            if free_cells[i] is None:
                continue
            card = free_cells[i]
            source_card = columns[i][-1]
            suit = source_card["card"][1]
            foundation = foundations[suit]

            if foundation_move_check(card, foundation):
                moves.append({
                            "type": "freecell_to_foundation",
                            "source": i,
                            "destination": suit
                                })
            for j in range(len(columns)):
                if can_be_placed(card,columns[j]):
                    moves.append({
                        "type":"freecell_to_column",
                        "source":i,
                        "destination":j
                    })

    return moves





