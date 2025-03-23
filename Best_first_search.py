''' 최고 우선 탐색은 평가값이 높은 상태를 먼저 탐색하는 방식이지만, Hill-Climbing을 개선한 방식이다.
    Hill-Climbing은 현재 상태에서 평가값이 높은 상태로만 이동하는 방식이기 때문에 지역 최적해에 빠질 수 있다.
    하지만 최고 우선 탐색은 이러한 문제를 해결하기 위해, 평가값이 높은 상태로만 이동하는 것이 아니라,
    open과 closed 리스트를 활용하여 탐색한 상태를 저장하고, 평가값이 높은 상태를 선택하되, 이전에 탐색한 상태는 제외하는 방식이다.
    이를 통해 지역 최적해에 빠지지 않고, 전역 최적해를 찾을 가능성을 높인다.
    이 코드는 2x5 퍼즐을 최고 우선 탐색 방식으로 푸는 코드이다.
    의사 코드는 다음과 같다.
    
    best_first(root)
        open<-[root]
        closed <-[]

    while open != [] do
    x<-the best vlaue of 평가 function in open list
    if x == goal then success
    else 

        x의 자식 노드를 생성한다
        x를 closed리스트에 추가한다
        if x의 자식노드가 open이나closed에있지않으면
        자식노드의 평가 함수값을 계산한다.
        자식노드를 open리스트에 추가한다.
        return falil
        ...

        놀랍게도 이 코드는 10,000회 이상의 연산을 했던 a * 알고리즘과 달리 1600g회 연산으로 정답을 찾았다.
====================================================================================================================
        현재 상태: [1, 0, 2, 3, 4, 5, 6, 7, 8, 9], 평가값: 8
        현재 상태: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 평가값: 10
        목표 상태에 도달했습니다! 탐색한 상태 수: 1649
'''
# 초기 상태와 목표 상태 정의
initial_state = [2, 1, 9, 4, 7, 0, 5, 3, 6, 8]
goal_state = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# 평가 함수 (목표 상태와 일치하는 위치가 많을수록 높은 점수)
def heuristic(state):
    return sum([1 if state[i] == goal_state[i] else 0 for i in range(len(state))])

# 퍼즐에서 가능한 이동 (빈 공간(0)과 인접한 값을 교환)
def get_state(state):
    children = []
    idx = state.index(0)
    
    moves = []
    if idx % 5 > 0: moves.append(-1)      # 왼쪽
    if idx % 5 < 4: moves.append(1)       # 오른쪽
    if idx - 5 >= 0: moves.append(-5)     # 위
    if idx + 5 < 10: moves.append(5)      # 아래

    for move in moves:
        new_state = state[:]
        swap_idx = idx + move
        new_state[idx], new_state[swap_idx] = new_state[swap_idx], new_state[idx]
        children.append(new_state)

    return children

# 최고 우선 탐색 (Hill-Climbing 방식)
def best_first(root):
    open_list = [root]
    closed_list = []
    state_count = 0

    while open_list:
        # open 리스트에서 평가값이 가장 높은 상태 선택
        open_list.sort(key=lambda x: heuristic(x), reverse=True)
        x = open_list.pop(0)
        state_count += 1

        print(f"현재 상태: {x}, 평가값: {heuristic(x)}")

        if x == goal_state:
            print(f"목표 상태에 도달했습니다! 탐색한 상태 수: {state_count}")
            return True
        else:
            closed_list.append(x)
            for child in get_state(x):
                if child not in open_list and child not in closed_list:
                    open_list.append(child)
                    #open에 넣을떄 어떻게 넣어도 상관없다. 어차피 sort를 통해 평가값이 높은 순으로 정렬되기 때문이다.

    print(f"목표 상태에 도달하지 못했습니다. 탐색한 상태 수: {state_count}")
    return False


# 알고리즘 실행
best_first(initial_state)