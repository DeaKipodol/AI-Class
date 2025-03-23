import heapq

class State:
    def __init__(self, board, goal, depth=0, cost=0, parent=None, move=None):
        self.board = board
        self.goal = goal
        self.depth = depth
        self.cost = cost
        self.parent = parent  # 부모 상태 (경로 복원용)
        self.move = move      # 이 상태에 도달하기 위한 이동 ("Left", "Right", "Up", "Down")

    def get_state_to_operate(self, i1, i2, depth, move):
        new_board = self.board[:]
        new_board[i1], new_board[i2] = new_board[i2], new_board[i1]
        return State(new_board, self.goal, depth, self.cost + 1, parent=self, move=move)

    def expand(self, depth):
        result = []
        i = self.board.index(0)
        # Left: 왼쪽 열이 아니라면 (인덱스 % 5 != 0)
        if i % 5 != 0:
            result.append(self.get_state_to_operate(i, i - 1, depth, "Left"))
        # Up: 윗 행이 아니라면 (i >= 5)
        if i >= 5:
            result.append(self.get_state_to_operate(i, i - 5, depth, "Up"))
        # Down: 아랫 행이 아니라면 (i < 5; 2행 퍼즐이므로 위 행이면 아래로 이동 가능)
        if i < 5:
            result.append(self.get_state_to_operate(i, i + 5, depth, "Down"))
        # Right: 오른쪽 열이 아니라면 (인덱스 % 5 != 4)
        if i % 5 != 4:
            result.append(self.get_state_to_operate(i, i + 1, depth, "Right"))
        return result

    def __str__(self):
        return (str(self.board[:5]) + "\n" +
                str(self.board[5:]) + "\n" +
                "----------------------------" +
                f"\nCost: {self.cost}, Heuristic: {self.heuristic()}, Depth: {self.depth}, Move: {self.move}")

    def __eq__(self, other):
        return self.board == other.board

    def __lt__(self, other):
        return (self.cost + self.heuristic()) < (other.cost + other.heuristic())

    def heuristic(self):
        # 맨해튼 거리 휴리스틱
        distance = 0
        for i, val in enumerate(self.board):
            if val != 0:
                goal_index = self.goal.index(val)
                goal_row, goal_col = divmod(goal_index, 5)
                curr_row, curr_col = divmod(i, 5)
                distance += abs(goal_row - curr_row) + abs(goal_col - curr_col)
        return distance

def reconstruct_path(state):
    """목표 상태에서 부모 포인터를 따라 경로를 복원하는 함수"""
    path = []
    while state.parent is not None:
        path.append(state.move)
        state = state.parent
    path.reverse()
    return path

################# 초기 상태 설정 ########################
puzzle = [2, 1, 9, 4, 7, 0, 5, 3, 6, 8]
goal = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

open_queue = [State(puzzle, goal)]
closed_dict = {}  # 각 상태(튜플 형태)별로 최소 비용 기록

count = 1
solution_state = None

while open_queue:
    current = heapq.heappop(open_queue)
    
    print(f"Step {count}:")
    print(current)
    count += 1

    if current.board == goal:
        print("탐색 성공!")
        solution_state = current
        break

    board_tuple = tuple(current.board)
    # 이미 동일한 보드 구성으로 더 낮은 비용을 방문한 경우 스킵
    if board_tuple in closed_dict and closed_dict[board_tuple] <= current.cost:
        continue
    closed_dict[board_tuple] = current.cost

    for state in current.expand(current.depth + 1):
        board_tuple_next = tuple(state.board)
        if board_tuple_next in closed_dict and closed_dict[board_tuple_next] <= state.cost:
            continue
        heapq.heappush(open_queue, state)

if solution_state:
    path = reconstruct_path(solution_state)
    print("Solution path:", path)
    print("Total moves:", len(path))
else:
    print("탐색 실패")

'''

----------------------------
Cost: 16, Heuristic: 13, Depth: 16, Move: Down
Step 3398:
[0, 1, 2, 3, 4]
[5, 6, 7, 8, 9]
----------------------------
Cost: 29, Heuristic: 0, Depth: 29, Move: Up
탐색 성공!
Solution path: ['Right', 'Right', 'Right', 'Up', 'Right', 'Down', 'Left', 'Up', 'Left', 'Left', 'Down', 'Right', 'Up', 'Left', 'Left', 'Down', 'Right', 'Right', 'Right', 'Up', 'Right', 'Down', 'Left', 'Up', 'Left', 'Left', 'Down', 'Left', 'Up']
Total moves: 29
            '''