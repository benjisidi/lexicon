from lexicon_setup_gui import game_setup
from player import teamObj, playerObj
import sys
import time
import pygame
import numpy as np
from button import *

def legible_remaining_time(secs):
	mins = secs/60.
	minute = np.floor(mins)
	secs = (mins - minute)*60
	if minute == 0 and secs < 10:
		return '{:.2f}'.format(secs)
	else:
		minute = int(minute)
		secs = int(secs)
		return '{0:02d}'.format(minute) + ':' + '{0:02d}'.format(secs)

def next_word(player, word, words, pass_=False):
	words.remove(word)
	if not pass_:
		player.score += 1
	return words

def draw_game(surface, buttons, teams):
	# Draw calls for all images, objects etc
	bgColour = [20, 20, 20]
	pygame.draw.rect(surface, bgColour, (0, 0, 800, 600))
	pygame.draw.rect(surface, [50, 0, 25], (95, 250, 590, 50))
	for team in teams:
		team.update_score()
	scoreboardString = 'Scores: '
	for team in teams:
		scoreboardString += '\n{}: {}'.format(team.name, team.score)
	buttons['scoreboard'].body = scoreboardString
	for button_ in buttons:
		if button_ != 'passedWord':
			try:
				buttons[button_].draw(surface=surface, centre=True)
			except TypeError:
				buttons[button_].draw()
		buttons['passedWord'].draw(surface=surface)

def run_go(surface, buttons, clock, fps, player, teams, words, timeLimit):
	dummyWords = [x for x in words]
	startTime = time.time()
	passedWord = ''
	passed = False
	while time.time() - startTime < timeLimit:
		if not passed:
			i = np.random.randint(0, len(dummyWords))
		buttons['currentWord'].string = dummyWords[i]
		nextWord = False
		while not nextWord and (time.time() - startTime < timeLimit):
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_RETURN:
						dummyWords = next_word(player, dummyWords[i], dummyWords)
						nextWord = True
						passed = False
					elif event.key == pygame.K_BACKSPACE:
						if passedWord == '':
							passedWord = dummyWords[i]
							dummyWords = next_word(player, dummyWords[i], dummyWords, pass_=True)
							nextWord = True
						else:
							currentWord = dummyWords[i]
							dummyWords += [passedWord]
							passedWord = dummyWords[i]
							dummyWords.remove(currentWord)
							i = len(dummyWords)-1
							passed = True
							nextWord = True

			buttons['passedWord'].string = 'Passed word: ' + passedWord
			buttons['remainingTime'].string = legible_remaining_time(timeLimit - (time.time() - startTime))
			if dummyWords == []:
				if passedWord == '':
					return dummyWords # End the go if there are no words left
				dummyWords = [passedWord]
				passedWord = ''
			clock.tick(fps)
			draw_game(surface, buttons, teams)
			pygame.display.flip()
	if passedWord != '':
		dummyWords.append(passedWord)
	return dummyWords
		#May need extra flip here

def run_rounds(surface, buttons, clock, fps, teams, wordLists, timeLimit, maxRounds, startRound=0):
	# Loop over teams and players, running go for each
	roundNumber = startRound
	teamIndex = 0
	roundThemes = [key for key in wordLists]
	while roundNumber < maxRounds:
		numGos = max(len(x.players) for x in teams) * len(teams)
		go = 0
		buttons['roundLabel'].string = roundThemes[roundNumber%len(roundThemes)].upper()
		while go <= numGos-1:
			team = teams[teamIndex%len(teams)]
			if wordLists[roundThemes[roundNumber % len(roundThemes)]] != []:
				player = team.players[team.goIndex%len(team.players)]
				ready = False
				buttons['passedWord'].string = ''
				buttons['currentWord'].string = '{}: Press SPACE when ready.'.format(player.name)
				buttons['remainingTime'].string = 'ROUND {}: {}'.format(roundNumber + 1, roundThemes[roundNumber%len(roundThemes)].upper())
				while not ready:
					for event in pygame.event.get():
						if event.type == pygame.KEYDOWN:
							if event.key == pygame.K_SPACE:
								ready = True
					clock.tick(fps)
					draw_game(surface, buttons, teams)
					pygame.display.flip()

				startTimer = time.time()
				buttons['currentWord'].string = 'Get Ready!'

				readyTime = 2
				while time.time() - startTimer < readyTime:
					buttons['remainingTime'].string = '{:02d}'.format(int(np.ceil(readyTime - (time.time() - startTimer))))
					clock.tick(fps)
					draw_game(surface, buttons, teams)
					pygame.display.flip()

				wordLists[roundThemes[roundNumber % len(roundThemes)]] = run_go(surface, buttons, clock, fps, player, teams\
																		,wordLists[roundThemes[roundNumber % len(roundThemes)]], timeLimit)
				team.goIndex += 1
				teamIndex += 1
				go += 1
			roundNumber += 1
	return wordLists

