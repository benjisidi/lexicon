'''
Player experience:
	-Read in dictionary
	-Set number of teams
	-Name teams
	-Number of players in teams
	-Name players
	-Set game parameters (time limit, number of rounds, number of passes per round)
	-Game start:
		-For the round time, display random words from dictionary 
		-Remove words once they have been displayed
		-Add 1 to team score
		-If pass:
			-Don't add to score
			-Don't remove word
			-Minus one from allowed passes
		-When time runs out, display score and move on to next team/player

Plan:
	-Draw Game_setup fn ---> USE TK
		-Choose dictionary
		-Name players
		-
	-Run_game fn ---> USE PYGAME
'''