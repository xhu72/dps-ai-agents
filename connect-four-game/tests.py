"""tests.py - run with:  python -m pytest tests.py"""
from game import new_board, drop, is_win, valid_moves, random_playout
from mcts import mcts


def test_pieces_stack():
    b = new_board()
    drop(b, 3, 'X')
    drop(b, 3, 'O')
    assert b[0][3] == 'X' and b[1][3] == 'O'


def test_full_column_not_legal():
    b = new_board()
    for i in range(6):
        drop(b, 0, 'X' if i % 2 else 'O')
    assert 0 not in valid_moves(b)


def test_horizontal_win():
    b = new_board()
    for c in range(4):
        r = drop(b, c, 'X')
    assert is_win(b, r, 3, 'X')


def test_playout_finishes():
    assert random_playout(new_board(), 'X') in ('X', 'O', None)


def test_mcts_takes_the_win():
    b = new_board()
    for c in range(3):
        drop(b, c, 'X')
        drop(b, c, 'O')
    assert mcts(b, 'X', cycles=300) == 3


def test_mcts_blocks():
    b = new_board()
    for c in (4, 5, 6):
        drop(b, c, 'O')
    drop(b, 0, 'X'); drop(b, 0, 'X'); drop(b, 1, 'X')
    assert mcts(b, 'X', cycles=500) == 3
