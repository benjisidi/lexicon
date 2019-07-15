import os
import numpy as np
from player import teamObj, playerObj

def game_setup():
	# Create and fill the required number of team objects with user input
	teams = int(raw_input('Enter number of teams: '))
	teamList = []
	for i in range(teams):
		teamList.append(teamObj(raw_input('Name team ' + str(i + 1) + ': ')))
	for team in teamList:
		team.players = int(raw_input('How many players on team {}: '\
						.format(team.name)))
	for team in teamList:
		teamSize = team.players
		team.players = []
		print 'TEAM {}:'.format(team.name.upper())
		for i in range(teamSize):
			team.players.append(playerObj(raw_input('Name player {}: '\
							.format(i+1))))
	numWords = int(raw_input('Enter number of words per player: '))
	masterList = []
	for team in teamList:
		print '----' + team.name.upper() + ':'
		for player in team.players:
			print '-----' + player.name.upper() + ':'
			for i in range(0, numWords):
				masterList.append(raw_input('Enter word {}: '.format(i+1)))
				print '\033[A                                                    \033[A'
	timeLimit = int(raw_input('Set round timer in seconds: '))
	maxRounds = int(raw_input('Set number of rounds: '))
	return teamList, masterList, timeLimit, maxRounds

if __name__ == '__main__':
	game_setup()