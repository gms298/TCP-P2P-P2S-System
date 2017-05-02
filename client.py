#!/usr/bin/env python

import socket
import thread
import os 
import platform
import datetime
import time
from mimetypes import MimeTypes
import urllib 

# Define this client's IP address/ hostname and Port number
SERVER_IP = ''
CLIENT_IP = ''

SERVER_PORT = 7735
CLIENT_PORT = 4443

BUFFER_SIZE = 1024

rfc_title_list = []
rfc_no_list = []

# Set OS String
if os.name == "posix":
	if platform.system() == "Darwin":
		v, _, _ = platform.mac_ver()
		OS = "macOS "+v
		print OS
	else:
		OS = platform.system()+" "+platform.release()
		print OS
else:
	OS = platform.system()+" "+platform.release()
	print OS

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

# CLIENT LOGIC - P2P and P2P

#need a loop to search valid RFCs
def searchrfc (array, dta):
		i = 0
		for amount in array:
			if array[i]== dta:
				print array[i]
				return "TRUE"#to say valid number	
			else:
				i+=1
		return None

# Spawn new thread processes to handle new p2p connections
def p2p_thread(conn1,addr):
	print 'New thread with connection address:', addr
	hel = conn1.recv(BUFFER_SIZE)
	# print hel

	conn1.send("Hello from Client!")
	#Recieve request from peer with RFC Number
	peer_info = conn1.recv(BUFFER_SIZE)
	# Value Passed as "GET RFC "+str(rfc_no)+" P2P-CI/1.0"+"\n"+"Host: "+CLIENT_IP+"\n"+"OS: Mac OS 10.4.1"
	print "RECEIVED DATA FROM PEER:" + peer_info
	#Hard Code
	#peer_info = "GET RFC 1234 P2P-CI/1.0\nHost: 127.0.0.1\nOS: Mac OS 10.4.1"

	#Split input by spaces to get rfcnum which is spot 2
	peer_info = peer_info.split(' ')

	#Send the appropriate text file back
	rfcnum = int(peer_info[2])

	# print rfcnum

	# print "RFC NO LIST",rfc_no_list


	match = searchrfc(rfc_no_list, rfcnum)

	if match == "TRUE":
		index = rfc_no_list.index(int(rfcnum))
		f_name = str(rfcnum)+"-"+str(rfc_title_list[index])+".txt"
		access = open( f_name, "r")
		#newfile = open(str(newfile)+".txt", "w")
		file = access.read()
		#newfile.write(file)
		access.close()
		#newfile.close()
		today = datetime.date.today()
		a = today.strftime("%a, %d %b %Y, %H:%M:%S %Z")
		b = time.ctime(os.path.getmtime(f_name))
		c = os.path.getsize(f_name)
		mime = MimeTypes()
		url = urllib.pathname2url(f_name)
		mime_type = mime.guess_type(url)
		d = mime_type[0]
		temp1 = "P2P-CI/1.0 200 OK\nDate: "+str(a)+"\n"+"OS: "+str(OS)+"\n"+"Last-Modified: "+str(b)+"\nContent-Length: "+str(c)+"\nContent-Type: "+str(d)+"\n"
		conn1.sendall(temp1)
		conn1.recv(BUFFER_SIZE)
		conn1.sendall(file)
		conn1.close()
		# print file 
	else:
		file = "FALSE"
		# print file 
		conn1.send("\nP2P-CI/1.0 400 Bad Request\n")
		conn1.close()

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
	# print hello

	# Adding files into Server automatically
	filelist =[]

   	# print os.listdir(".")

   	for file1 in os.listdir("."):
   		if file1.endswith(".txt"):
			filelist.append(file1)

	for i in filelist:
		rfc_no_list.append(int(i.split('.txt')[0].split('-')[0]))
		rfc_title_list.append(i.split('.txt')[0].split('-')[1])

	j=0
	for num in rfc_no_list:
		tosend = "ADD RFC "+str(num)+" P2P-CI/1.0"+"\n"+"Host: "+CLIENT_IP+"\n"+"Port: "+str(CLIENT_PORT)+"\n"+"Title: "+rfc_title_list[j]+"\n"
		j+=1
		s.sendall(tosend)
		data = s.recv(BUFFER_SIZE)
		print data

	# Call P2S Logic
	p2s_get_input()

