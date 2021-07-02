import socket
import pickle

PORT = 5500
IP = socket.gethostbyname(socket.gethostname())
ADDR = (IP, PORT)
BUFSIZE = 10
MAX_CONNECTIONS = 5

class Network:
	#SOCKET CONSTANTS

	def __init__(self):
		self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.host = IP
		self.port = PORT
		self.addr = (self.host, self.port)

	def connect(self):

		self.conn.connect(self.addr)

		#ADD NAME HERE LATER, send to server

		#Receives a ID from server and returns it
		id = self.conn.recv(8).decode("utf-8")
		return int(id)

	def send(self, data):
		data_send = data.encode("utf-8")
		self.conn.send(data_send)

		reply = self.conn.recv(2048 * 4)
		reply = pickle.loads(reply)
		return reply

