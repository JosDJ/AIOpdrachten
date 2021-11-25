'''Constraints:
    1 every Ace borders a King
    2 every King borders a Queen
    3 every Queen borders a Jack
    4 no Ace borders a Queen
    5 no two of the same cards border each other

'''
import itertools
import time

# the board has 8 cells, let’s represent the board with a dict key=cell, value=card
start_board = {cell: '.' for cell in range(8)}
cards = ['K', 'K', 'Q', 'Q', 'J', 'J', 'A', 'A']
neighbors = {0: [3], 1: [2], 2: [1, 4, 3], 3: [0, 2, 5], 4: [2, 5], 5: [3, 4, 6, 7], 6: [5], 7: [5]}


def is_valid(board):
    valid_cells_in_board = []
    for cell in board:
        n_chars = []
        for neighbor in neighbors[cell]:
            n_chars.append(board[neighbor])
        if len(set(n_chars)) == 1 and n_chars[0] == "." and board[cell] != '.':
            valid_cells_in_board.append(True)
        else:
            if board[cell] == "A":
                check = True if "K" in n_chars and "A" not in n_chars and "Q" not in n_chars \
                    else False
                if not check:
                    if "." in n_chars:
                        check = True
                valid_cells_in_board.append(check)
                if not check:
                    break
            elif board[cell] == "K":
                check = True if "Q" in n_chars and "K" not in n_chars else False
                valid_cells_in_board.append(check)
                if not check:
                    break
            elif board[cell] == "Q":
                check = True if "J" in n_chars and "Q" not in n_chars else False
                valid_cells_in_board.append(check)
                if not check:
                    break
            elif board[cell] == "J":
                check = False if "J" in n_chars else True
                valid_cells_in_board.append(check)
                if not check:
                    break
    return all(valid_cells_in_board)


def brute_force():
    # er zijn 8! = 40320 permutaties (8*7*6*5*4*3*2*1)
    x = itertools.permutations(cards)
    perms = 0
    for permutation in list(x):
        perms += 1
        y = is_valid({0: permutation[0], 1: permutation[1], 2: permutation[2], 3: permutation[3], 4: permutation[4],
                      5: permutation[5], 6: permutation[6], 7: permutation[7]})
        if y:
            print("Aantal permutaties geprobeerd: ", perms, " | Board ziet er zo uit: ", permutation)


def backtracking_search(board):
    # check if board is valid
    if is_valid(board):
        # check if board is filled
        if '.' not in board.values():
            print("Oplossing gevonden: ", board.values())
            return True
        # board not filled so we need to find the next empty in dict
        else:
            # select next key in dict that has no value
            next_key = None
            for key, value in board.items():
                if value == ".":
                    next_key = key
                    break
            for card in cards:
                if sum(value == card for value in board.values()) >= 2:
                    continue
                else:
                    board[next_key] = card
                    if backtracking_search(board):
                        return True
                    else:
                        board[next_key] = "."
            return False


def test():
    # # is_valid(board) checks all cards, returns False if any card is invalid
    print('f ', is_valid({0: 'J', 1: 'K', 2: 'Q', 3: 'Q', 4: 'J', 5: 'K', 6: 'A', 7: 'A'}))  # 1
    print('f ', is_valid({0: 'J', 1: 'J', 2: 'Q', 3: 'Q', 4: 'K', 5: 'K', 6: 'A', 7: 'A'}))  # 2
    print('t ', is_valid({0: '.', 1: '.', 2: '.', 3: '.', 4: '.', 5: '.', 6: '.', 7: '.'}))  # 3
    print('t ', is_valid({0: 'J', 1: '.', 2: '.', 3: '.', 4: '.', 5: '.', 6: '.', 7: '.'}))  # 4
    print('f ', is_valid({0: '.', 1: '.', 2: '.', 3: 'J', 4: 'J', 5: 'A', 6: 'J', 7: 'J'}))  # [1]    #5
    print('f ', is_valid({0: 'J', 1: '.', 2: '.', 3: '.', 4: 'J', 5: 'K', 6: 'J', 7: 'Q'}))  # [3]    #6
    print('t ', is_valid({0: '.', 1: 'Q', 2: '.', 3: '.', 4: 'Q', 5: 'J', 6: '.', 7: '.'}))  # [3]    #7
    print('f ', is_valid({0: 'Q', 1: '.', 2: '.', 3: 'K', 4: '.', 5: '.', 6: '.', 7: '.'}))  # [3]    #8
    print('f ', is_valid({0: '.', 1: 'A', 2: 'Q', 3: '.', 4: '.', 5: 'Q', 6: '.', 7: '.'}))  # [4]    #9
    print('f ', is_valid({0: '.', 1: '.', 2: '.', 3: '.', 4: 'J', 5: 'J', 6: '.', 7: '.'}))  # [5]    #10
    print('f ', is_valid({0: '.', 1: '.', 2: '.', 3: '.', 4: '.', 5: 'Q', 6: '.', 7: 'Q'}))  # [5]    #11
    print('t ', is_valid({0: 'Q', 1: 'Q', 2: '.', 3: '.', 4: '.', 5: '.', 6: '.', 7: '.'}))  # 12
    print(is_valid({0: 'K', 1: 'Q', 2: 'J', 3: 'Q', 4: 'A', 5: 'K', 6: 'A', 7: 'J'}))


t0 = time.process_time()
brute_force()
t1 = time.process_time()
print(t1 - t0)
print("---------------------------------------------------------------------------------------------------")
t0 = time.process_time()
backtracking_search(start_board)
t1 = time.process_time()
print(t1 - t0)
