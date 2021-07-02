"""This is the blob Class"""

import pygame
import random

COLORS = [(255,0,0), (255, 128, 0), (255,255,0), (128,255,0),(0,255,0),(0,255,128),(0,255,255),(0, 128, 255), (0,0,255), (0,0,255), (128,0,255),(255,0,255), (255,0,128),(128,128,128), (0,0,0)]

class Blob:

	size = 5
	thickness = 0

	def __init__(self,x, y):
		self.x = x
		self.y = y
		self.blob_color = COLORS[random.randint(0,len(COLORS) - 1)]

	def draw(self, win):
		pygame.draw.circle(win, self.blob_color, (self.x,self.y), self.size, self.thickness)

		