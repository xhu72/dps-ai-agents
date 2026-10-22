from game import ROWS, COLS, valid_moves, drop, is_win, other, random_playout
import math, copy, random

# ---- tree node ----------------
# each node stores the position (board, to_move, move), its links (parent, children, depth), its growth (untried) and its statistics (U, N, winner)
class Node:
    def __init__(self, board, to_move, parent=None, move=None, depth=0):
        self.board = board            # the grid at this point in the game
        self.to_move = to_move        # whose turn it is at this node
        self.parent = parent          # the node one level up. Back-propagation needs it to walk from a leaf back to the root, updating every node on the way
        self.move = move              # the column that was played to get here from the parent
        self.depth = depth            # how many moves below the root this node is
        self.children = []            # the list of nodes one level down
        self.untried = valid_moves(board) # the columns not yet turned into children
        self.U = 0.0                  # total reward (wins) for the player who moved here(1 per win, 0.5 per draw, 0 per loss)
        self.N = 0                    # number of playouts through this node
        self.winner = None            # 'X' or 'O' if the game is already won at this node, and None otherwise.
        

# ---- 1. Selection stage: the objective part, from the rules ----------------
def all_lines():
    """Return every line of 4 cells on the board (69 lines =24 horizontal + 21 vertical + 16 diagonal in one direction +16 diagonal in the other direction). Each line is a list of 4 (row, col) positions."""
    directions = [(0, 1),    # right       (horizontal)
                  (1, 0),    # up          (vertical)
                  (1, 1),    # up-right    (diagonal)
                  (1, -1)]   # up-left     (diagonal)
    lines = []
    for r in range(ROWS):
        for c in range(COLS):
            for dr, dc in directions:
                line = []
                for i in range(4):
                    line.append((r + i * dr, c + i * dc))
                if on_board(line):
                    lines.append(line)
    return lines


def on_board(line):
    """True if every cell of the line is inside the board."""
    for r, c in line:
        if r < 0 or r >= ROWS or c < 0 or c >= COLS:
            return False
    return True


def line_points(pieces, player):
    """Points for ONE line of 4 cells, from `player`'s point of view."""
    mine = pieces.count(player)
    theirs = pieces.count(other(player))
    if theirs == 0:              # only my pieces: I could still win here
        return mine * mine       # 1 piece = 1, 2 = 4, 3 = 9
    if mine == 0:                # only their pieces: they could win here
        return -(theirs * theirs)
    return 0                     # both players in it: blocked, worth nothing
  
def evaluate(board, player): 
    """Rule-based score for `player`, from 0 (bad) to 1 (good).It checks all 69 possible lines of four cells, adds up their scores, and converts the final score to a number between 0 and 1"""
    score = 0
    for line in all_lines():
        pieces = []
        for r, c in line:
            pieces.append(board[r][c])      # e.g. ['X', 'X', '.', '.']
        score = score + line_points(pieces, player)
        
    # tanh() compresses numbers into a range between -1 and 1. 
    # The number 40 controls how quickly the score approaches 0 or 1. 
    # + 1 and / 2 transform that result into a value between 0 and 1.
    return (math.tanh(score / 40) + 1) / 2 

# ---- 1. Selection stage: playout U/N + exploration ----------------
def utility(child, parent, C=1.4, w=0.5): 
    """ give each child node a score. C controls how much to explore; w controls how much to trust the rules versus the playouts.w = 0 gives the UCB1. w > 0 gives UCB1 that also listens to the game rules."""  
    if child.N == 0:
        return math.inf                                     # always try unvisited first
    playout = child.U / child.N                             # playout part
    objective = evaluate(child.board, other(child.to_move)) # objective part
    explore = C * math.sqrt(math.log(parent.N) / child.N)   # exploration part
    return (1 - w) * playout + w * objective + explore      

def can_go_deeper(node):
    """True if selection should keep walking down from this node."""
    if node.winner is not None:       # game is over here
        return False
    if len(node.untried) > 0:         # some moves not tried yet: expand HERE
        return False
    if len(node.children) == 0:       # no children (depth limit): nowhere to go
        return False
    return True


def best_child(parent, C, w):
    """The child with the highest utility."""
    best = None
    best_score = -math.inf
    for child in parent.children:
        score = utility(child, parent, C, w)
        if score > best_score:
            best = child
            best_score = score
    return best


def select(node, C, w):
    """walk down from the root, always taking the best child,
    until reaching a node where the tree should grow."""
    while can_go_deeper(node):
        node = best_child(node, C, w)
    return node
  
# ---- 2. Expansion stage: add new nodes ----------------  
def can_expand(node, max_depth):
    """True if new children can be added to this node."""
    if node.winner is not None:        # the game is already won here, so there are no more moves
        return False
    if len(node.untried) == 0:         # every move already has a child, so there’s nothing left to add
        return False
    if node.depth >= max_depth:        # tree is already as tall as allowed
        return False
    return True


def make_child(node, col):
    """Create the child node for playing column `col` from `node`."""
    new_board = copy.deepcopy(node.board)       # copy the parent’s board, so the parent’s position stays unchanged
    row = drop(new_board, col, node.to_move)    # play the move on the copy
    # create the Node. It’s now the other player’s turn, its parent is node, it remembers which column was played, and it’s one level deeper.
    child = Node(new_board,                     
                 other(node.to_move),          
                 parent=node,
                 move=col,
                 depth=node.depth + 1)
    if is_win(new_board, row, col, node.to_move):   # did this move win?
        child.winner = node.to_move
        child.untried = []                      # game over: no more moves
    return child


def expand(node, x, max_depth):
    """add up to x new children to `node`. Returns the nodes to run playouts from."""
    if not can_expand(node, max_depth):
        return [node]                           # can't grow: simulate from node itself

    how_many = min(x, len(node.untried))        # can't add more than are left
    new_children = []
    for i in range(how_many):
        index = random.randrange(len(node.untried))
        col = node.untried.pop(index)           # take a random untried move
        child = make_child(node, col)
        node.children.append(child)             # attach it to the tree
        new_children.append(child)
    return new_children
  
# ---- 3. simulate stage ----------------  
def simulate(node):
    if node.winner is not None:
        return node.winner
    return random_playout(node.board, node.to_move)

# ---- 4. back-propagate stage -------------  
def back_propagate(node, winner):
    while node is not None:
        mover = other(node.to_move)
        node.N += 1
        if winner is None:
            node.U += 0.5
        elif winner == mover:
            node.U += 1
        node = node.parent
        
# ---- Main function - Monte Carlo Tree Search Algorithm -------------
def one_cycle(root, x, max_depth, C, w):
    """Do the 4 MCTS steps once."""
    leaf = select(root, C, w)                       # 1. SELECT
    new_nodes = expand(leaf, x, max_depth)          # 2. EXPAND
    for node in new_nodes:
        winner = simulate(node)                     # 3. SIMULATE
        back_propagate(node, winner)                # 4. BACK-PROPAGATE


def most_visited_child(root):
    """The root's child with the most playouts (highest N)."""
    best = None
    for child in root.children:
        if best is None or child.N > best.N:
            best = child
    return best


def mcts(board, player, cycles=500, x=1, max_depth=42, C=1.4, w=0.5):
    """Return the best column for `player` to play on `board`."""
    root = Node(board, player)                      # the tree starts with one node
    for i in range(cycles):
        one_cycle(root, x, max_depth, C, w)         # grow the tree a little
    best = most_visited_child(root)
    return best.move                                # the column to play