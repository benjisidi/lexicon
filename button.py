import pygame
import pygame.locals as pl
import numpy as np
import wx

class txt():

	def __init__(self, surface=None, x=0, y=0, string='', font=['default', 12, 'sys', [255,255,255], False, False]):
		self.string = string
		self.colour = font[3]
		size = font[1]
		bold = font[4]
		italic = font[5]
		self.size = size
		if font[0].lower() == 'default':
			font = pygame.font.get_default_font()
		if font[2].lower() == 'file':
			self.font = pygame.font.Font(font[0], size)
		elif font[2].lower() == 'sys':
			self.font = pygame.font.SysFont(font[0], size, bold, italic)
		self.dims = pygame.font.Font.size(self.font, self.string)
		self.x = x
		self.y = y
		self.surface = surface

	def draw(self, surface=None, x=None, y=None, centre=False):
		if surface == None:
			surface = self.surface
		if x == None:
			x = self.x
		if y == None:
			y = self.y
		string = self.string
		label = self.font.render(string, True, self.colour)
		if centre:
			self.dims = pygame.font.Font.size(self.font, self.string)
			x -= self.dims[0]/2
			y -= self.dims[1]/2
		surface.blit(label, (x, y))

class txtbox():
	def __init__(self, surface, x, y, width, height, body, font=['default', 12, 'sys', [255, 255, 255], False, False], autoscroll=True):
		self.x = x
		self.y = y
		self.width = width # in px
		self.height = height # in lines
		self.body = body
		self.font_params = font
		self.surface = surface
		self.topline = 0
		self.autoscroll = autoscroll
		if font[0].lower() == 'default':
			default_font = pygame.font.get_default_font()
			self.font = pygame.font.SysFont(default_font, font[1], font[4], font[5])
		elif font[2].lower() == 'file':
			self.font = pygame.font.Font(font[0], font[1])
		elif font[2].lower() == 'sys':
			self.font = pygame.font.SysFont(font[0], font[1], font[4], font[5])

	def draw(self, surface=None, centre=None):
		surface = self.surface
		words = [line.split(' ') for line in self.body.splitlines()]
		space = self.font.size(' ')[0]
		word_x, word_y = self.x, self.y
		if self.autoscroll:
			while len(words) - self.topline > self.height:
				self.topline += 1
			if len(words) > self.height:
				words = words[self.topline:self.topline + self.height]
		else:
			words = words[self.topline:self.topline + self.height]
	#	while len(words) > self.height:
	#		words[len(words)-1:len(words)] = []
		for line in words:
			for word in line:
				word_surface = self.font.render(word, 1, self.font_params[3])
				word_width, word_height = word_surface.get_size()
				if word_x + word_width >= self.x + self.width:
					word_x = self.x
					word_y += word_height
				self.surface.blit(word_surface, (word_x, word_y)) 
				word_x += word_width + space
			word_x = self.x
			word_y += word_height

	def scroll_up(self):
		self.autoscroll = False
		if self.topline > 0:
			self.topline -= 1

	def scroll_down(self):
		self.autoscroll = False
		if self.topline < len(self.body.splitlines()) - self.height:
			self.topline += 1

		'''printed_moves = moves
		while len(printed_moves) > linelimit:
			printed_moves[0:1] = []
		movetext = '\n'.join(printed_moves)
		text.writepre(screen, font, textarea, (0,0,0), movetext)'''


