class teamObj:
	
	def __init__(self, name, players = []):
		self.name = name
		self.score = 0
		self.players = players
		self.goIndex = 0

	def update_score(self):
		total = 0
		for player in self.players:
			total += player.score
		self.score = total

class playerObj:

	def __init__(self, name):
		self.name = name
		self.score = 0