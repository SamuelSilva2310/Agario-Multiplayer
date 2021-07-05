"""This is the player class"""

import pygame
import random

# Local imports
import resources

pygame.font.init()

COLORS = resources.COLORS

NAME_FONT = pygame.font.SysFont("comicsans", 20)
SCORE_FONT = pygame.font.SysFont("comicsans", 30)
WIN_WIDTH = 1400
WIN_HEIGHT = 800


class Player:
    size = 20
    thickness = 0

    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name
        self.player_color = COLORS[random.randint(0, len(COLORS) - 1)]

    def convert_coords_int(self):
        """
        Converts player coords to int
        @return:
        """
        self.x = int(self.x)
        self.y = int(self.y)

    def move(self, x=0, y=0):
        """
        Moves player, changes its coords
        @param x: int
        @param y: int
        @return: None
        """
        self.x += x
        self.y += y

    def draw(self, win):
        """
        Draws the player and its name on screen
        @param win: pygame.Window
        @return: None
        """
        pygame.draw.circle(win, self.player_color, (self.x, self.y), self.size, self.thickness)
        text = NAME_FONT.render(self.name, 1, (0, 0, 0))
        win.blit(text, (self.x - text.get_width() / 2, self.y - text.get_height() / 2))


    def draw_score(self, win):
        """
        Draws the player score
        @param win: pygame.Window
        @return:None
        """
        text = SCORE_FONT.render("Score: " + str(int(self.size)), 1, (0, 0, 0))
        win.blit(text, (10, WIN_HEIGHT - text.get_height() - 10))
