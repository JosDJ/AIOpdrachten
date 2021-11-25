start_state = ["CFGW", ""]
legal_states = ["CFGW", "G", "CFW", "FG", "CW", ""]




characters = ["W", "G", "C"]

# check if goal state is reached
def is_goal_state(left_bank):
    if left_bank == "":
        return True
    else:
        return False

def sort_state(state):
    i = 0
    for riverside_state in state:
        sorted_characters = sorted(riverside_state)
        riverside_state = "".join(sorted_characters)
        state[i] = riverside_state
        i = i+1

    return state

# Function that checks if state is valid
def is_valid_state(state):
    # sort state alphabetically and check if that state is a legal state
    for riverside_state in state:
        sorted_characters = sorted(riverside_state)
        riverside_state = "".join(sorted_characters)
        if riverside_state in legal_states:
            return True
    return False


def print_solution(path):
    print(path)


# Function that returns all possible states following the current state
def return_succesor_state(current_state, path):
    sort_state(current_state)
    succesor_states = []
    left = current_state[0]
    right = current_state[1]

    if "F" in left:
        left = left.replace('F', '')
        right = right + "F"
        current_state = [left, right]
    elif "F" in right:
        right = right.replace("F","")
        left = left + "F"
        current_state = [left, right]

    if is_valid_state(current_state) and current_state not in path:
        succesor_states.append(current_state)

    else:
        for char in characters:
            move_char(char, current_state)
            if is_valid_state(current_state):
                succesor_states.append(current_state)
            else:
                move_char(char, current_state)

    return succesor_states


# Function that moves a character to the other side based on its position
def move_char(char, state):
    # keep index to know at what side of river we are
    index = 0
    # check all riversides on whether or not a character is present and change the characters riverside
    for riverside in state:
        if char in riverside:
            state[index] = state[index].replace(char, "")
            index = index + 1
        elif char not in riverside:
            state[index] = state[index] + char
            index = index + 1


# depth first search algorithm
def find_all_paths(state, path):
    path = path + [state]
    print(path)
    if is_goal_state(state[0]):
        for step in path:
            print(step)
        print("Game finished")
        return

    paths = []  # list of paths

    for child in return_succesor_state(state, path):
        if child not in path:
            newpaths = find_all_paths(child, path)
            for newpath in newpaths:
                paths.append(newpath)


find_all_paths(start_state, [])
