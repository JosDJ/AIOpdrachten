"""

Othello is a turn-based two-player strategy board game.

-----------------------------------------------------------------------------
Board representation

We represent the board as a flat-list of 100 elements, which includes each square on
the board as well as the outside edge. Each consecutive sublist of ten
elements represents a single row, and each list element stores a piece. 
An initial board contains four pieces in the center:

    ? ? ? ? ? ? ? ? ? ?
    ? . . . . . . . . ?
    ? . . . . . . . . ?
    ? . . . . . . . . ?
    ? . . . o @ . . . ?
    ? . . . @ o . . . ?
    ? . . . . . . . . ?
    ? . . . . . . . . ?
    ? . . . . . . . . ?
    ? ? ? ? ? ? ? ? ? ?

The outside edge is marked ?, empty squares are ., black is @, and white is o.

This representation has two useful properties:

1. Square (m,n) can be accessed as `board[mn]`, and m,n means m*10 + n. This avoids conversion
   between square locations and list indexes.
2. Operations involving bounds checking are slightly simpler.
"""
import random
import time
# The black and white pieces represent the two players.
EMPTY, BLACK, WHITE, OUTER = '.', '@', 'o', '?'
PIECES = (EMPTY, BLACK, WHITE, OUTER)
PLAYERS = {BLACK: 'Black', WHITE: 'White'}

# To refer to neighbor squares we can add a direction to a square.
UP, DOWN, LEFT, RIGHT = -10, 10, -1, 1
UP_RIGHT, DOWN_RIGHT, DOWN_LEFT, UP_LEFT = -9, 11, 9, -11
# in total 8 directions.
DIRECTIONS = (UP, UP_RIGHT, RIGHT, DOWN_RIGHT, DOWN, DOWN_LEFT, LEFT, UP_LEFT)

HEURISTIC_VALUES = [
    "?","?","?","?","?","?","?","?","?","?",
    "?",100, -20, 10, 5, 5, 10, -20, 100,"?",
    "?",-20, -50, -2, -2, -2, -2, -50, -20,"?",
    "?",10, -2, -1, -1, -1, -1, -2, 10,"?",
    "?",5, -2, -1, -1, -1, -1, -2, 5,"?",
    "?",5, -2, -1, -1, -1, -1, -2, 5,"?",
    "?",10, -2, -1, -1, -1, -1, -2, 10,"?",
    "?",-20, -50, -2, -2, -2, -2, -50, -20,"?",
    "?",100, -20, 10, 5, 5, 10, -20, 100,"?",
    "?","?","?","?","?","?","?","?","?","?"
]


def squares():
    # list all the valid squares on the board.
    # returns a list of valid integers [11, 12, ...]; e.g. 19,20,21 are invalid
    # 11 means first row, first col, because the board size is 10x10
    return [i for i in range(11, 89) if 1 <= (i % 10) <= 8]


def initial_board():
    # create a new board with the initial black and white positions filled
    # returns a list ['?', '?', '?', ..., '?', '?', '?', '.', '.', '.', ...]
    board = [OUTER] * 100
    for i in squares():
        board[i] = EMPTY
    # the middle four squares should hold the initial piece positions.
    board[44], board[45] = WHITE, BLACK
    board[54], board[55] = BLACK, WHITE
    return board


def print_board(board):
    # get a string representation of the board
    # heading '  1 2 3 4 5 6 7 8\n'
    rep = ''
    rep += '  %s\n' % ' '.join(map(str, range(1, 9)))
    # begin,end = 11,19 21,29 31,39 ..
    for row in range(1, 9):
        begin, end = 10 * row + 1, 10 * row + 9
        rep += '%d %s\n' % (row, ' '.join(board[begin:end]))
    return rep


# -----------------------------------------------------------------------------
# Playing the game

# We need functions to get moves from players, check to make sure that the moves
# are legal, apply the moves to the board, and detect when the game is over.

# Checking moves. A move must be both valid and legal: it must refer to a real square,
# and it must form a bracket with another piece of the same color with pieces of the
# opposite color in between.

def is_valid(move):
    # is move a square on the board?
    # move must be an int, and must refer to a real square
    return isinstance(move, int) and move in squares()


def opponent(player):
    # get player's opponent piece
    return BLACK if player is WHITE else WHITE


def find_bracket(square, player, board, direction):
    # find and return the square that forms a bracket with square for player in the given
    # direction; returns None if no such square exists
    bracket = square + direction
    if board[bracket] == player:
        return None
    opp = opponent(player)
    while board[bracket] == opp:
        bracket += direction
    # if last square board[bracket] not in (EMPTY, OUTER, opp) then it is player
    return None if board[bracket] in (OUTER, EMPTY) else bracket


def is_legal(move, player, board):
    # is this a legal move for the player?
    # move must be an empty square and there has to be a bracket in some direction
    # note: any(iterable) will return True if any element of the iterable is true
    hasbracket = lambda direction: find_bracket(move, player, board, direction)
    return board[move] == EMPTY and any(hasbracket(x) for x in DIRECTIONS)


