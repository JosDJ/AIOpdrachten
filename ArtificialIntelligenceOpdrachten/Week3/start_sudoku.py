import time


#   1 2 3 4 .. 9
# A
# B
# C
# D
# ..
# I

def cross(A, B):
    # concat of chars in string A and chars in string B
    return [a + b for a in A for b in B]


digits = '123456789'
rows = 'ABCDEFGHI'
cols = digits
cells = cross(rows, cols)  # 81 cells A1..9, B1..9, C1..9, ...

# unit = a row, a column, a box; list of all units
unit_list = ([cross(r, cols) for r in rows] +  # 9 rows
             [cross(rows, c) for c in cols] +  # 9 cols
             [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')])  # 9 units

units = dict((s, [u for u in unit_list if s in u]) for s in cells)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in cells)


def test():
    # a set of tests that must pass
    assert len(cells) == 81
    assert len(unit_list) == 27
    assert all(len(units[s]) == 3 for s in cells)
    assert all(len(peers[s]) == 20 for s in cells)
    assert units['C2'] == [['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2'],
                           ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'],
                           ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']]
    assert peers['C2'] == set(['A2', 'B2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2',
                               'C1', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9',
                               'A1', 'A3', 'B1', 'B3'])
    print('All tests pass.')


def display(grid):
    # grid is a dict of {cell: string}, e.g. grid['A1'] = '1234'
    print()
    for r in rows:
        for c in cols:
            v = grid[r + c]
            # avoid the '123456789'
            if v == '123456789':
                v = '.'
            print(''.join(v), end=' ')
            if c == '3' or c == '6': print('|', end='')
        print()
        if r == 'C' or r == 'F':
            print('-------------------')
    print()


def parse_string_to_dict(grid_string):
    # grid_string is a string like '4.....8.5.3..........7......2.....6....   '
    # convert grid_string into a dict of {cell: chars}
    char_list1 = [c for c in grid_string if c in digits or c == '.']
    # char_list1 = ['8', '5', '.', '.', '.', '2', '4', ...  ]

    assert len(char_list1) == 81

    # replace '.' with '1234567'
    char_list2 = [s.replace('.', '123456789') for s in char_list1]

    # grid {'A1': '8', 'A2': '5', 'A3': '123456789',  }
    return dict(zip(cells, char_list2))


def no_conflict(grid, cell, val):
    # check if assignment is possible: value v not a value of a peer
    for peer in peers[cell]:
        if grid[peer] == val:
            return False  # conflict
    return True  # no conflict


def solve(grid):
    # backtracking search for a solution (DFS)
    # your code here
    # check if all cells have 1
    cells_filled = []
    for cell in grid:
        if int(grid[cell]) < 10:
            cells_filled.append(True)
        else:
            cells_filled.append(False)
    if all(cells_filled):
        print("Sudoku solved")
        print(grid)
        return True
    else:
        # find next key with no valid value
        next_key = None
        copy_value = None
        for key, value in grid.items():
            if int(value) > 9:
                next_key = key
                copy_value = value[:]
                break
        for new_value in range(1, 10):
            if no_conflict(grid, next_key, str(new_value)):
                grid[next_key] = str(new_value)
                if solve(grid):
                    return True
                else:
                    grid[next_key] = copy_value
                    continue
        return False


def solve_with_arc_consistency(grid):
    cells_filled = []
    for cell in grid:
        if int(grid[cell]) < 10:
            cells_filled.append(True)
        else:
            cells_filled.append(False)
    if all(cells_filled):
        print("Sudoku solved")
        display(grid)
        return True
    else:
        for cell in grid:
            #print(cell)
            if int(grid[cell]) > 9:
                possible_values = list(grid[cell])
                #print(possible_values)
                for v in possible_values:
                    #print(v)
                    if no_conflict(grid, cell, v):
                        grid_copy = grid.copy()
                        grid_copy[cell] = v
                        #print("No conflict")
                        if make_arc_consistent(grid_copy,cell,v):
                            if solve_with_arc_consistency(grid_copy):
                                return True
                    else:
                        continue
                return False


def make_arc_consistent(grid, cell, value):
    grid_copy = grid.copy()

    for peer in peers[cell]:
        if value in grid[peer]:
            if len(grid[peer]) <= 1:  # if peer has <= 1 value
                return False
            else:
                #   print("replace value" , value, " in peer")
                grid[peer] = grid[peer].replace(value, "")


    if grid != grid_copy:   # if peer is value verwisseld met lege string

        cells_with_one_solution = []  # lijst met cellen die maar 1 oplossing hebben
        for c in grid:
            if len(grid[c]) == 1:
                if c != cell:
                    cells_with_one_solution.append((c, grid[c])) # dit zijn cellen met 1 oplossing (dus opgeloste cellen)
        cells_bool = []
        for v in cells_with_one_solution:
            cell_bool = make_arc_consistent(grid, v[0], v[1])
            cells_bool.append(cell_bool)
        if not all(cells_bool):
            return False

    return True


# minimum nr of clues for a unique solution is 17
slist = [None for x in range(20)]
slist[0] = '.56.1.3....16....589...7..4.8.1.45..2.......1..42.5.9.1..4...899....16....3.6.41.'
slist[1] = '.6.2.58...1....7..9...7..4..73.4..5....5..2.8.5.6.3....9.73....1.......93......2.'
slist[2] = '.....9.73.2.....569..16.2.........3.....1.56..9....7...6.34....7.3.2....5..6...1.'
slist[3] = '..1.3....5.917....8....57....3.1.....8..6.59..2.9..8.........2......6...315.9...8'
slist[4] = '....6.8748.....6.3.....5.....3.4.2..5.2........72...35.....3..........69....96487'
slist[5] = '.94....5..5...7.6.........71.2.6.........2.19.6...84..98.......51..9..78......5..'
slist[6] = '.5...98..7...6..21..2...6..............4.598.461....5.54.....9.1....87...2..5....'
slist[7] = '...17.69..4....5.........14.....1.....3.5716..9.....353.54.9....6.3....8..4......'
slist[8] = '..6.4.5.......2.3.23.5..8765.3.........8.1.6.......7.1........5.6..3......76...8.'
slist[9] = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
slist[10] = '85...24..72......9..4.........1.7..23.5...9...4...........8..7..17..........36.4.'
slist[11] = '...5....2...3..85997...83..53...9...19.73...4...84...1.471..6...5...41...1...6247'
slist[12] = '.....6....59.....82....8....45........3........6..3.54...325..6..................'
slist[13] = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
slist[14] = '8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4..'
slist[15] = '6..3.2....5.....1..........7.26............543.........8.15........4.2........7..'
slist[16] = '.6.5.1.9.1...9..539....7....4.8...7.......5.8.817.5.3.....5.2............76..8...'
slist[17] = '..5...987.4..5...1..7......2...48....9.1.....6..2.....3..6..2.......9.7.......5..'
slist[18] = '3.6.7...........518.........1.4.5...7.....6.....2......2.....4.....8.3.....5.....'
slist[19] = '1.....3.8.7.4..............2.3.1...........958.........5.6...7.....8.2...4.......'

for i, sudo in enumerate(slist):
    print('*** sudoku {0} ***'.format(i))

    d = parse_string_to_dict(sudo)
    display(d)
    start_time = time.time()
    #solve(d)
    solve_with_arc_consistency(d)
    end_time = time.time()
    hours, rem = divmod(end_time - start_time, 3600)
    minutes, seconds = divmod(rem, 60)
    print("duration [hh:mm:ss.ddd]: {:0>2}:{:0>2}:{:06.3f}".format(int(hours), int(minutes), seconds))
    print()

# board = '.56.1.3....16....589...7..4.8.1.45..2.......1..42.5.9.1..4...899....16....3.6.41.'
# d = parse_string_to_dict(board)
# display(d)
# solve_with_arc_consistency(d)
# display(d)
# d2 = parse_string_to_dict(board)
# solve(d)
# display(d)


