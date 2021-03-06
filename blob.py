"""This is the blob Class"""

import pygame
import random

# Local imports
import resources

COLORS = resources.COLORS


class Blob:
    size = 5
    thickness = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.blob_color = COLORS[random.randint(0, len(COLORS) - 1)]

    def draw(self, win):
        """
        Draws the blob on screen
        @param win: pygame.Window
        @return: None
        """
        pygame.draw.circle(win, self.blob_color, (self.x, self.y), self.size, self.thickness)
