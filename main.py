import pygame
import os
import random
import math

#Local Imports
from player import Player
from blob import Blob
from network import Network

pygame.font.init()

WIN_WIDTH = 1400
WIN_HEIGHT = 800

BG_COLOR = (255,255,255)

PLAYER_SPEED = 2
MAX_BLOB_AMOUNT = 200
BLOB_START_RADIUS = 5
BLOB_GROW_AMOUNT = 0.5


"""How to check if ball collide
dis = math.sqrt((objec_x - object2_x)**2 + (object_y-object2_y)**2)
if dis <= START_BALL_RADIUS + PLAYER_SCORE:
"""

"""How to check if players collide
dis = math.sqrt((p1x - p2x)**2 + (p1y-p2y)**2)
if dis < players[player2]["score"] - players[player1]["score"]*0.85:
"""


#Game Stuff
balls = []
players = []



def generate_blobs(blobs = None):

	if blobs is None:
		blobs = []

	for _ in range(MAX_BLOB_AMOUNT - len(blobs)):
		x = random.randint(0,1400)
		y = random.randint(0,800)
		blobs.append(Blob(x,y))
	return blobs

 
def draw_window(win, players, blobs):
	#Fill screen so we clear frames
	win.fill(BG_COLOR)
	for blob in blobs:
		blob.draw(win)
	
	for player in players:
		players[player].draw(win)
	pygame.display.update()
	

def main():

	global players

	#WINDOW AND CLOCK STUFF
	win = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
	clock = pygame.time.Clock()
	FPS = 144

	#Connect client to server
	client = Network()
	current_id = client.connect()
	print("[ID]", current_id)
	players, blobs = client.send("get")
	
	#MAIN LOOP
	run = True
	while run:
		clock.tick(FPS)
		player = players[current_id]
		player.convert_coords_int()


		"""PLAYER MOVEMENT"""
		#####################

		keys = pygame.key.get_pressed()
		if keys[pygame.K_LEFT] or keys[pygame.K_a]:
			player.move(x = PLAYER_SPEED * (-1))

		if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
			player.move(x = PLAYER_SPEED)

		if keys[pygame.K_UP] or keys[pygame.K_w]:
			player.move(y = PLAYER_SPEED * (-1))

		if keys[pygame.K_DOWN] or keys[pygame.K_s]:
			player.move(y = PLAYER_SPEED)

		if player.x - 5 < 0:
			player.x = 10
		if player.x  + 5> WIN_WIDTH:
			player.x = WIN_WIDTH - 10
		if player.y  - 5 < 0:
			player.y = 10
		if player.y + 5 > WIN_HEIGHT:
			player.y = WIN_HEIGHT - 10

		data = "move" + " " + str(player.x) + " " + str(player.y)
		
		#get data again
		players, blobs = client.send(data)
		
		#Check collisions and blob amounts
		# player_collision()
		# check_collision(players,blobs)
		# blobs = generate_blobs(blobs)
		
		"""PYGAME EVENTS"""
		#####################
		for event in pygame.event.get():

			#EXIT PROGRAM
			if event.type == pygame.QUIT:
				run = False

		#Redraw Window -> Update Frames
		draw_window(win, players, blobs)

	pygame.quit()
	quit()

main()

	