def end_game(surface, buttons, clock, fps, teamList):
	quit = False
	buttons['currentWord'].string = 'Game Over'
	scores = {}
	winningScore = 0
	winningTeam = ''
	for team in teamList:
		if team.score > winningScore:
			winningScore = team.score
			winningTeam = team.name
	buttons['remainingTime'].string = winningTeam + ' Wins!'
	while not quit:
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == (pygame.K_q or pygame.K_ESCAPE):
					quit = True		
		clock.tick(fps)
		draw_game(surface, buttons, teamList)
		pygame.display.flip()
	pygame.quit()
	sys.exit(0)

def quit():
		pygame.quit()
		sys.exit(0)

def load_words(filePath):
	fileObj = open(filePath, 'r')
	lines = fileObj.readlines()
	strippedLines = [x.strip('\n\r') for x in lines]
	fileObj.close()
	return strippedLines

def run_game(param):
	surface = param[0]  
	fps = param[1] 
	clock = param[2] 
	teamList, chosen_dictionaries, timeLimit, maxRounds = game_setup(surface)
	scoreboardString = 'Scores: '
	for team in teamList:
		scoreboardString += '\n{}: {}'.format(team.name, team.score)
	buttonColour = [40, 40, 70]
	hotPink = [236, 0, 140]
	buttonFont = ['fonts/verdanaz.ttf', 14, 'file', [236, 0, 140], False, False]	
	currentWord = txt(surface, 400, 275, 'Game Setup', ['fonts/verdanaz.ttf', 30, 'file', [236, 0, 140], False, False])
	remainingTime = txt(surface, 400, 25, str(timeLimit), ['fonts/verdanaz.ttf', 36, 'file', [236, 0, 140], False, False])
	passedWord = txt(surface, 100, 350, 'Passed Word: ', ['fonts/verdanai.ttf', 20, 'file', [236, 0, 140], False, False])
	scoreboard = txtbox(surface, 25, 465, 300, 100, scoreboardString, ['fonts/verdanaz.ttf', 20, 'file', [165, 0, 98], False, False])
	quitButton = button(surface, 650, 500, 50, 20, 'rrect', text='QUIT', font=buttonFont, function=quit, colour = buttonColour)
	roundLabel = txt(surface, 100, 100, '', ['fonts/verdanaz.ttf', 20, 'file', [236, 0, 140], False, False])
	buttons = {'roundLabel':roundLabel, 'quitButton':quitButton, 'currentWord':currentWord, 'remainingTime':remainingTime, 'passedWord':passedWord, 'scoreboard':scoreboard}
	wordLists = {}
	for list_ in chosen_dictionaries:
		listName = list_.split('/')[-1][:-5]
		wordLists[listName] = load_words(list_)


	wordLists = run_rounds(surface, buttons, clock, fps, teamList, wordLists, timeLimit, maxRounds)
	
	continue_ = False

	while not continue_:
		buttons['currentWord'].string = 'Play another round? (y/n)'
		buttons['remainingTime'].string = 'Rounds over.'
		draw_game(surface, buttons, teamList)
		pygame.display.flip()
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_n:
					continue_ = True
				if event.key == pygame.K_y:
					wordLists = run_rounds(surface, buttons, clock, fps, teamList, wordLists, timeLimit, maxRounds+1, maxRounds)
					maxRounds += 1
			clock.tick(fps)
			draw_game(surface, buttons, teamList)
			pygame.display.flip()
	end_game(surface, buttons, clock, fps, teamList)


if __name__ == '__main__':
	run_game()