class button():

	def __init__(self, surface, x, y, width, height, shape, colour = [255, 255,255], hover_colours = [[0,0,0],[0,0,0],[255,255,255],[200, 200, 200]], function = None,\
				param=None, text=None, font=['default', 12, 'sys', [0, 0, 0]], rectrad=.2, holdable=False):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.function = function
		self.shape = shape
		self.colour = colour
		self.hover_colour = hover_colours[0]
		self.click_colour = hover_colours[1]
		self.current_colour = colour
		self.hover_text_colour = hover_colours[2]
		self.click_text_colour = hover_colours[3]
		self.neutral_text_colour = font[3]
		self.surface = surface
		self.param = param
		self.text = text
		self.font = font
		self.rectrad = rectrad
		self.clicked_counter = 0
		self.holdable = holdable

	def update_text(self, string):
		self.text = string

	def draw(self):
		# Initialize params
		width = self.width
		height = self.height
		x = self.x
		y = self.y
		if width >= height:
			radius = int(height * self.rectrad)
		else:
			radius = int(width * self.rectrad)
		function = self.function
		param = self.param
		surface = self.surface

		mouse = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()

		

		if (x < mouse[0] < (x + width)) and (y < mouse[1] < (y + height)) and (click == (1, 0, 0)) and (function != None) or self.clicked_counter != 0: # On click
			self.current_colour = self.click_colour
			self.font[3] = self.hover_text_colour
			self.clicked_counter += 1
			if self.clicked_counter > 1 and self.holdable:
				self.clicked_counter = 0
			elif self.clicked_counter > 1 and click != (1, 0, 0):
				self.clicked_counter = 0
			if param != None and self.clicked_counter == 0:
				function(param)
			elif self.clicked_counter == 0:
				function()


		elif (x < mouse[0] < (x + width)) and (y < mouse[1] < (y + height)) and (function != None):
			self.current_colour = self.hover_colour # Hover
			self.font[3] = self.click_text_colour

		else:
			self.current_colour = self.colour
			self.font[3] = self.neutral_text_colour

		colour = self.current_colour


		if colour[0] + colour[1] + colour[2] == 0:
			colourkey = (1,1,1)
		else:
			colourkey = (0,0,0)

		# Rounded Rectangle
		if self.shape == 'rrect':
			surf_temp = pygame.Surface((width,height))
			surf_temp.fill(colourkey)

			pygame.draw.rect(surf_temp,colour,(0,radius,width,height-2*radius),0)
			pygame.draw.rect(surf_temp,colour,(radius,0,width-2*radius,height),0)

			for point in [
				[radius,radius],
				[width-radius,radius],
				[radius,height-radius],
				[width-radius,height-radius]
			]:
				pygame.draw.circle(surf_temp,colour,point,radius,0)
			
		# Up arrow
		if self.shape == 'uarrow':
			height = int(self.width * 4/3.)
			surf_temp = pygame.Surface((width,height))
			surf_temp.fill(colourkey)
			pygame.draw.polygon(surf_temp, colour, [(0, height), (width/2, 0), (width/2, int(height*(5/8.)))])
			pygame.draw.polygon(surf_temp, colour, [(width/2, 0), (width, height), (width/2, int(height*(5/8.)))])

		# Down arrow; just draws up one then flips
		if self.shape == 'darrow':
			height = int(self.width * 4/3.)
			surf_temp = pygame.Surface((width,height))
			surf_temp.fill(colourkey)
			pygame.draw.polygon(surf_temp, colour, [(0, height), (width/2, 0), (width/2, int(height*(5/8.)))])
			pygame.draw.polygon(surf_temp, colour, [(width/2, 0), (width, height), (width/2, int(height*(5/8.)))])
			surf_temp = pygame.transform.flip(surf_temp, False, True)

		surf_temp.set_colorkey(colourkey)
		surface.blit(surf_temp,(x, y))

		if self.text != None:
			text = self.text
			font = self.font
			try: 
				bold = font[4]
			except IndexError: 
				bold = False
			try:
				italic = font[5]
			except IndexError: 
				italic = False
			label = txt(surface, x, y, text, [font[0], font[1], font[2], font[3], bold, italic])
			size = label.dims
			xpos = self.x + (self.width - size[0])/2
			ypos = self.y + (self.height - size[1])/2
			if  'avenir' in font[0]:
				ypos += font[1]*.14
			label.draw(surface, xpos, ypos)


class inputLabel():

	def __init__(self, surface, x, y, inputX, inputY, highlight_colour = [255, 255, 255]\
				,text=None, font=['default', 12, 'sys', [0, 0, 0]], rectrad=.2, active = False, cursorColour = [0,0,0]):
		self.surface = surface
		self.x = x
		self.y = y
		self.inputX = inputX
		self.inputY = inputY
		self.highlight_colour = highlight_colour
		self.text = text
		self.font = font
		self.active = active
		self.input = ''
		self.cursorPos = 0
		self.cursorVisible = False
		self.cursorColour = cursorColour
		self.cursorCounter = 0

	def draw(self, events):
		# Initialize params
		x = self.x
		y = self.y
		inputText = self.input
		font = self.font
		inputX = self.inputX
		inputY = self.inputY
		surface = self.surface
		size = 0
		try: 
			bold = font[4]
		except IndexError: 
			bold = False
		try:
			italic = font[5]
		except IndexError: 
			italic = False
		if self.active:
			if self.cursorCounter > 60:
				self.cursorCounter = 0
			if self.cursorCounter > 30:
				self.cursorVisible = True
			else: 
				self.cursorVisible = False
			for event in events:
				if event.type == pygame.KEYDOWN:
					self.cursorVisible
					if event.key == pl.K_BACKSPACE:
						self.input = self.input[:max(self.cursorPos -1, 0)] + self.input[self.cursorPos:]
						self.cursorPos = max(self.cursorPos -1, 0)
					elif event.key == pl.K_RIGHT:
						self.cursorPos = min(self.cursorPos + 1, len(self.input))
					elif event.key == pl.K_LEFT:
						self.cursorPos = max(self.cursorPos -1, 0)
					elif event.key == pl.K_RETURN:
						self.active = False
						self.cursorVisible = False
						return True
					else:
						self.input =  self.input[:self.cursorPos] + event.unicode + self.input[self.cursorPos:]
						self.cursorPos += len(event.unicode)
			# Draw highlight box
			tempLabel = txt(surface, x, y, self.input, [font[0], font[1], font[2], font[3], bold, italic])
			size = tempLabel.dims
			highlight = pygame.Surface((max(size[0], 10), size[1]), pygame.SRCALPHA, 32)
			highlight.fill(self.highlight_colour + [50])
			surface.blit(highlight, (inputX, inputY))
			del tempLabel
		else:
			self.cursorVisible = False
		if self.text != None:
			text = self.text
			font = self.font
			label = txt(surface, x, y, text, [font[0], font[1], font[2], font[3], bold, italic])
			size = label.dims
			label.draw(surface)

		if self.input != '':
			inputLabel = txt(surface, inputX, inputY, inputText, [font[0], font[1], font[2], font[3], bold, italic])
			size = inputLabel.dims
			inputLabel.draw(surface, inputX, inputY)

		if self.cursorVisible:
			tempLabel = txt(surface, inputX, inputY, self.input[:self.cursorPos], [font[0], font[1], font[2], font[3], bold, italic])
			tempLabelSize = tempLabel.dims
			pygame.draw.rect(surface, self.cursorColour, (inputX + tempLabelSize[0], inputY, 1, tempLabelSize[1]))
			del tempLabel

		self.cursorCounter += 1
		return False

	def get_input(self):
		output = self.input
		return output

