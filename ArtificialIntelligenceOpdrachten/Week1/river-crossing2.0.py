start_state = "WCGF|"
characters = ["F","C","G","W"]


def is_goal_state(state):
    state = state.split("|")
    if state[0] == '':
        return True
    else:
        return False


def return_successor_state(state):
    successor_states = []
    temp_state = state.split("|")
    for riverside in temp_state:
        if "F" in riverside:
            for char in characters:
                if riverside == temp_state[0] and move_right(state,char) is not None:
                    if is_legal_state(move_right(state,char)):
                        successor_states.append(move_right(state, char))
                elif riverside == temp_state[1] and move_left(state,char) is not None:
                    if is_legal_state(move_left(state, char)):
                        successor_states.append(move_left(state, char))
    return successor_states


def is_legal_state(state):
    if state == "":
        return False
    else:
        state = state.split("|")
        left = state[0]
        right = state[1]

        if "W" in left and "G" in left and "F" not in left:
            return False
        elif "G" in left and "C" in left and "F" not in left:
            return False

        if "W" in right and "G" in right and "F" not in right:
            return False
        elif "G" in right and "C" in right and "F" not in right:
            return False
        else:
            return True


def move_left(state, char):
    state = state.split("|")
    new_state = ""
    if char == "F":
        state[0] = state[0] + "F"
        sorted_0 = sorted(state[0])
        state[0] = "".join(sorted_0)
        state[0] = state[0] + "|"
        state[1] = state[1].replace("F", "")
        sorted_1 = sorted(state[1])
        state[1] = "".join(sorted_1)
        for riverside in state:
            new_state += riverside
        return new_state
    elif char in state[1]:
        state[1] = state[1].replace("F", "")
        state[1] = state[1].replace(char, "")
        sorted_1 = sorted(state[1])
        state[1] = "".join(sorted_1)
        state[0] = state[0] + char + "F"
        sorted_0 = sorted(state[0])
        state[0] = "".join(sorted_0)
        state[0] = state[0] + "|"
        for riverside in state:
            new_state += riverside
    return new_state


def move_right(state, char):
    new_state = ""
    state = state.split("|")
    if char == "F":
        # return None als de farmer alleen naar rechts wilt
        return
    elif char in state[0]:
        state[0] = state[0].replace(char, "")
        state[0] = state[0].replace("F", "")
        sorted_0 = sorted(state[0])
        state[0] = "".join(sorted_0)
        state[1] = state[1] + char + "F"
        sorted_1 = sorted(state[1])
        state[1] = "".join(sorted_1)
        state[0] = state[0] + "|"
        for riverside in state:
            new_state += riverside
    return new_state


def find_all_paths(state, path):
    path = path + [state]
    if is_goal_state(state[0]):
        return [path]
    paths = []  # list of paths

    for child in return_successor_state(state):
        if child not in path:
            newpaths = find_all_paths(child, path)
            for newpath in newpaths:
                paths.append(newpath)

    return paths


print(find_all_paths(start_state, []))
