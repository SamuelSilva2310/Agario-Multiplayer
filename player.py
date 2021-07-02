"""This is the player class"""

import pygame
import random

COLORS = [(255,0,0), (255, 128, 0), (255,255,0), (128,255,0),(0,255,0),(0,255,128),(0,255,255),(0, 128, 255), (0,0,255), (0,0,255), (128,0,255),(255,0,255), (255,0,128),(128,128,128), (0,0,0)]

class Player:

	size = 20
	thickness = 0

	def __init__(self, x, y):
		
		self.x = x
		self.y = y
		self.player_color = COLORS[random.randint(0,len(COLORS) - 1)]

	def convert_coords_int(self):
		self.x = int(self.x)
		self.y = int(self.y)


	def move(self, x=0, y=0):
		self.x += x
		self.y += y


	def draw(self, win):
		pygame.draw.circle(win, self.player_color, (self.x,self.y), self.size, self.thickness)



