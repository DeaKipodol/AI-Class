import random
POPULATION_SIZE = 4
MUTATION_RATE =0.1

SIZE =5

class Chromosome:
    '''
    유전자 알고리금의 구성요소중 염색체에 해당.
    각 염색체는 적합도(fitness) 평가가 가능해야 됨.
    '''
    def __init__(self,g=[]):
        # g=[]는 염색체의 데이터이며 본체이다. 따라서 생성시에 반드시 가져야 되는 것이므로 init에 빈리스트를 생성한다.
        #copy를 안하면 유전자를 만들때마다 하나의 g의 값을 계속 바꾸는 꼴이 된다.
        #Chromosome 객체를 만들 때 마다 그 객체만의 리스트를 만들기 위해 copy 사용
        self.genes =g.copy()                                                                                                    
        self.fitness = 0
        if self.genes.__len__()==0:
            i=0
            while i < SIZE :
                if random.random() > 0.5:
                    self.genes.append(1)
                else:
                    self.genes.append(0)
                i+=1
    def cal_fitness(self):
        self.fitness = 0
        value=0
        for i in range(SIZE):
            value += self.genes[i]*pow(2,SIZE-i-1)
        self.fitness = value
        return self.fitness
    def __str__(self):
        return self.genes.__str__() 
def print_population(population):
    i=0
    for x in population:
        print("chromosome #",i," : ",x," fitness : ",x.cal_fitness())
        i+=1
    print("")
# 선택연산
def select(population):
    max_value = sum([c.cal_fitness() for c in population])
    pick = random.uniform(0, max_value)
    current = 0
    # 룰렛휠에서어떤조각에속하는지를알아내는루프
    for c in population:
        current += c.cal_fitness()
        if current > pick:
            return c
# 교차연산
def crossover(pop):
    father = select(pop)
    mother = select(pop)
    index = random.randint(1, SIZE -1)
    child1 = father.genes[:index] + mother.genes[index:] 
    child2 = mother.genes[:index] + father.genes[index:] 
    return (child1, child2)
def mutate(c):
    for i in range(SIZE):
        if random.random() < MUTATION_RATE:
            if random.random() < 0.5:
                c.genes[i] = 1
            else:
                c.genes[i] = 0

