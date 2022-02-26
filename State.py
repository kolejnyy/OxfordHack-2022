import numpy as np
import random

class State:
	def __init__(self, path, gold, categories, is_binary=False):
		self.path = path
		self.gold = gold
		self.categories = categories
		self.allQueries = np.load(path)
		self.num_of_sets = 5
		self.is_binary = is_binary
		# 6 records in total
		# 4 entries each, guessing the last one
		self.nextQuery()
		

	# Post: overwrites query with a new one
	def nextQuery(self):
		n = self.allQueries.shape[0]
		q = self.allQueries[random.randint(0, n - 1)]
		
		self.query = q[:self.num_of_sets]
		self.answer = q[self.num_of_sets]

	# Post: returns a higher-lower prediction
	def getPrediction(self):
		p1 = float(self.query[-1][-1])
		p2 = float(self.query[-2][-1])
		noise = random.randint(-10, 10)
		return (2*p1 - p2) + noise/100


 	# higher = true iff user predicted higher or equal
	# Post: returns true iff answer is correct 
	def checkAnswer(self, higher):
		if self.is_binary:
			if higher:
				return int(self.answer[-1]) == 1
			return int(self.answer[-1]) == 0
		if higher:
			return float(self.answer[-1]) > self.getPrediction()
		return float(self.answer[-1]) <= self.getPrediction()

	# udpates the state
	# Post: new query, gold updated depending on the answer
	def updateState(self, higher, bet):
		assert bet <= self.gold
		if self.checkAnswer(higher):
			self.gold += bet
		else: 
			self.gold -= bet
		self.nextQuery()
	
	def printSet(self, set):
		for i in range(len(set)):
			print("    ", self.categories[i], " = ", set[i])
	
	# used for debugging
	def printState(self):
		print("------- State -------")
		print("sets:")
		# Printing sets
		for i, q in enumerate(self.query):
			print("  set ", i)
			self.printSet(q)
		print("answer set:")
		self.printSet(self.answer)
		# -----
		print("gold =\t", self.gold)
		print("prediction = ", toPrice(self.getPrediction()))




# takes a float, and returns string with 2 decimal places
def toPrice(f):
    return "{:.2f}".format(f)
     