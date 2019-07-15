import os
import numpy as np
from player import teamObj, playerObj
import pygame
from button import *
import sys
import namegame
import lexicon_game

def main_menu():
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
	buttonColour = [40, 40, 70]
	titleFont = ['fonts/verdanaz.ttf', 36, 'file', [236, 0, 140], False, False]
	subtitleFont = ['fonts/verdanaz.ttf', 24, 'file', [236, 0, 140], False, False]
	buttonFont = ['fonts/verdanaz.ttf', 20, 'file', [236, 0, 140], False, False]
	quitButtonFont = ['fonts/verdanaz.ttf', 14, 'file', [236, 0, 140], False, False]

	def quit():
		pygame.quit()
		sys.exit(0)

	pygame.init()
	surface = pygame.display.set_mode((800, 600))
	pygame.display.set_caption('Lexicon v0.1')
	fps = 60
	clock = pygame.time.Clock()

	titleLabel = txt(surface, titleX, titleY, 'Welcome to Lexicon', font=titleFont)

	lexiconButton = button(surface, col1, row1, 300, 200, 'rrect', text='Predefined Words', font=buttonFont,\
							function=lexicon_game.run_game, param=[surface, fps, clock], colour=buttonColour)
	namegameButton = button(surface, col1 + 350, row1, 300, 200, 'rrect', text='User Inputted Words', font=buttonFont,\
							function=namegame.run_game, param=[surface, fps, clock], colour=buttonColour)
	quitButton = button(surface, 650, 500, 50, 20, 'rrect', text='QUIT', font=quitButtonFont, function=quit, colour = buttonColour)

	while True:
		events = pygame.event.get()
		surface.fill(bgColour)
		titleLabel.draw(centre=True)
		lexiconButton.draw()
		namegameButton.draw()
		quitButton.draw()
		clock.tick(fps)
		pygame.display.flip()

if __name__ == '__main__':
	main_menu()