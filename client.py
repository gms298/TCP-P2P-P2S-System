#!/usr/bin/env python

import socket
import thread
#Read Files
import csv

# Define this client's IP address/ hostname and Port number
SERVER_IP = '127.0.0.1'
CLIENT_IP = '127.0.0.1'
SERVER_PORT = 7734
CLIENT_PORT = 4368
BUFFER_SIZE = 1024

# Data structure - Each node in a linked list
class Node(object):
		def __init__ (self, dta, next = None):
			self.data = dta
			self.next_node = next
		def get_next (self):
			return self.next_node
		def set_next(self, next):
			self.next_node = next
		def get_data (self):
			return self.data
		def set_data (self, dta):
			self.data = dta

# Linked List with add, find and remove methods
class LinkedList (object):
	def __init__(self, rroot = None):
		self.root = rroot
		self.size = 0
	def get_size (self):
		return self.size
	def add (self, dta):
		new_node = Node (dta, self.root)
		self.root = new_node
		self.size +=1
	def remove (self, dta):
		this_node = self.root
		prev_node = None
		while this_node:
			if this_node.get_data() == dta:
				if prev_node:
					prev_node.set_next(this_node.get_next())
				else:
					self.root = this_node
				self.size -= 1
				return True
			else:
				prev_node = this_node
				this_node = this_node.get_next()
		return False
	def find (self, ref, dta):

		self.root = ref
		this_node = self.root
		while this_node:
			match = this_node.get_data()
			rfc_n=match[1]	
			hostname = match[0]
			if rfc_n == dta:
				 # return this_node.get_data() 
				return hostname #to return pointer to this node	

			else:
				this_node = this_node.get_next()
		return None
	def findPeer (self, ref, dta):

		self.root = ref
		this_node = self.root
		while this_node:
			match = this_node.get_data()	
			hostname = match[0]
			if hostname == dta:
				 # return this_node.get_data() 
				return match #to return pointer to this node	

			else:
				this_node = this_node.get_next()
		return None
	def get_root(self):
		return self.root

# CLIENT LOGIC - P2P and P2S

# Spawn new thread processes to handle new p2p connections
def p2p_thread(conn1,addr):
	print 'New thread with connection address:', addr
	hel = conn1.recv(BUFFER_SIZE)
	print hel

	conn1.send("THANK YOU FOR CONNECTING")

	client_data = conn1.recv(BUFFER_SIZE)

	print client_data

	conn1.send("GOT YOUR CONNECTION !")

# Spawn new thread process to handle P2S communication
def p2s_thread():

	# P2S Connection
	s.connect((SERVER_IP, SERVER_PORT))
	s.send(CLIENT_IP)

	# If running in different machines, uncomment the lines below & comment the line above!
	# host_name = socket.gethostname()
	# s.send(host_name)

	# Receiving a welcome message from server
	hello = s.recv(BUFFER_SIZE)
	print hello

	# Call P2S Logic
	p2s_get_input()

# P2S logic
def p2s_get_input():
	user_input = raw_input('>>P2S: Enter your command (ADD/LOOKUP/LIST/P2P): ')
	if user_input == "ADD":
		rfc_no = raw_input(">> Enter RFC Number: ")
		rfc_title = raw_input(">> Enter RFC Title: ")
		tosend = "ADD RFC "+str(rfc_no)+" P2P-CI/1.0"+"\n"+"Host: "+CLIENT_IP+"\n"+"Port: "+str(CLIENT_PORT)+"\n"+"Title: "+rfc_title+"\n"

		s.sendall(tosend)
		data = s.recv(BUFFER_SIZE)

		print data

		p2s_get_input()

	elif user_input == "LOOKUP":
		rfc_no = raw_input(">> Enter RFC Number: ")
		rfc_title = raw_input(">> Enter RFC Title: ")
		tosend = "LOOKUP RFC "+str(rfc_no)+" P2P-CI/1.0"+"\n"+"Host: "+CLIENT_IP+"\n"+"Port: "+str(CLIENT_PORT)+"\n"+"Title: "+rfc_title+"\n"

		s.sendall(tosend)
		data = s.recv(BUFFER_SIZE)

		print data
		
		p2s_get_input()

	elif user_input == "LIST":
		tosend = "LIST ALL P2P-CI/1.0"+"\n"+"Host: "+CLIENT_IP+"\n"+"Port: "+str(CLIENT_PORT)+"\n"

		s.sendall(tosend)
		data = s.recv(BUFFER_SIZE)

		print data
		
		p2s_get_input()

	elif user_input == "P2P":
		print "Switching to P2P Menu ... \n"
		p2p_get_input()

	else:
		print "\n"
		p2s_get_input()

# P2P Logic
def p2p_get_input():
	user_input = raw_input('>>P2P: Enter your command (GET/P2S): ')
	if user_input == "GET":
		# Get RFC number and Title from user
		rfc_no = raw_input(">> Enter RFC Number: ")
		rfc_title = raw_input(">> Enter RFC Title: ")

		# LOOKUP the RFC from the server through active P2S connection
		tosend = "LOOKUP RFC "+str(rfc_no)+" P2P-CI/1.0"+"\n"+"Host: "+CLIENT_IP+"\n"+"Port: "+str(CLIENT_PORT)+"\n"+"Title: "+rfc_title+"\n"

		s.sendall(tosend)
		data = s.recv(BUFFER_SIZE)

		print data

		# Parse the LOOKUP reply
		read=data.split(' ')
		new_read = data.split('\n')

		print new_read[1]

		temp=new_read[1].split(' ')

		length = len(temp)

		print temp
		client_hostname = temp[length-3]
		client_port = temp[length-2]

		print "PORT number: "+client_port
		print "Hostname: "+client_hostname

		# Create a new socket to do a "GET" request - P2P 
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((str(client_hostname), int(client_port)))

		sock.send('HELLO')
		hello = sock.recv(BUFFER_SIZE)
		print hello

		tosend = "GET RFC "+str(rfc_no)+" P2P-CI/1.0"+"\n"+"Host: "+CLIENT_IP+"\n"+"OS: Mac OS 10.4.1"

		sock.sendall(tosend)

		client_data = sock.recv(BUFFER_SIZE)

		print client_data

		sock.close()

		p2p_get_input()

	elif user_input == "P2S":
		print "Switching to P2S Menu ... \n"
		p2s_get_input()

	else:
		print "\n"
		p2p_get_input()


# COMMS

# P2S socket on a new thread
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
thread.start_new_thread(p2s_thread, ())

# P2P socket on an infinite loop with multi-threading
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.bind((CLIENT_IP, CLIENT_PORT))
c.listen(5)
print 'Listening on port 4368 for P2P requests ..'

while 1:
	cl, addr = c.accept()
	thread.start_new_thread(p2p_thread, (cl, addr))