class selector():

	def __init__(self, surface, x, y, inputX, inputY, highlight_colour = [255, 255, 255], box_colour = [255, 255, 255], selected = False\
				,text=None, font=['default', 12, 'sys', [0, 0, 0]], rectrad=.2, active = False):
		self.surface = surface
		self.x = x
		self.y = y
		self.inputX = inputX
		self.inputY = inputY
		self.highlight_colour = highlight_colour
		self.text = text
		self.font = font
		self.active = active
		self.selected = selected
		self.box_colour = box_colour



	def draw(self, events):
		# Initialize params
		x = self.x
		y = self.y
		font = self.font
		inputX = self.inputX
		inputY = self.inputY
		surface = self.surface
		size = 0
		try: 
			bold = font[4]
		except IndexError: 
			bold = False
		try:
			italic = font[5]
		except IndexError: 
			italic = False

		#Draw checkbox
		def draw_box(surface, x, y, font, checked=False, colour=[255, 255, 255], width=2):
			tempLabel = txt(string='X', font=font)
			length = tempLabel.dims[0]
			tempSurf = pygame.Surface((length+2, length+2), pygame.SRCALPHA, 32)
			pygame.draw.rect(tempSurf, colour, (0, 0, length, length), width)
			if checked:
				pygame.draw.line(tempSurf, colour, (0, 0), (length, length), width)
				pygame.draw.line(tempSurf, colour, (length, 0), (0, length), width)
			surface.blit(tempSurf, (x, y))
			return length

		boxColour = self.box_colour
		if self.active:
			for event in events:
				if event.type == pygame.KEYDOWN:
					if event.key == pl.K_RETURN:
						self.selected = not self.selected
						self.active = False
						return True
			
			# Draw highlight box
			'''highlight = pygame.Surface((size, size), pygame.SRCALPHA, 32)
			highlight.fill(self.highlight_colour + [50])
			surface.blit(highlight, (inputX, inputY))'''

			boxColour = self.highlight_colour

		if self.selected:
			size = draw_box(surface, inputX, inputY, font, checked=True, colour=boxColour)
		else:
			size = draw_box(surface, inputX, inputY, font, colour=boxColour)

		if self.text != None:
			text = self.text
			font = self.font
			label = txt(surface, x, y, text, [font[0], font[1], font[2], font[3], bold, italic])
			size = label.dims
			label.draw(surface)


	def get_selected(self):
		output = self.selected
		return output

class save_dialog():

	def __init__(self):
		pass

if __name__ == '__main__':
	niceFont = ['fonts/verdanaz.ttf', 20, 'file', [236, 0, 140], False, False]
	pygame.display.init()
	pygame.font.init()
	screen_size= [800, 600]
	surface = pygame.display.set_mode(screen_size)
	hotPink = [236, 0, 140]
	testInput = selector(surface, 50, 50, 250, 50, text = 'Enter Name:', active=True, font=niceFont,box_colour = hotPink)
	testInput2 = selector(surface, 50, 150, 250, 150, text = 'Enter Height:', active=False, font=niceFont, box_colour=hotPink)
	inputs = [testInput, testInput2]
	inputCounter = 0
	while True:
		clock = pygame.time.Clock()
		surface.fill((100, 100, 100))
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.KEYDOWN:
				if event.key == pl.K_UP:
					inputCounter -=1
				elif event.key == pl.K_DOWN:
					inputCounter += 1
		for i in range(0, len(inputs)):
			if inputs[i].draw(events):
				inputs[i].selected = not inputs[i].selected
			if inputCounter % len(inputs) == i:
				inputs[i].active = True
			else:
				inputs[i].active = False
				
		pygame.display.flip()
		clock.tick(60)