'''초기 상태가 
2,1,9,4,7,
0,5,3,6,8
인 퍼즐을 

목표상태

0,1,2,3,4,
5,6,7,8,9

로 만드는 알고리즘이다

8 퍼즐 과 다른 점은
첫째, 초기상태와 목표상태의 행렬의 갯수이다

따라서 연산자 또한 달라진다

둘째, 좌우 상하 연산이 달라진다

8퍼즐에서는 3X3 특성상
+3,-1,+1,-3
연산을 해주면 되지만 
2X5퍼즐즐에서는 그 범위가 달라져야한다.

2X5의 경우 자신의 인덱스 위치 i와
좌 는 i-1  위치 교환
우 는 i+1  위치 교환
상 은 i-5 위치 교환 
하 는 i-5 위치 교환 

셋째,
상하좌우를 적용시켜서는 안되는 인덱스가 달라진다
'상'연산이 제한되는 인덱스는 최상위행 0행에 위치한

0,1,2,3,4

'하'연산이 제한되는 인덱스는 최하위행 1행에 위치한
5,6,7,8,9

'좌'는
0,1
'우'는
4,9
따라서 이를 적용한 탐색 알고리즘은 아래와 같다
반복을 막기 위해 open과 closed를 활용한 알고리즘이다. 

하지만 BFS 방식을 사용하면 10,000회가 넘는 연산에도 정답을 못찾는다.

알고리즘의 문제인가 봐서 문제를 단순화했다.
1
[5, 1, 2, 3, 4]
[6, 0, 7, 8, 9]
----------------------------
2
[5, 1, 2, 3, 4]
[0, 6, 7, 8, 9]
----------------------------
3
[5, 0, 2, 3, 4]
[6, 1, 7, 8, 9]
----------------------------
4
[5, 1, 2, 3, 4]
[6, 7, 0, 8, 9]
----------------------------
5
[5, 1, 2, 3, 0]
[4, 6, 7, 8, 9]
----------------------------
6
[0, 1, 2, 3, 4]
[5, 6, 7, 8, 9]
----------------------------
탐색 성공
...

BFS는 제대로 구현되었다.

중간 출력을 제외하고 돌리면 35depth에있다., 연산으로 치면
 84조 7천억 의 연산을 해야한다
 2.5^35 ≈ 8.47 × 10^13

 따라서 a알고리즘을 적용해 봤는데 a알고리즘 은 탐색에 성공했다,
   이알고리즘도 10000회 이상의 연산을 해야 되었는데
 복잡한 문제라는 걸 알수있다.

 
'''
class State:
    def __init__(self,board,goal,depth=0):
        self.board=board
        self.goal=goal
        self.depth=depth
    def get_state_to_operate(self,i1,i2,depth):
        new_board=self.board[:]
        new_board[i1],new_board[i2]=new_board[i2],new_board[i1]
        return State(new_board,self.goal,depth)
    
    def expand(self, depth):
        result = []
        i = self.board.index(0)
        if i % 5 != 0:  # Left
            result.append(self.get_state_to_operate(i, i - 1, depth))

        if i >= 5:  # Up
            result.append(self.get_state_to_operate(i, i - 5, depth))

        if i < 5:  # Down
            result.append(self.get_state_to_operate(i, i + 5, depth))

        if i % 5 != 4:  # Right
            result.append(self.get_state_to_operate(i, i + 1, depth))
        return result
    
    def __str__(self):
        return str(self.board[:5])+"\n"+\
        str(self.board[5:])+"\n"+\
"----------------------------"
                   
    
    def __eq__(self, other):
        return self.board == other.board
    
    def __ne__(self, other):
        return self.board != other.board
#################초기상태########################
puzzle=[
        5, 1, 2, 3, 4,
    6, 0, 7, 8, 9
    ]
goal=[
       0,1,2,3,4,
       5,6,7,8,9  
    ]
open_queue = []
open_queue.append(State(puzzle,goal))

closed_queue = [ ]

depth=0
count=1
'''탐색 시작'''

while len(open_queue)!=0:
    current=open_queue.pop(0)
    # current는 State객체
    print(count)
    print(current)
    
    if current.board==goal:
        print("탐색 성공")
        break
    depth = current.depth+1
    count+=1
    closed_queue.append(current)
    #깊이 제한
    if depth>30:
        continue
    for state in current.expand(depth):
        #현재 상태에서 확장을 하고 확장된 리스트속 상태 객체 하나하나 꺼낸다.
        #그리고 이미 거쳐간 노드라면 중복을 피하기 위해 버린다.
        if (state in closed_queue)or (state in open_queue):
            continue
        else:#BFS이브로 맨뒤에 추가 마치 큐처럼
            open_queue.append(state)

