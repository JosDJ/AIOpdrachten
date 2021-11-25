import random
import string
board = []

with open('words_NL.txt', 'r') as f:
    lines = [line.rstrip() for line in f.readlines()]
    f.close()


prefixes = []
for word in lines:
    prefix = ""
    for char in word:
        prefix += char
        prefixes.append(prefix)
prefixes_list = list(dict.fromkeys(prefixes))
print(prefixes_list)


def create_board(n):
    for i in range(n):
        row = ''.join(random.choices(string.ascii_lowercase, k=n))
        board.append(row)

def print_board():
    for row in board:
        print(row)


def find_all_words(col,row, prefix):
    if prefix not in prefixes_list:
        return
    if prefix in lines:
        print(prefix)
        return

    col_min = col-1 if col > 0 else len(board)-1
    col_plus = col+1 if col < len(board)-1 else 0
    row_min = row-1 if row > 0 else len(board)-1
    row_plus = row+1 if row < len(board)-1 else 0

    #check left
    find_all_words(row, col_min, prefix + board[row][col_min])
    #check right
    find_all_words(row, col_plus, prefix + board[row][col_plus])
    #check top
    find_all_words(row_min, col, prefix + board[row_min][col])
    # check bottom
    find_all_words(row_plus, col, prefix + board[row_plus][col])

create_board(10)
print_board()

for row in range(len(board)):
    for col in range(len(board[row])):
        find_all_words(row, col, board[row][col])
