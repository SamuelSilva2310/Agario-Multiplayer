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

LEADER_FONT = pygame.font.SysFont("comicsans", 30)


PLAYER_BASE_SPEED = 7

#Game Variables
balls = []
players = []

 
def draw_window(win, players, blobs, current_id):
	"""Draw Screen every Frame"""

	#Fill screen so we clear frames
	win.fill(BG_COLOR)

	for blob in blobs:
		blob.draw(win)
	
	#Draw players from the smallest to the biggest so the bigger 
	#are above the smaller when on screen 
	for player in sorted(players, key=lambda x: players[x].size):
		players[player].draw(win)
		if current_id == player:
			players[player].draw_score(win)


	#LEADERBOARD
	sort_players = list(reversed(sorted(players, key=lambda x: players[x].size)))

	amount = min(len(players), 5)
	for position, player in enumerate(sort_players[:amount]):

		text = LEADER_FONT.render(str(position+1) + ". " + players[player].name, 1, (0,0,0))
		win.blit(text, (WIN_WIDTH - text.get_width() - 20, 10 + position * 20)) 

	pygame.display.update()
	

def main():

	global players

	#WINDOW AND CLOCK STUFF
	win = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
	pygame.display.set_caption('Agar Clone')
	clock = pygame.time.Clock()
	FPS = 60

	#Get name from player
	name = str(input("Insert you name: "))

	#Connect client to server
	client = Network()
	current_id = client.connect(name)
	print("[ID]", current_id)
	players, blobs = client.send("get")
	
	#How far a player can go on each margin
	dif = 8

	#MAIN LOOP
	run = True
	while run:
		clock.tick(FPS)
		player = players[current_id]
		player.convert_coords_int()


		"""PLAYER MOVEMENT"""
		#####################

		#TO make player velocity decrease the bigger the player is
		# we subtract PLAYER_BASE_SPEED by it size / 40
		vel = PLAYER_BASE_SPEED - round(player.size/40)

		#Lowest velocity a player can have when getting bigger
		if vel <= 4:
			vel = 4

		keys = pygame.key.get_pressed()
		if keys[pygame.K_LEFT] or keys[pygame.K_a]:
			player.move(x = vel * (-1))

		if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
			player.move(x = vel)

		if keys[pygame.K_UP] or keys[pygame.K_w]:
			player.move(y =vel * (-1))

		if keys[pygame.K_DOWN] or keys[pygame.K_s]:
			player.move(y = vel)


		if player.x - dif < 0:
			player.x = 10
		if player.x  + dif > WIN_WIDTH:
			player.x = WIN_WIDTH - 10
		if player.y  - dif < 0:
			player.y = 10
		if player.y + dif > WIN_HEIGHT:
			player.y = WIN_HEIGHT - 10

		#Prepare data with the move command
		data = "move" + " " + str(player.x) + " " + str(player.y)
		
		#get data again
		players, blobs = client.send(data)
		
		"""PYGAME EVENTS"""
		for event in pygame.event.get():

			#EXIT PROGRAM
			if event.type == pygame.QUIT:
				run = False

		#Redraw Window -> Update Frames
		draw_window(win, players, blobs, current_id)

	pygame.quit()
	quit()

if __name__ == "__main__":
	main()

	