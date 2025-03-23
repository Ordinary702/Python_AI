import copy
import random
from collections import deque

# 퍼즐 크기
ROWS = 2
COLS = 5

# 목표 상태
GOAL_STATE = [
    [1, 2, 3, 4, 5],
    [6, 7, 8, 0, 0]
]

# 방향: 상, 하, 좌, 우
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def print_puzzle(state):
    for row in state:
        print(' '.join(str(x) if x != 0 else '_' for x in row))
    print()

def state_to_tuple(state):
    return tuple(tuple(row) for row in state)

def find_blank_positions(state):
    positions = []
    for i in range(ROWS):
        for j in range(COLS):
            if state[i][j] == 0:
                positions.append((i, j))
    return positions

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

# BFS 구현
def bfs(start_state):
    visited = set()
    queue = deque()
    parent = dict()

    state_key = state_to_tuple(start_state)
    queue.append(start_state)
    visited.add(state_key)
    parent[state_key] = None

    while queue:
        current = queue.popleft()

        if is_goal(current):
            print("목표 상태에 도달했습니다!")
            return reconstruct_path(current, parent)

        for next_state in get_next_states(current):
            key = state_to_tuple(next_state)
            if key not in visited:
                visited.add(key)
                queue.append(next_state)
                parent[key] = current

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

solution = bfs(start)

if solution:
    print(f"\n총 이동 횟수: {len(solution) - 1}")
    for idx, step in enumerate(solution):
        print(f"Step {idx}:")
        print_puzzle(step)