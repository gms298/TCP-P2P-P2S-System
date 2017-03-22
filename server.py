#!/usr/bin/env python

import socket
import thread

TCP_IP = '127.0.0.1'
TCP_PORT = 7734
BUFFER_SIZE = 1024

# Each client entry in Client Linked list ['hostname','Port number']
peer = []
# Each rfc entry in RFC Linked list['hostname','RFC No', 'RFC Title']
rfc = []

# -------------------------------------------------
#Data structure 
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

#Linked List
class LinkedList (object):
	def __init__(self, rroot = None):
		self.root = rroot
		self.size = 0
	def get_size(self):
		return self.size
	def add(self, dta):
		new_node = Node (dta, self.root)
		self.root = new_node
		self.size +=1
	def remove(self, dta):
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
	def find(self, ref, dta):

		self.root = ref
		this_node = self.root
		while this_node:
			match = this_node.get_data()	
			hostname = match[0]
			portnumber = match[1]
			if hostname == dta:
				 # return this_node.get_data() 
				return portnumber 
			else:
				this_node = this_node.get_next()
		return None

	def findPeer(self, ref, dta):
		self.root = ref
		this_node = self.root
		to_Return = ""
		while this_node:
			match = this_node.get_data()	
			hostname = match[0]
			if hostname == dta:
				 to_Return = match[1]
				 break
			else:
				this_node = this_node.get_next()
				to_Return = "ERROR"
		return to_Return

	def findRFC(self, ref, dta):

		self.root = ref
		this_node = self.root
		hostmatch = []
		while this_node:
			match = this_node.get_data()	
			rfcnum = match[0]
			hostname = match[2]
			if int(rfcnum) == dta:

				hostmatch.append(hostname)
				this_node = this_node.get_next()
			else:
				this_node = this_node.get_next()
		return hostmatch

	def get_root(self):
		return self.root

# -------------------------------------------------
# SERVER LOGIC
serverPeersList = LinkedList()
serverRFCList = LinkedList()

def ADD(rfc_no, rfc_title, ip, port):
	# Adding Peer into serverPeersList
	if serverPeersList.find(serverPeersList.get_root(), ip):
		print "Entry "+ip+" : "+str(port)+" already exists"
	else:
		temp = [ip,int(port)]
		print "================TO CHECK DATA TYPE BEFORE ADDING INTO LINKED LIST================"
		print temp
		serverPeersList.add(temp)
		print "Entry "+ip+" : "+str(port)+" added to the list"

	# Adding RFC details into serverRFCList
	hostmatch = serverRFCList.findRFC(serverRFCList.get_root(), int(rfc_no))
	if not hostmatch:
		print "Adding RFC File: "+rfc_no+" | "+rfc_title
		temp = [int(rfc_no),rfc_title,ip]
		serverRFCList.add(temp)
		print "================TO CHECK DATA TYPE BEFORE ADDING INTO LINKED LIST================"
		print temp
		print "SUCESS: No other hosts have this file. Added you to the list!"
		return True
	else:
		match = 0
		for host in hostmatch:
			if ip == host:
				match +=1
		if match > 0:
			print "FAILURE: TRYING TO ADD DUPLICATE RFC ENTRY!"
			return False
		else:
			print "Adding RFC File: "+rfc_no+" | "+rfc_title
			temp = [int(rfc_no),rfc_title,ip]
			serverRFCList.add(temp)
			print "================TO CHECK DATA TYPE BEFORE ADDING INTO LINKED LIST================"
			print temp
			print "SUCESS: Other Hosts have this file. Added you to the list anyway!"
			return True

# LOOKUP (COMMAND-LOOKUP, RFC, RFC-NUM, VERSION)
def LOOKUP(rfc_no):
	to_Return = ""
	hostmatch = serverRFCList.findRFC(serverRFCList.get_root(), int(rfc_no))
	if not hostmatch:
		print "FILE DOES NOT EXIST"
		return "ERROR"
	else:
		for host in hostmatch:
			port_number = serverPeersList.findPeer(serverPeersList.get_root(), host)
			to_Add = host+" "+str(port_number)+" \n"
			to_Return += to_Add
		return to_Return

# -------------------------------------------------
# COMMS

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(5)
print 'Listening on port 7734'

def client_thread(conn,addr):
	print 'New thread with connection address:', addr
	# Add this client to the serverPeersList
	# Ask 

	# Server logic
	while 1:

		data = conn.recv(BUFFER_SIZE)
		if not data: break
		read=data.split(' ')

		print "Received Command:", data

		if read[0]== "ADD":
			new_read = data.split('\n')
			print new_read[2].split('Port: ')[1]
			code = ADD(read[2], new_read[3].split('Title: ')[1], new_read[1].split('Host: ')[1], new_read[2].split('Port: ')[1])
			if code:
				conn.send("Added!")  
			else:
				conn.send("Entry already exists!")

		elif read[0]== "LOOKUP":
			code = LOOKUP(read[2])
			if code == "ERROR":
				conn.send("File Does Not Exist") 
			else:
				conn.send(code)

		elif read[0] == "LIST":
			code = LIST(read)
			if code == "ERROR":
				conn.send("No Entries in the list") 
			else:
				conn.send(code)
		else:
			conn.send("INVALID REQUEST!")

	# Delete client's entries from linked list
	# .. here 
	
	conn.close()

while 1:
	c, addr = s.accept()
	thread.start_new_thread(client_thread, (c, addr))

s.close()