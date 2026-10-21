import random

def create_deck():
    deck = []
    suits = ["Spades","Hearts","Clubs","Diamonds"]
    ranks = list(range(1,14))
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

