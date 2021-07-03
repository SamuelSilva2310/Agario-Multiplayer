"""This is the player class"""

import pygame
import random
pygame.font.init()

COLORS = [(255,0,0), (255, 128, 0), (255,255,0), (128,255,0),(0,255,0),(0,255,128),(0,255,255),(0, 128, 255), (0,0,255), (0,0,255), (128,0,255),(255,0,255), (255,0,128),(128,128,128), (0,0,0)]
NAME_FONT = pygame.font.SysFont("comicsans",20)
SCORE_FONT = pygame.font.SysFont("comicsans",30)
WIN_WIDTH = 1400
WIN_HEIGHT = 800

class Player:

	size = 20
	thickness = 0

	def __init__(self, x, y, name):
		
		self.x = x
		self.y = y
		self.name = name
		self.player_color = COLORS[random.randint(0,len(COLORS) - 1)]

	def convert_coords_int(self):
		self.x = int(self.x)
		self.y = int(self.y)


	def move(self, x=0, y=0):
		self.x += x
		self.y += y


	def draw(self, win):
		pygame.draw.circle(win, self.player_color, (self.x,self.y), self.size, self.thickness)
		text = NAME_FONT.render(self.name, 1, (0,0,0))
		win.blit(text, (self.x - text.get_width()/2, self.y - text.get_height()/2))

	#Need a seperate function so we only see our score
	def draw_score(self,win):
		text = SCORE_FONT.render( "Score: " + str(int(self.size)), 1, (0,0,0))
		win.blit(text, (10, WIN_HEIGHT - text.get_height() - 10))