if __name__ == "__main__":
    # 초기화
    population = []
    i=0

    while i< POPULATION_SIZE:
        population.append(Chromosome())
        i+= 1
        
    count=0
    population.sort(key=lambda x: x.cal_fitness(), reverse=True)
    print("세대번호=", count)
    print_population(population)
    count=1
    while population[0].cal_fitness() < 31:
        new_pop= []

        for _ in range(POPULATION_SIZE//2):
            ''' 우리는 다음 세대(new_pop)에 총 4개의 염색체를 채워 넣어야 합니다.
                그런데 crossover를 한 번 할 때마다 염색체가 2개씩 생깁니다.
                그렇다면 총 4개의 염색체를 만들려면 crossover를 몇 번 해야 할까요?
                crossover 1번 실행 -> 자식 2개 생성 (총 2개)
                crossover 1번 더 실행 -> 자식 2개 또 생성 (총 4개)
                결국 crossover를 2번 실행해야 목표인 4개의 염색체를 만들 수 있습니다.
                코드가 계산하는 방식 POPULATION_SIZE // 2

                코드는 이 '2번'이라는 횟수를 계산해야 합니다.
                전체 필요한 염색체 수(POPULATION_SIZE, 즉 4)를 crossover 한 번에 만들어지는 염색체 수(2)로 나눠주면 됩니다.
                4 / 2 = 2

                6개의 염색채도 마찬가지 6//2-> 3번
                '''
            c1, c2 = crossover(population)
            new_pop.append(Chromosome(c1))
            new_pop.append(Chromosome(c2))
        population = new_pop.copy()#선택된 염색체끼리 교차한 결과, 즉 다음세대

        #이후 돌연변이 연산
        for c in population:
            mutate(c)
        # 출력을 위한 정렬 - 적합도 기준
        population.sort(key=lambda x: x.cal_fitness(), reverse=True)
        print("세대번호=", count)
        print_population(population)
        count += 1
        if count > 100 : break;
        
''' 

아래는 첫세대만에 적합도를 찾은 실행결과와 20세대 이상 되서야 문제를 해결한 실행 결과이다. 
이처럼 유전자 알고리즘은 수행 시간을 예측할 수 없다.
순전히 확률적인 특성을 가지기 때문이다.

    실행결과 1:
    세대번호= 0
    chromosome # 0  :  [1, 1, 1, 1, 1]  fitness :  31
    chromosome # 1  :  [0, 0, 1, 1, 0]  fitness :  6
    chromosome # 2  :  [0, 0, 1, 0, 0]  fitness :  4
    chromosome # 3  :  [0, 0, 0, 0, 1]  fitness :  1
    실행결과 2:
    세대번호= 0
    chromosome # 0  :  [1, 0, 1, 1, 0]  fitness :  22
    chromosome # 1  :  [1, 0, 1, 0, 0]  fitness :  20
    chromosome # 2  :  [0, 0, 1, 1, 1]  fitness :  7
    chromosome # 3  :  [0, 0, 0, 0, 0]  fitness :  0

    세대번호= 1
    chromosome # 0  :  [1, 1, 1, 0, 0]  fitness :  28
    chromosome # 1  :  [1, 0, 1, 0, 0]  fitness :  20
    chromosome # 2  :  [1, 0, 1, 0, 0]  fitness :  20
    chromosome # 3  :  [1, 0, 0, 0, 0]  fitness :  16

    세대번호= 2
    chromosome # 0  :  [1, 1, 1, 0, 0]  fitness :  28
    chromosome # 1  :  [1, 1, 1, 0, 0]  fitness :  28
    chromosome # 2  :  [1, 1, 1, 0, 0]  fitness :  28
    chromosome # 3  :  [1, 0, 0, 0, 0]  fitness :  16

    세대번호= 3
    chromosome # 0  :  [1, 1, 0, 0, 0]  fitness :  24
    chromosome # 1  :  [1, 0, 1, 0, 0]  fitness :  20
    chromosome # 2  :  [1, 0, 0, 0, 0]  fitness :  16
    chromosome # 3  :  [1, 0, 0, 0, 0]  fitness :  16

    세대번호= 4
    chromosome # 0  :  [1, 1, 0, 0, 0]  fitness :  24
    chromosome # 1  :  [1, 0, 1, 0, 0]  fitness :  20
    chromosome # 2  :  [1, 0, 0, 0, 0]  fitness :  16
    chromosome # 3  :  [1, 0, 0, 0, 0]  fitness :  16

    세대번호= 5
    chromosome # 0  :  [1, 0, 1, 0, 0]  fitness :  20
    chromosome # 1  :  [1, 0, 0, 0, 0]  fitness :  16
    chromosome # 2  :  [1, 0, 0, 0, 0]  fitness :  16
    chromosome # 3  :  [1, 0, 0, 0, 0]  fitness :  16

    세대번호= 6
    chromosome # 0  :  [1, 0, 0, 0, 0]  fitness :  16
    chromosome # 1  :  [1, 0, 0, 0, 0]  fitness :  16
    chromosome # 2  :  [1, 0, 0, 0, 0]  fitness :  16
    chromosome # 3  :  [1, 0, 0, 0, 0]  fitness :  16

    세대번호= 7
    chromosome # 0  :  [1, 1, 0, 0, 0]  fitness :  24
    chromosome # 1  :  [1, 0, 0, 0, 0]  fitness :  16
    chromosome # 2  :  [1, 0, 0, 0, 0]  fitness :  16
    chromosome # 3  :  [1, 0, 0, 0, 0]  fitness :  16

    세대번호= 8
    chromosome # 0  :  [1, 1, 0, 0, 0]  fitness :  24
    chromosome # 1  :  [1, 0, 0, 0, 0]  fitness :  16
    chromosome # 2  :  [1, 0, 0, 0, 0]  fitness :  16
    chromosome # 3  :  [1, 0, 0, 0, 0]  fitness :  16

    세대번호= 9
    chromosome # 0  :  [1, 1, 0, 0, 0]  fitness :  24
    chromosome # 1  :  [1, 1, 0, 0, 0]  fitness :  24
    chromosome # 2  :  [1, 1, 0, 0, 0]  fitness :  24
    chromosome # 3  :  [1, 0, 1, 0, 0]  fitness :  20

    세대번호= 10
    chromosome # 0  :  [1, 1, 1, 0, 0]  fitness :  28
    chromosome # 1  :  [1, 1, 0, 0, 1]  fitness :  25
    chromosome # 2  :  [1, 1, 0, 0, 0]  fitness :  24
    chromosome # 3  :  [1, 0, 0, 0, 1]  fitness :  17

    세대번호= 11
    chromosome # 0  :  [1, 1, 1, 0, 1]  fitness :  29
    chromosome # 1  :  [1, 1, 1, 0, 0]  fitness :  28
    chromosome # 2  :  [1, 1, 0, 0, 0]  fitness :  24
    chromosome # 3  :  [1, 0, 1, 0, 0]  fitness :  20

    세대번호= 12
    chromosome # 0  :  [1, 1, 1, 1, 0]  fitness :  30
    chromosome # 1  :  [1, 1, 1, 1, 0]  fitness :  30
    chromosome # 2  :  [1, 1, 0, 0, 1]  fitness :  25
    chromosome # 3  :  [1, 1, 0, 0, 0]  fitness :  24

    세대번호= 13
    chromosome # 0  :  [1, 1, 0, 0, 1]  fitness :  25
    chromosome # 1  :  [1, 1, 0, 0, 0]  fitness :  24
    chromosome # 2  :  [1, 1, 0, 0, 0]  fitness :  24
    chromosome # 3  :  [1, 1, 0, 0, 0]  fitness :  24

    세대번호= 14
    chromosome # 0  :  [1, 1, 0, 0, 1]  fitness :  25
    chromosome # 1  :  [1, 1, 0, 0, 0]  fitness :  24
    chromosome # 2  :  [1, 1, 0, 0, 0]  fitness :  24
    chromosome # 3  :  [0, 1, 0, 0, 0]  fitness :  8

    세대번호= 15
    chromosome # 0  :  [1, 1, 0, 0, 1]  fitness :  25
    chromosome # 1  :  [1, 1, 0, 0, 0]  fitness :  24
    chromosome # 2  :  [1, 1, 0, 0, 0]  fitness :  24
    chromosome # 3  :  [1, 1, 0, 0, 0]  fitness :  24

    세대번호= 16
    chromosome # 0  :  [1, 1, 0, 1, 0]  fitness :  26
    chromosome # 1  :  [1, 1, 0, 1, 0]  fitness :  26
    chromosome # 2  :  [1, 1, 0, 0, 0]  fitness :  24
    chromosome # 3  :  [1, 1, 0, 0, 0]  fitness :  24

    세대번호= 17
    chromosome # 0  :  [1, 1, 0, 1, 0]  fitness :  26
    chromosome # 1  :  [1, 1, 0, 1, 0]  fitness :  26
    chromosome # 2  :  [1, 1, 0, 0, 0]  fitness :  24
    chromosome # 3  :  [1, 1, 0, 0, 0]  fitness :  24

    세대번호= 18
    chromosome # 0  :  [1, 1, 0, 1, 0]  fitness :  26
    chromosome # 1  :  [1, 1, 0, 1, 0]  fitness :  26
    chromosome # 2  :  [1, 1, 0, 0, 0]  fitness :  24
    chromosome # 3  :  [1, 1, 0, 0, 0]  fitness :  24

    세대번호= 19
    chromosome # 0  :  [1, 1, 1, 0, 0]  fitness :  28
    chromosome # 1  :  [1, 1, 0, 1, 0]  fitness :  26
    chromosome # 2  :  [1, 1, 0, 1, 0]  fitness :  26
    chromosome # 3  :  [1, 1, 0, 1, 0]  fitness :  26

    세대번호= 20
    chromosome # 0  :  [1, 1, 1, 1, 0]  fitness :  30
    chromosome # 1  :  [1, 1, 0, 1, 0]  fitness :  26
    chromosome # 2  :  [1, 1, 0, 1, 0]  fitness :  26
    chromosome # 3  :  [0, 1, 0, 0, 0]  fitness :  8

    세대번호= 21
    chromosome # 0  :  [1, 1, 1, 1, 0]  fitness :  30
    chromosome # 1  :  [1, 1, 1, 0, 0]  fitness :  28
    chromosome # 2  :  [1, 1, 0, 1, 0]  fitness :  26
    chromosome # 3  :  [1, 1, 0, 0, 0]  fitness :  24

    세대번호= 22
    chromosome # 0  :  [1, 1, 1, 1, 0]  fitness :  30
    chromosome # 1  :  [1, 1, 1, 1, 0]  fitness :  30
    chromosome # 2  :  [1, 1, 1, 0, 1]  fitness :  29
    chromosome # 3  :  [1, 1, 0, 1, 0]  fitness :  26

    세대번호= 23
    chromosome # 0  :  [1, 1, 1, 1, 1]  fitness :  31
    chromosome # 1  :  [1, 1, 1, 1, 0]  fitness :  30
    chromosome # 2  :  [1, 1, 1, 0, 1]  fitness :  29
    chromosome # 3  :  [1, 1, 1, 0, 1]  fitness :  29

        '''