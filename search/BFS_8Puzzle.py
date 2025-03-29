class State:
    def __init__(self,board,goal,depth=0):
        self.board=board
        self.goal=goal
        self.depth=depth
    def get_state_to_operate(self,i1,i2,depth):
        new_board=self.board[:]
        new_board[i1],new_board[i2]=new_board[i2],new_board[i1]
        return State(new_board,self.goal,depth)
    def expand(self,depth):
        result=[]
        i=self.board.index(0)
        if not i in [0,3,6]:#Left
            result.append(self.get_state_to_operate(i,i-1,depth))

        if not i in [0,1,2]:#Up
            result.append(self.get_state_to_operate(i,i-3,depth))

        if not i in [6,7,8]:#down
            result.append(self.get_state_to_operate(i,i+3,depth))

        if not i in [2,5,8]:#Right
            result.append(self.get_state_to_operate(i,i+1,depth))
        return result# 한 레벨의 탐색 완료
    
    def __str__(self):
        return str(self.board[:3])+"\n"+\
        str(self.board[3:6])+"\n"+\
        str(self.board[6:])+"\n"+\
"----------------------------"
                   
    
    def __eq__(self, other):
        return self.board == other.board
    
    def __ne__(self, other):
        return self.board != other.board
#################초기상태########################
puzzle=[
        2,8,3,
        1,6,4,
        7,0,5    
    ]
goal=[
       1,2,3,
       8,0,4,
       7,6,5    
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
    if depth>5:
        continue
    for state in current.expand(depth):
        #현재 상태에서 확장을 하고 확장된 리스트속 상태 객체 하나하나 꺼낸다.
        #그리고 이미 거쳐간 노드라면 중복을 피하기 위해 버린다.
        if (state in closed_queue)or (state in open_queue):
            continue
        else:#BFS이브로 맨뒤에 추가 마치 큐처럼
            open_queue.append(state)

