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
	# Team objects are now set up and have a list of player objects each.
	listDirectory = './wordLists'
	availableLists = os.listdir(listDirectory)
	availableLists = [x for x in availableLists if x.endswith('.list')]
	print '---AVAILABLE GAME CATEGORIES---'
	for i in range(len(availableLists)):
		print '[{}] '.format(i) + availableLists[i]
	selectedFile = availableLists[int(raw_input('Select desired category: '))]
	selectedFileObject = open(listDirectory + '/' + selectedFile, 'r' )
	masterList = [x.strip('\n\r') for x in selectedFileObject.readlines()]
	masterList = [x for x in masterList if len(x) > 3]
	timeLimit = int(raw_input('Set round timer in seconds: '))
	maxRounds = int(raw_input('Set number of rounds: '))
	return teamList, masterList, timeLimit, maxRounds

if __name__ == '__main__':
	game_setup()