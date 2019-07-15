import os
import numpy as np
from player import teamObj, playerObj
import pygame
from button import *
import sys

def game_setup(surface):
	global screenCounter
	titleX = 400
	titleY = 50
	subtitlePad = 35	
	col1 = 50
	row1 = 120
	col2 = 450
	lineSpacing = 30
	screenCounter = 0
	hotPink = [236, 0, 140]
	bgColour = [20, 20, 35]
	cursorColour = [255, 255, 255]
	buttonColour = [40, 40, 70]
	titleFont = ['fonts/verdanaz.ttf', 26, 'file', [236, 0, 140], False, False]
	subtitleFont = ['fonts/verdanaz.ttf', 24, 'file', [236, 0, 140], False, False]
	errorFont = ['fonts/verdanab.ttf', 20, 'file', [118, 0, 50], False, False]
	niceFont = ['fonts/verdanaz.ttf', 20, 'file', [236, 0, 140], False, False]
	buttonFont = ['fonts/verdanaz.ttf', 14, 'file', [236, 0, 140], False, False]
	teamSelector = inputLabel(surface, col1, row1, col2, row1, text = 'Enter Number of teams: '\
							,font=niceFont, highlight_colour=hotPink, active=True, cursorColour=cursorColour)
	clock = pygame.time.Clock()
	title = txt(surface, titleX, titleY, 'Game Setup', font=titleFont)

	def back_screen():
		global screenCounter
		screenCounter -= 1

	def quit():
		pygame.quit()
		sys.exit(0)

	quitButton = button(surface, 650, 500, 50, 20, 'rrect', text='QUIT', font=buttonFont, function=quit, colour = buttonColour)
	backButton = button(surface, 100, 500, 50, 20, 'rrect', text='BACK', font=buttonFont, function=back_screen, colour = buttonColour)
	errorTxt = txt(surface, 400, 450, '', font=errorFont)
	done = False
	while not done:

		if screenCounter == 0:
			teamSelector.active = True
		# ---NUMBER OF TEAMS
		while screenCounter == 0:
			events = pygame.event.get()
			surface.fill(bgColour)
			title.draw(centre=True)
			teamSelector.draw(events)
			for event in events:
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_RETURN:
						if teamSelector.get_input().strip(' ') == '0':
							errorTxt.string = 'Please enter an integer number of teams'
							teamSelector.active = True
						else:
							try:
								numTeams = int(teamSelector.get_input())
								screenCounter += 1
							except ValueError:
								errorTxt.string = 'Please enter an integer number of teams'
								teamSelector.active = True
			errorTxt.draw(centre=True)
			quitButton.draw()
			clock.tick(60)
			pygame.display.flip()

		# ---NAME TEAMS---
		if screenCounter == 1:
			teams = []
			teamSelectors = []
			inputCounter = 0
			errorTxt.string = ''
			for i in range(0, numTeams):
				teamSelectors.append(inputLabel(surface, col1, row1 + i*lineSpacing, col2, row1 + i*lineSpacing\
				, text='Name team {}:'.format(i+1),font=niceFont, highlight_colour=hotPink, cursorColour=cursorColour))
		while screenCounter == 1:
			redo = False
			events = pygame.event.get()
			surface.fill(bgColour)
			title.draw(centre=True)
			for i in range(0, len(teamSelectors)):
				if teamSelectors[i].draw(events):
					inputCounter += 1
				if inputCounter % len(teamSelectors) == i:
					teamSelectors[i].active = True
				else:
					teamSelectors[i].active = False
			for event in events:
				if event.type == pygame.KEYDOWN:
					if event.key == pl.K_UP:
						inputCounter -=1
					elif event.key == pl.K_DOWN:
						inputCounter += 1
					elif event.key == pl.K_RETURN:
						if inputCounter % len(teamSelectors) == 0 and (inputCounter != 0):
							for i in range(0, numTeams):
								if teamSelectors[i].get_input().strip(' ') == '':
									errorTxt.string = 'Please enter a name for all teams'
									redo = True
							if not redo:
								for i in range(0, numTeams):		
									teams.append(teamObj(teamSelectors[i].get_input(), []))
								screenCounter += 1								
			backButton.draw()
			quitButton.draw()
			errorTxt.draw(centre=True)
			clock.tick(60)
			pygame.display.flip()


		# ---NUMBER OF PLAYERS---
		if screenCounter == 2:
			teamNumbers = []
			for i in range(0, numTeams):
				teamNumbers.append(inputLabel(surface, col1, row1 + i*lineSpacing, col2, row1 + i*lineSpacing, \
					text='Number of players in {}:'.format(teams[i].name), font=niceFont, highlight_colour=hotPink, cursorColour=cursorColour))
			inputCounter = 0
			teamNumbers[0].active=True
			errorTxt.string = ''

		while screenCounter == 2:
			events = pygame.event.get()
			surface.fill(bgColour)
			title.draw(centre=True)
			for box in teamNumbers:
				box.draw(events)
			for event in events:
				if event.type == pygame.KEYDOWN:
					if event.key == pl.K_UP:
						inputCounter -=1
					elif event.key == pl.K_DOWN:
						inputCounter += 1
					elif event.key == pl.K_RETURN:
						inputCounter += 1
						if inputCounter % len(teamNumbers) == 0 and (inputCounter != 0):
							try:
								for i in range(0, len(teams)):
									teams[i].players += [playerObj('')]*int(teamNumbers[i].get_input())
								screenCounter += 1
							except ValueError:
								for i in range(0, len(teams)):
									teams[i].players = []
								errorTxt.string = 'Please enter an integer number of players'
								inputCounter -= 1

			for i in range(0, len(teamNumbers)):
				if i == inputCounter % len(teamNumbers):
					teamNumbers[i].active = True
				else:	
					teamNumbers[i].active = False
			errorTxt.draw(centre=True)
			backButton.draw()
			quitButton.draw()
			clock.tick(60)
			pygame.display.flip()

		if screenCounter == 3:
			playerList = []

		# ---NAME PLAYERS---
		if screenCounter >= 3 and (screenCounter < (3 + numTeams)):
			for i in range(0, numTeams):
				playerNames = []
				teamSubtitle = txt(surface, titleX, titleY + subtitlePad, 'TEAM ' + teams[i].name.upper(), font=subtitleFont)
				inputCounter = 0
				for j in range(0, len(teams[i].players)):
					playerNames.append(inputLabel(surface, col1, row1 + j*lineSpacing, col2, row1 + j*lineSpacing\
												,text='Name of player {}:'.format(j + 1), font=niceFont, highlight_colour=hotPink, cursorColour=cursorColour))
				while screenCounter == i+3:
					redo = False
					events = pygame.event.get()
					surface.fill(bgColour)
					for k in range(0, len(playerNames)):
						playerNames[k].draw(events)	
					for event in events:
						if event.type == pygame.KEYDOWN:
							if event.key == pl.K_UP:
								inputCounter -=1
							elif event.key == pl.K_DOWN:
								inputCounter += 1
							elif event.key == pl.K_RETURN:
								inputCounter += 1
								if inputCounter % len(playerNames) == 0 and (inputCounter != 0):
									for l in range(0, len(playerNames)):
										if playerNames[l].get_input().strip(' ') == '':
											errorTxt.string = 'Please enter a name for all players'
											redo = True
									if not redo:
										for l in range(0, len(playerNames)):
											teams[i].players[l] = playerObj(playerNames[l].get_input())
										screenCounter += 1

					for k in range(0, len(playerNames)):
						if k == inputCounter % len(playerNames):
							playerNames[k].active = True
						else:	
							playerNames[k].active = False

					title.draw(centre=True)
					teamSubtitle.draw(centre=True)
					errorTxt.draw(centre=True)
					backButton.draw()
					quitButton.draw()
					clock.tick(60)
					pygame.display.flip()

				#if playerNames[-1].draw(events):

		if screenCounter == numTeams + 3:
			
			timeLimit = 0
			maxRounds = 0
			wordsPerPlayer = 0
			errorTxt.string = ''
			timeInput = inputLabel(surface, col1, row1, col2, row1, text='Round time limit (s):', \
							font=niceFont, highlight_colour=hotPink, cursorColour=cursorColour)
			maxRoundsInput = inputLabel(surface, col1, row1+lineSpacing, col2, row1+lineSpacing, text='Number of rounds:', \
							font=niceFont, highlight_colour=hotPink, cursorColour=cursorColour)
			wPPInput = inputLabel(surface, col1, row1+lineSpacing*2, col2, row1+lineSpacing*2, text='Words per player:', \
							font=niceFont, highlight_colour=hotPink, cursorColour=cursorColour)
			inputCounter = 0
			paramInputs = [timeInput, maxRoundsInput, wPPInput]
			while screenCounter == 3 + numTeams:
				events = pygame.event.get()
				surface.fill(bgColour)
				for box in paramInputs:
					box.draw(events)
				for event in events:
					if event.type == pygame.KEYDOWN:
						if event.key == pl.K_UP:
							inputCounter -=1
						elif event.key == pl.K_DOWN:
							inputCounter += 1
						elif event.key == pl.K_RETURN:
							inputCounter += 1
							if inputCounter % 3 == 0 and (inputCounter != 0):
								try:
									timeLimit = int(timeInput.get_input())
									maxRounds = int(maxRoundsInput.get_input())
									wordsPerPlayer = int(wPPInput.get_input())
									screenCounter += 1
								except ValueError:
									errorTxt.string = 'Please enter an integer number for time, rounds and words.'
				for i in range(0, len(paramInputs)):
					if i == inputCounter%len(paramInputs):
						paramInputs[i].active = True
					else:
						paramInputs[i].active = False
				errorTxt.draw(centre=True)
				title.draw(centre=True)
				quitButton.draw()
				backButton.draw()
				clock.tick(60)
				pygame.display.flip()

		if screenCounter == 4 + numTeams:
			wordList = []
			for team in teams:
				for player in team.players:
					nameLabel = txt(surface, titleX, titleY + 60, player.name.upper() + ':', font=subtitleFont)
					for i in range(0, wordsPerPlayer):
						errorTxt.string = ''
						wordInput = inputLabel(surface, col1, row1, col2, row1, text='Enter word {}:'.format(i+1), \
									font=niceFont, highlight_colour=hotPink, active=True, cursorColour=cursorColour)
						advance = False
						while not advance:
							redo = False
							wordInput.active = True
							events = pygame.event.get()
							surface.fill(bgColour)
							nameLabel.draw(centre=True)
							wordInput.draw(events)
							for event in events:
								if event.type == pygame.KEYDOWN:
									if event.key == pl.K_RETURN:
										if wordInput.get_input().strip(' ') == '':
											errorTxt.string = 'Please enter a word'
											redo = True
										if not redo:
											wordList.append(wordInput.get_input())
											advance = True
							title.draw(centre=True)
							errorTxt.draw(centre=True)
							quitButton.draw()
							clock.tick(60)
							pygame.display.flip()
			screenCounter += 1

		if screenCounter == 5 + numTeams:	
			return teams, wordList, timeLimit, maxRounds


if __name__ =='__main__':
	pygame.display.init()
	pygame.font.init()
	surface = pygame.display.set_mode((800, 600))
	game_setup(surface)