# Connect Four: Monte Carlo Tree Search

A move generator for Connect Four (6 rows x 7 columns) based on the
Monte Carlo tree search algorithm in Figure 5.11 of the textbook
(Russell & Norvig, *Artificial Intelligence: A Modern Approach*).

## Files

| File | What it contains |
|---|---|
| `game.py` | The rules: board, valid moves, dropping a piece, win check, random playout, and the rule-based `evaluate` function (objective part of the utility) |
| `mcts.py` | The search: `Node`, `utility`, `select`, `expand`, `simulate`, `back_propagate`, and the main `mcts` function |
| `main.py` | The experiments: changes one setting at a time and prints the results |
| `tests.py` | Automated tests with their test data (small board positions with known correct answers) |

## Requirements

- Python 3.10 or newer
- pytest (for the tests only)

```
pip install pytest
```

## How to run the tests

From the `connect-four-game` folder:

```
python -m pytest -v tests.py
```

All 6 tests should pass.

The tests also run automatically on **GitHub Actions** on every push
(workflow file: `.github/workflows/connect-four-game.yml`).

## How to run the experiments

```
python main.py
```

This plays games between our MCTS and a fixed opponent (MCTS with plain
UCB1, 100 cycles) and prints the win rate for each setting. It also runs
MCTS 20 times on the empty board to check whether it always picks the
same move. The experiments take a few minutes.