# P2S logic
def p2s_get_input():
	user_input = raw_input('>>P2S: Enter your command (ADD/LOOKUP/LIST/P2P): ')
	if user_input == "ADD":
		while True:
			try:
				rfc_no = int(raw_input(">> Enter RFC Number: "))
				break
			except ValueError:
				print("Oops! Not a valid number.  Try again...")
		rfc_title = raw_input(">> Enter RFC Title: ")
		tosend = "ADD RFC "+str(rfc_no)+" P2P-CI/1.0"+"\n"+"Host: "+CLIENT_IP+"\n"+"Port: "+str(CLIENT_PORT)+"\n"+"Title: "+rfc_title+"\n"

		s.sendall(tosend)
		data = s.recv(BUFFER_SIZE)
		print data
		p2s_get_input()

	elif user_input == "LOOKUP":
		while True:
			try:
				rfc_no = int(raw_input(">> Enter RFC Number: "))
				break
			except ValueError:
				print("Oops! Not a valid number.  Try again...")
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
		while True:
			try:
				rfc_no = int(raw_input(">> Enter RFC Number: "))
				break
			except ValueError:
				print("Oops! Not a valid number.  Try again...")
						
		rfc_title = raw_input(">> Enter RFC Title: ")

		# LOOKUP the RFC from the server through active P2S connection
		tosend = "LOOKUP RFC "+str(rfc_no)+" P2P-CI/1.0"+"\n"+"Host: "+CLIENT_IP+"\n"+"Port: "+str(CLIENT_PORT)+"\n"+"Title: "+rfc_title+"\n"

		s.sendall(tosend)
		data = s.recv(BUFFER_SIZE)

		print data

		# Parse the LOOKUP reply
		read=data.split(' ')
		new_read = data.split('\n')

		if new_read[0].split('P2P-CI/1.0 ')[1].split(' ')[0]=="404":
			p2p_get_input()
		else:
			temp=new_read[1].split(' ')

			length = len(temp)

			client_hostname = temp[length-3]
			client_port = temp[length-2]

			# Create a new socket to do a "GET" request - P2P 
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.connect((str(client_hostname), int(client_port)))

			sock.send('HELLO')
			hello = sock.recv(BUFFER_SIZE)

			tosend = "GET RFC "+str(rfc_no)+" P2P-CI/1.0"+"\n"+"Host: "+CLIENT_IP+"\n"+"OS: "+OS+"\n"

			sock.sendall(tosend)

			initial = sock.recv(BUFFER_SIZE)
			temp2 = initial.split("\n")[0].split("P2P-CI/1.0 ")[1].split(" ")[0]

			if int(temp2)==200:
				sock.send("OK")
				client_data = sock.recv(BUFFER_SIZE)
				# Create new .txt file based off of rfc num
				writefile = open(str(rfc_no)+"-"+str(rfc_title)+ ".txt", "w")

				#write to new file file 
				writefile.write(client_data)
				writefile.close() 

				#add new RFC to this clients RFC List
				rfc_no_list.append(int(rfc_no))
				rfc_title_list.append(rfc_title)

				sock.close()

				tosend = "ADD RFC "+str(rfc_no)+" P2P-CI/1.0"+"\n"+"Host: "+CLIENT_IP+"\n"+"Port: "+str(CLIENT_PORT)+"\n"+"Title: "+rfc_title+"\n"
				s.sendall(tosend)
				dta = s.recv(BUFFER_SIZE)
				print dta
			else:
				print initial
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