def make_move(move, player, board):
    # when the player makes a valid move, we need to update the board and flip all the
    # bracketed pieces.
    board[move] = player
    # look for a bracket in any direction
    for d in DIRECTIONS:
        make_flips(move, player, board, d)
    return board


def make_flips(move, player, board, direction):
    # flip pieces in the given direction as a result of the move by player
    bracket = find_bracket(move, player, board, direction)
    if not bracket:
        return
    # found a bracket in this direction
    square = move + direction
    while square != bracket:
        board[square] = player
        square += direction


# Monitoring players

# define an exception
class IllegalMoveError(Exception):
    def __init__(self, player, move, board):
        self.player = player
        self.move = move
        self.board = board

    def __str__(self):
        return '%s cannot move to square %d' % (PLAYERS[self.player], self.move)


def legal_moves(player, board):
    # get a list of all legal moves for player
    # legal means: move must be an empty square and there has to be is an occupied line in some direction
    return [sq for sq in squares() if is_legal(sq, player, board)]


def any_legal_move(player, board):
    # can player make any moves?
    return any(is_legal(sq, player, board) for sq in squares())


# Putting it all together. Each round consists of:
# - Get a move from the current player.
# - Apply it to the board.
# - Switch players. If the game is over, get the final score.

def play(black_strategy, white_strategy):
    # play a game of Othello and return the final board and score

    board = initial_board()
    turn = random.choice((WHITE, BLACK))
    while any_legal_move(turn, board):
        t0 = time.process_time()
        print(print_board(board))
        if turn == WHITE:
            move = get_move(white_strategy, turn, board)
            make_move(move, turn, board)# do move according to strategy
            turn = next_player(board, turn)  # switch turn
        else:
            move = get_move(black_strategy, turn, board)  # see above
            make_move(move, turn, board)
            turn = next_player(board, turn)
        t1= time.process_time()
        print("Time spent searching move: ", t1-t0)

    black_score = score(BLACK, board)
    white_score = score(WHITE, board)
    print("Black score: ", black_score, " | White score: ", white_score)
    print("Black won") if black_score>white_score else print("White won")
    print("Final boardstate:")
    print(print_board(board))  # print endgame


def next_player(board, prev_player):
    # which player should move next?  Returns None if no legal moves exist
    if prev_player == WHITE and any_legal_move(BLACK, board):
        return BLACK
    elif any_legal_move(WHITE, board):
        return WHITE
    else:
        return None


def get_move(strategy, player, board):
    # call strategy(player, board) to get a move
    if strategy == minimax:
        MAX = WHITE if player == WHITE else BLACK
        return strategy(player, board, 5, MAX, -9999, 9999)
    else:
        return strategy(player, board)


def score(player, board):
    # compute player's score (number of player's pieces minus opponent's)
    return board.count(player)


def get_heuristic_value(location):
    return HEURISTIC_VALUES[location]

# Play strategies
# 2A
def random_move(player, board):
    if any_legal_move(player, board):
        move = random.choice(legal_moves(player, board))
        if is_valid(move):
            make_move(move, player, board)
            return move
        else:
            return None


# 2B
def minimax(player, board, depth, MAX, alpha, beta):
    if depth == 0 or not any_legal_move(player, board):
        return score(player, board)
    action = None
    best_value = -9999 if player == MAX else 9999
    for move in legal_moves(player, board):
        copy = board[:]
        new_state = make_move(move,player,copy)
        eval_state = minimax(opponent(player), new_state, depth-1, MAX, alpha, beta)

        if player == MAX and best_value < eval_state:
            best_value = eval_state + get_heuristic_value(move)
            action = move
            alpha = max(alpha, best_value)
            if beta <= alpha:
                break
        elif player != MAX and best_value > eval_state:
            best_value = eval_state + get_heuristic_value(move)
            action = move
            beta = min(beta, best_value)
            if beta <= alpha:
                break
    return action


# play(random_move, random_move)

play(minimax, minimax)
# 2C
# TELLEN VAN STENEN IS NIET GOED OMDAT DE LOCATIES OP HET BORD OOK EEN WAARDE HEBBEN, HOEKPUNTEN ZIJN BIJVOORBEELD ERG
# BELANGRIJK

# EVALUATIE FUNCTIE IS EEN VALUE VAN HET BORD ERBIJ GEVEN

# 2D Wanneer de eis is dat een zet binnen twee seconden moet worden gedaan, tot welke diepte kun je dan
# gaan met Minimax? >>> gaat iets nog niet helemaal ok dus vrij diep
#

# 2E zie code

# 2F Wat is de maximale diepte waarbij het programma nog een acceptabele performance heeft? Op welke
# manieren zou je de performance nog verder kunnen verbeteren?
# betere code :),
