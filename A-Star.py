import copy
import random
import heapq

ROWS = 2
COLS = 5

GOAL_STATE = [
    [1, 2, 3, 4, 5],
    [6, 7, 8, 0, 0]
]

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def print_puzzle(state):
    for row in state:
        print(' '.join(str(x) if x != 0 else '_' for x in row))
    print()

def state_to_tuple(state):
    return tuple(tuple(row) for row in state)

def find_blank_positions(state):
    return [(i, j) for i in range(ROWS) for j in range(COLS) if state[i][j] == 0]

def move(state, tile_pos, blank_pos):
    new_state = copy.deepcopy(state)
    ti, tj = tile_pos
    bi, bj = blank_pos
    new_state[bi][bj], new_state[ti][tj] = new_state[ti][tj], new_state[bi][bj]
    return new_state

def get_next_states(state):
    next_states = []
    blanks = find_blank_positions(state)

    for bi, bj in blanks:
        for di, dj in DIRECTIONS:
            ni, nj = bi + di, bj + dj
            if 0 <= ni < ROWS and 0 <= nj < COLS and state[ni][nj] != 0:
                new_state = move(state, (ni, nj), (bi, bj))
                next_states.append(new_state)
    return next_states

def generate_random_puzzle():
    tiles = list(range(1, 9)) + [0, 0]
    random.shuffle(tiles)
    return [tiles[:5], tiles[5:]]

def is_goal(state):
    return state == GOAL_STATE

def find_goal_position(value):
    for i in range(ROWS):
        for j in range(COLS):
            if GOAL_STATE[i][j] == value:
                return (i, j)
    return None

# 맨해튼 거리 휴리스틱
def heuristic(state):
    dist = 0
    for i in range(ROWS):
        for j in range(COLS):
            val = state[i][j]
            if val != 0:
                gi, gj = find_goal_position(val)
                dist += abs(i - gi) + abs(j - gj)
    return dist

# A* 알고리즘
def a_star(start_state):
    open_list = []
    heapq.heappush(open_list, (heuristic(start_state), 0, start_state))
    visited = set()
    parent = {state_to_tuple(start_state): None}
    g_score = {state_to_tuple(start_state): 0}

    while open_list:
        f, g, current = heapq.heappop(open_list)

        if is_goal(current):
            print("목표 상태에 도달했습니다!")
            return reconstruct_path(current, parent)

        key = state_to_tuple(current)
        if key in visited:
            continue
        visited.add(key)

        for next_state in get_next_states(current):
            next_key = state_to_tuple(next_state)
            tentative_g = g + 1

            if next_key not in g_score or tentative_g < g_score[next_key]:
                g_score[next_key] = tentative_g
                f_score = tentative_g + heuristic(next_state)
                heapq.heappush(open_list, (f_score, tentative_g, next_state))
                parent[next_key] = current

    print("해결할 수 없는 퍼즐입니다.")
    return None

def reconstruct_path(end_state, parent):
    path = []
    current = end_state
    while current is not None:
        path.append(current)
        current = parent[state_to_tuple(current)]
    path.reverse()
    return path

# 실행 예제
start = generate_random_puzzle()
print("시작 상태:")
print_puzzle(start)

solution = a_star(start)

if solution:
    print(f"\n총 이동 횟수: {len(solution) - 1}")
    for idx, step in enumerate(solution):
        print(f"Step {idx}:")
        print_puzzle(step)