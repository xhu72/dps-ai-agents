"""experiments.py - tests MCTS. It changes one setting at a time, plays games, and prints the results..
    python experiments.py
"""
import random
from collections import Counter

from game import new_board, valid_moves, drop, is_win, other
from mcts import mcts

REFERENCE = {'cycles': 100, 'w': 0}     # fixed opponent: plain UCB1, 100 cycles

def choose_move(board, player, mcts_player, settings):
    """Pick a column: MCTS for its own turns, random for the opponent."""
    if player == mcts_player:
        return mcts(board, player, **settings)       # MCTS thinks
    else:
        #return random.choice(valid_moves(board))     # opponent plays randomly
        return mcts(board, player, **REFERENCE)


def play_game(settings, mcts_is_x=True):
    """Play one game: MCTS against a random player. Returns True if MCTS won, False if it lost or drew."""
    board = new_board()
    player = 'X'                                     # X always moves first

    if mcts_is_x:
        mcts_player = 'X'
    else:
        mcts_player = 'O'

    while len(valid_moves(board)) > 0:               # until the board is full
        col = choose_move(board, player, mcts_player, settings)
        row = drop(board, col, player)

        if is_win(board, row, col, player):          # someone won
            if player == mcts_player:
                return True                          # MCTS won
            else:
                return False                         # random player won

        player = other(player)                       # next player's turn

    return False                                     # board full: draw


def win_rate(settings, games=10):
    """Play several games and return the fraction MCTS won (0.0 to 1.0)."""
    wins = 0
    for game_number in range(games):
        # take turns going first: even games MCTS is X, odd games it is O
        if game_number % 2 == 0:
            mcts_goes_first = True
        else:
            mcts_goes_first = False

        if play_game(settings, mcts_is_x=mcts_goes_first):
            wins = wins + 1

    return wins / games


def same_move_test(settings, runs=20):
    """Does MCTS pick the same move every time from the empty board?
    Runs MCTS `runs` times and counts how often each column was chosen."""
    counts = Counter()               
    for i in range(runs):
        move = mcts(new_board(), 'X', **settings)
        counts[move] = counts[move] + 1
    return counts

if __name__ == "__main__":
    print("cycles:")
    for cycles in [10, 50, 200]:
        print(f"  {cycles:4} -> win rate {win_rate({'cycles': cycles})}")
        
    print("expansion nodes x:")
    for x in [1, 3, 7]:
        print(f"  {x:4} -> win rate {win_rate({'cycles': 100, 'x': x})}")
        
    print("tree height:")
    for h in [1, 2, 4, 42]:
        print(f"  {h:4} -> win rate {win_rate({'cycles': 100, 'max_depth': h})}")
        
    print("utility weight w (0 = plain UCB1):")
    for w in [0, 0.5, 0.9]:
        print(f"  {w:4} -> win rate {win_rate({'cycles': 100, 'w': w})}")
        
    print("same move? (moves chosen on the empty board, 20 runs each)")
    for cycles in [50, 500]:
        print(f"  {cycles:4} cycles -> {dict(same_move_test({'cycles': cycles}))}")
