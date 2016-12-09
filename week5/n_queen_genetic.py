import random
import copy
def swap(a, b):
	return b, a

def board_cmp(b1, b2):
	if b1.fitness > b2.fitness:
		return 1
	elif b1.fitness == b2.fitness:
		return 0
	else:
		return -1

class board:

	def calc_fitness(self):
		conflict = 0
		for i in range(self.n - 1):
			for j in range(i + 1, self.n):
				if abs(self.board[i] - self.board[j]) == j - i:
					conflict += 1
		self.fitness = 1.0 / (conflict + 1)

	def __init__(self, n = 8):
		self.n = n
		self.board = range(n)
		random.shuffle(self.board)
		self.calc_fitness()

	def mutate(self):
		cor = random.sample(range(self.n), 2)
		self.board[cor[0]], self.board[cor[1]] = swap(self.board[cor[0]], self.board[cor[1]])
		self.calc_fitness()

	def set_board(self, board):
		self.board = board
		self.calc_fitness()

	def display(self):
		for i in range(self.n):
			for j in range(self.n):
				if j == self.board.index(i):
					print 'Q',
				else:
					print '.',
			print

class queen_solver:

	def check(self):
		for b in self.population:
			if b.fitness > 0.8:
				return b
		return None

	def select(self):
		self.population.sort(cmp = board_cmp, reverse = True)
		self.parents = self.population[0 : int(self.survival * self.size)]

	def mate_one(self):
		parent = random.sample(self.parents, 2)
		index1 = random.randint(0, self.n)
		index2 = random.randint(0, self.n)
		while (index2 == index1):
			index2 = random.randint(0, self.n)
		if index1 > index2:
			index1, index2 = swap(index1, index2)
		section1 = parent[0].board[index1 : index2]
		section2 = parent[1].board[index1 : index2]
		start = parent[0].board[0:index1]
		end = parent[0].board[index2:self.n]
		for i in range(0, index1):
			while start[i] in section2:
				start[i] = section1[section2.index(start[i])]
		for i in range(index2, self.n):
			while end[i - index2] in section2:
				end[i - index2] = section1[section2.index(end[i - index2])]
		child = board(self.n)
		child.set_board(start + section2 + end)
		return child

	def reproduce(self):
		children = []
		while len(self.parents) + len(children) <= self.size:
			children.append(self.mate_one())
		self.population = self.parents + children

	def mutate(self):
		index_box = random.sample(range(self.size), int(self.size*self.mutation_rate))
		for i in index_box:
			self.population[i].mutate()

	def __init__(self, n = 8, size = 100, survival = 0.3, mutation_rate = 0.05):
		self.n = n
		self.population = []
		self.size = size
		self.survival = survival
		self.mutation_rate = mutation_rate
		for i in range(size):
			self.population.append(board(n))

	def print_best(self):
		self.population.sort(cmp = board_cmp, reverse = True)
		print self.population[0].fitness
		#self.population[0].display()

iter = 0
pop = queen_solver(n = 200, size = 200, survival = 0.5, mutation_rate = 0.05)
rs = pop.check()
while rs == None:
	iter+=1
	pop.select()
	pop.reproduce()
	pop.mutate()
	print iter
	pop.print_best()
	rs = pop.check()
rs.display()
