import random
import string

board = [
    ["p", "i", "e", "t"],
    ["g", "a", "a", "t"],
    ["a", "t", "m", "s"],
    ["h", "u", "i", "s"]
]

with open('words_NL.txt', 'r') as f:
    lines = [line.rstrip() for line in f.readlines()]
    f.close()

prefixes = set()
for word in lines:
    prefix = ""
    for char in word:
        prefix += char
        prefixes.add(prefix)


def create_board(n):
    for i in range(n):
        row = ''.join(random.choices(string.ascii_lowercase, k=n))
        board.append(row)


def print_board():
    for row in board:
        print(row)


def get_char_at_XY(x, y):
    return board[x][y]


def successor_states(node, path):
    successor_states = []
    x = node[0]
    y = node[1]

    x_min = x - 1 if x > 0 else len(board) - 1
    x_plus = x + 1 if x < len(board) - 1 else 0
    y_min = y - 1 if y > 0 else len(board) - 1
    y_plus = y + 1 if y < len(board) - 1 else 0

    word = ""
    for node in path:
        word += get_char_at_XY(node[0], node[1])

    successor_state = word + get_char_at_XY(x_min, y)
    if successor_state in prefixes:
        successor_states.append([x_min, y])

    successor_state = word + get_char_at_XY(x_plus, y)
    if successor_state in prefixes:
        successor_states.append([x_plus, y])

    successor_state = word + get_char_at_XY(x, y_min)
    if successor_state in prefixes:
        successor_states.append([x, y_min])

    successor_state = word + get_char_at_XY(x, y_plus)
    if successor_state in prefixes:
        successor_states.append([x, y_plus])

    return successor_states


def find_all_words(node, path):
    path = path + [node]

    word = ""
    for node in path:
        word += get_char_at_XY(node[0], node[1])

    if word in lines:
        print("Gevonden woord: ", word)

    paths = []
    for child in successor_states(node, path):
        if child not in path:
            newpaths = find_all_words(child, path)
            for newpath in newpaths:
                paths.append(newpath)
    return paths



print_board()

for y in range(len(board)):
    for x in range(len(board[y])):
        print(find_all_words([x, y], []))


# eerste "" eruit halen
