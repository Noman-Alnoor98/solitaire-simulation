import random
from copy import deepcopy
import pandas as pd

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
            suit = card["card"][1]
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

def apply_move(game,move):
    move_type = move["type"]
    source = move["source"]
    destination = move["destination"]

    if move_type == "column_to_column":
        return move_across_cols(game,source,destination)
    if move_type == "column_to_freecell":
        return move_to_freecell(game,source,destination)
    if move_type == "freecell_to_column":
        return move_from_freecell(game,source,destination)
    if move_type == "column_to_foundation":
        return move_column_to_foundation(game,source)
    if move_type == "freecell_to_foundation":
        return move_freecell_to_foundation(game,source)
    return False
    
    
def check_moves(game):
    before = deepcopy(game)
    moves = legal_move(game)
    assert game == before, "Moves changed the board"
    for move in moves:
        trial_game = deepcopy(before)
        assert apply_move(trial_game,move) is True,(
            f"Cannot apply move : {move}"
        )
    print(f"Passed: {len(moves)} moves are working")

def random_strategy(game,moves,rng):
    assert len(moves) != 0, "No legal moves"
    return rng.choice(moves)

def simulate(strategy, game_seed,strategy_seed,max_moves = 100000):
    game = new_game(seed = game_seed)
    rng = random.Random(strategy_seed)
    moves_played = 0
    stop_reason = None
    while True:
        if not game_won(game):
            if not moves_played >= max_moves:
                moves = legal_move(game)
                if len(moves) == 0:
                    stop_reason = "no_moves_left"
                    break
                chosen_move = strategy(game,moves,rng)
                if not apply_move(game,chosen_move):
                    raise RuntimeError(f"Move was rejectd: {chosen_move}")
                moves_played += 1
            else:
                stop_reason = "move_limit_reached"
                break
        else:
            stop_reason = "game_won"
            break
    return {
        "won": stop_reason == "game_won",
        "moves": moves_played,
        "foundation_cards": sum(
            len(pile) for pile in game["foundations"].values()
                ),
        "stop_reason": stop_reason,
        "game_seed": game_seed,
        "strategy_seed": strategy_seed
    }

def simulate_games(strategy,game_seeds,strategy_seed = 1998, max_moves = 1000):
    results = []
    
    for run, seed in enumerate(game_seeds):
        result = simulate(random_strategy,game_seed=seed,strategy_seed=strategy_seed+run,max_moves=1000)
        result["strategy"]  = strategy.__name__
        result["max_moves"] = max_moves
        results.append(result)
    return results


results = simulate_games(
    random_strategy,
    game_seeds=range(1998, 2018),
    strategy_seed=42,
    max_moves=1000
)



simulation_results = pd.DataFrame(results)


print("Games played:", len(simulation_results))
print("Games won:", simulation_results["won"].sum())
print("Win rate (%):", 100 * simulation_results["won"].mean())
print("Average foundation cards:", simulation_results["foundation_cards"].mean())
print("Average moves played:", simulation_results["moves"].mean())

print("\nStopping reasons:")
print(simulation_results["stop_reason"].value_counts())