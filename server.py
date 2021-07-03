import socket
import pickle
from _thread import *
import time
import random 
import math

#Local Imports
from player import Player
from blob import Blob

#SOCKET CONSTANTS
PORT = 5500
IP = socket.gethostbyname(socket.gethostname())
ADDR = (IP, PORT)
BUFSIZE = 10
MAX_CONNECTIONS = 30

#GAME CONSTANTS
MAX_BLOB_AMOUNT = 400
BLOB_START_RADIUS = 5
BLOB_GROW_AMOUNT = 0.3

#Game Variables
player_id = 0 #An ID wich will be given to each player.
connections = 0
players = {} # {"id" : PlayerObject}
blobs = []

##################
#  SERVER SETUP  #
##################

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
print("[SERVER] Server is starting...")

try:
	server.listen(MAX_CONNECTIONS)  # Listen for a certain amount of connections
	print("[SERVER] Waiting for connections...")
except Exception as e:
	print("[EXCEPTION]", e)


#Game Methods
def check_collision(players, blobs):
	"""
	Checks for player vs blob collision
	"""

	for player in players:
		p = players[player]
		px = p.x
		py = p.y

		for blob in blobs:
			bx = blob.x
			by = blob.y

			dis = math.sqrt((px - bx)**2 + (py-by)**2)
			if dis <= BLOB_START_RADIUS + p.size:
				p.size += BLOB_GROW_AMOUNT
				blobs.remove(blob)
	

def player_collision(players):
	"""
	Checks for player vs player collision
	"""
	sort_players = sorted(players, key=lambda x: players[x].size)
	for x, player1 in enumerate(sort_players):
		for player2 in sort_players[x+1:]:
			p1x = players[player1].x
			p1y = players[player1].y

			p2x = players[player2].x
			p2y = players[player2].y

			dis = math.sqrt((p1x - p2x)**2 + (p1y-p2y)**2)
			if dis < players[player2].size - players[player1].size*0.85:
				players[player2].size = math.sqrt(players[player2].size**2 + players[player1].size**2) # adding areas instead of radii
				players[player1].size = 20
				print("Killed")
				players[player1].x = random.randint(0,1400)
				players[player1].y = random.randint(0,800)


def generate_blobs(blobs):
	"""
	Generates blobs so the amount of blobs is always the MAX_BLOB_AMOUNT
	"""
	if len(blobs) == 0 :
		blobs = []

	for _ in range(MAX_BLOB_AMOUNT - len(blobs)):
		x = random.randint(0,1400)
		y = random.randint(0,800)
		blobs.append(Blob(x,y))
	
	return blobs

def player_thread(conn, id):

	"""A thread method that runs for every player/client"""
	global connections, players, blobs

	current_id = id

		
	#Receive name
	name = conn.recv(64).decode("utf-8")

	#Setup new Player
	x = random.randint(0,1400)
	y = random.randint(0,800)
	player = Player(x,y, name)
	players[current_id] = player

	conn.send(str(current_id).encode("utf-8")) #send ID to client

	#Start loop for game events
	while True:

		try:
			#recieve any command from a player
			data = conn.recv(32)
			data = data.decode("utf-8")

			#Do something depending on command recieved
			"""Data example: 
				'move x y'
				then we split by the ' ' space.
			"""

			if data.split(' ')[0] == "move":
				split_data=data.split(' ')
				x = int(split_data[1])
				y = int(split_data[2])
				players[current_id].x = x
				players[current_id].y = y

			#Check collisions
			check_collision(players,blobs)
			player_collision(players)

			blobs = generate_blobs(blobs)

			##need to send players, balls back to client.
			data_send = pickle.dumps((players, blobs))
			conn.send(data_send)

		except Exception as e:
			print("[EXCEPTION]", e)
			break

		time.sleep(0.001)

	print(f"[DISCONNECTED] Player ID: {current_id}")
	del players[current_id]
	conn.close()



blobs = generate_blobs(blobs)
while True:
	conn, addr = server.accept()
	print(f"[CONNECTION] {addr} connected. ") 
	connections += 1

	#start a new client thread
	start_new_thread(player_thread, (conn, player_id))
	player_id += 1

