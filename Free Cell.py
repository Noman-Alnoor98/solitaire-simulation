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



