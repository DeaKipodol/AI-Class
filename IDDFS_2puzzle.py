class State:
    def __init__(self, board, goal, depth=0):
        self.board = board
        self.goal = goal
        self.depth = depth

    def get_state_to_operate(self, i1, i2, depth):
        new_board = self.board[:]
        new_board[i1], new_board[i2] = new_board[i2], new_board[i1]
        return State(new_board, self.goal, depth)

    def expand(self, depth):
        result = []
        i = self.board.index(0)
        cols = 5  # 2x5 그리드

        # 좌측 이동
        if i % cols != 0:
            result.append(self.get_state_to_operate(i, i-1, depth))
        # 우측 이동
        if i % cols != cols-1:
            result.append(self.get_state_to_operate(i, i+1, depth))
        # 상단 이동
        if i >= cols:
            result.append(self.get_state_to_operate(i, i-cols, depth))
        # 하단 이동
        if i < cols:
            result.append(self.get_state_to_operate(i, i+cols, depth))
        return result

    def __str__(self):
        return "\n".join([str(self.board[:5]), str(self.board[5:]), "----------------------------"])

    def __eq__(self, other):
        return self.board == other.board

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(tuple(self.board))

# 초기 상태 설정
puzzle = [2, 1, 9, 4, 7, 0, 5, 3, 6, 8]
goal = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

max_depth = 30
found = False
final_count = 0
final_depth = 0

for depth_limit in range(max_depth):
    open_stack = [State(puzzle, goal)]
    closed_set = set()
    count = 0
    local_found = False

    while open_stack and not local_found:
        current = open_stack.pop()
        count += 1

        if current.board == goal:
            print("탐색 성공")
            local_found = True
            final_count = count
            final_depth = current.depth
            found = True
            break

        if current.depth >= depth_limit:
            continue

        if current in closed_set:
            continue
        closed_set.add(current)

        for state in current.expand(current.depth + 1):
            if state not in closed_set and state not in open_stack:
                open_stack.append(state)

    if found:
        break

if found:
    print(f"총 탐색 횟수: {final_count}, 최종 깊이: {final_depth}")
else:
    print("탐색 실패")