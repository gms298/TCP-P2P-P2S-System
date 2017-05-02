#!/usr/bin/env python

import socket
import thread

TCP_IP = ''
TCP_PORT = 7735
BUFFER_SIZE = 1024

#variables for status codes
statuscode = ['200','400','404','505']
phrase = ['OK','Bad Request', 'Not Found', 'P2P-CI Version Not Supported']
version = 'P2P-CI/1.0'
supported_version = '1.0'

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

	def removePeer(self, dta):
		if self.root == None:
			return False
		this_node = self.root
		prev_node = None
		count = 0
		while this_node:
			match = this_node.get_data()	
			hostname = match[0]
			if hostname == dta:
				if prev_node:
					prev_node.set_next(this_node.get_next())
					prev_node = this_node
					this_node = this_node.get_next()
				else:
					self.root = this_node.get_next()
					prev_node = None
					this_node = this_node.get_next()

				self.size -= 1
				count +=1
			else:
				prev_node = this_node
				this_node = this_node.get_next()
		if count>0:
			return True
		else:
			return False

	def removeRFC(self, dta):
		this_node = self.root
		prev_node = None
		count = 0
		while this_node:
			match = this_node.get_data()	
			hostname = match[2]
			if hostname == dta:
				if prev_node:
					prev_node.set_next(this_node.get_next())
					prev_node = this_node
					this_node = this_node.get_next()
				else:
					self.root = this_node.get_next()
					prev_node = None
					this_node = this_node.get_next()
				self.size -= 1
				count +=1
			else:
				prev_node = this_node
				this_node = this_node.get_next()
		if count>0:
			return True
		else:
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

	# Parse through hostlist and RFC List and return RFC #, RFC title
	def entireList(self, ref, dta):
		# passed array format['RFC No', 'RFC Title', 'Hostname']
		self.root = ref
		this_node = self.root
		entireList = ""
		#return port number and host name then call rfc list to append those
		while this_node:
			match = this_node.get_data()	
			number = match[0]
			title = match[1]
			hostname = match[2]
			port_number = serverPeersList.findPeer(serverPeersList.get_root(), hostname)
			entireList += str(number)+" "+title+" "+hostname+" "+str(port_number)+"\n"
			this_node = this_node.get_next()
		return entireList #['RFC No', 'RFC Title', 'Hostname']

	def get_root(self):
		return self.root

# -------------------------------------------------
# SERVER LOGIC

# Each entry in Peers Linked list = > ['Hostname','Port number']
serverPeersList = LinkedList()
# Each entry in RFC Linked list = > ['RFC No', 'RFC Title', 'Hostname']
serverRFCList = LinkedList()

def ADD(rfc_no, rfc_title, ip, port):
	# Adding Peer into serverPeersList
	if serverPeersList.find(serverPeersList.get_root(), ip):
		print ' '
		# print "Entry "+ip+" : "+str(port)+" already exists"
	else:
		temp = [ip,int(port)]
		# print "================CHECK DATA TYPE BEFORE ADDING INTO LINKED LIST================"
		# print temp
		serverPeersList.add(temp)
		# print "Entry "+ip+" : "+str(port)+" added to the list"

	# Adding RFC details into serverRFCList
	hostmatch = serverRFCList.findRFC(serverRFCList.get_root(), int(rfc_no))
	if not hostmatch:
		# print "Adding RFC File: "+rfc_no+" | "+rfc_title
		temp = [int(rfc_no),rfc_title,ip]
		serverRFCList.add(temp)
		# print "================CHECK DATA TYPE BEFORE ADDING INTO LINKED LIST================"
		# print temp
		# print "SUCESS: No other hosts have this file. Added you to the list!"
		return True
	else:
		match = 0
		for host in hostmatch:
			if ip == host:
				match +=1
		if match > 0:
			# print "FAILURE: TRYING TO ADD DUPLICATE RFC ENTRY!"
			return False
		else:
			# print "Adding RFC File: "+rfc_no+" | "+rfc_title
			temp = [int(rfc_no),rfc_title,ip]
			serverRFCList.add(temp)
			# print "================TO CHECK DATA TYPE BEFORE ADDING INTO LINKED LIST================"
			# print temp
			# print "SUCESS: Other Hosts have this file. Added you to the list anyway!"
			return True


def LOOKUP(rfc_no, rfc_title):
	to_Return = version +" "+ statuscode[0] +" "+ phrase[0] + "\n"
	hostmatch = serverRFCList.findRFC(serverRFCList.get_root(), int(rfc_no))
	if not hostmatch:
		return "ERROR"
	else:
		for host in hostmatch:
			port_number = serverPeersList.findPeer(serverPeersList.get_root(), host)
			to_Add = str(rfc_no)+" "+rfc_title+" "+host+" "+str(port_number)+" \n"
			to_Return += to_Add
		return to_Return

#Client Entry:
#LIST ALL P2P-CI/1.0
#Host: thishost.csc.ncsu.edu
#Port: 5678

#Respons:
#version <sp> status code <sp> phrase <cr> <lf>
#<cr> <lf>
#RFC number <sp> RFC title <sp> hostname <sp> upload port number<cr><lf>
#RFC number <sp> RFC title <sp> hostname <sp> upload port number<cr><lf>
#...
#<cr><lf>
def LIST(rfc_no):
	to_Return = ""
	#Return RFC number, RFC title, hostname

	portlist = serverRFCList.entireList(serverRFCList.get_root(), "test")

	#Return Hostname, portnumber
	#namelist = serverPeersList.entireHosts(serverPeersList.get_root(), "Bogus" )

	#for no RFCs in the List
	if portlist=="":
		return "ERROR"
	else:
		to_Return = version +" "+ statuscode[0] +" "+ phrase[0] + "\n" + portlist
		return to_Return

def DELETE(ip):
	# DELETE every entry from serverPeersList
	deletePeer = serverPeersList.removePeer(ip)

	# DELETE every entry from serverRFCList
	deleteRFC = serverRFCList.removeRFC(ip)
	return None

# -------------------------------------------------
# COMMS

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(5)

print 'Listening on port 7734'

def client_thread(conn,addr):
	print 'New thread with connection address:', addr
	host_name = conn.recv(BUFFER_SIZE)

	conn.send("SERVER: Thank you for connecting!")
	# Add this client to the serverPeersList
	# Ask 

	# Server logic
	while 1:

		data = conn.recv(BUFFER_SIZE)
		if not data: break
		read=data.split(' ')

		print "REQUEST MESSAGE : \n", data

		new_read = data.split('\n')

		if read[0]== "LIST":
			p2p_version = read[2].split('\n')[0]
		else:
			p2p_version = read[3].split('\n')[0]
		

		if str(p2p_version.split('P2P-CI/')[1]) == supported_version:
			# Operations
			if read[0]== "ADD":
				code = ADD(read[2], new_read[3].split('Title: ')[1], new_read[1].split('Host: ')[1], new_read[2].split('Port: ')[1])
				if code:
					conn.send(version +" "+ statuscode[0] +" "+ phrase[0] + "\n" + read[2] +" "+ new_read[3].split('Title: ')[1] +" "+ new_read[1].split('Host: ')[1] +" "+ new_read[2].split('Port: ')[1] + "\n")  
				else:
					conn.send(version +" "+ statuscode[1] +" "+ phrase[1] + "\n")
				
			elif read[0]== "LOOKUP":
				code = LOOKUP(read[2], new_read[3].split('Title: ')[1])
				if code == "ERROR":
					conn.send(version +" "+ statuscode[2] +" "+ phrase[2] + "\n") 
				else:
					conn.send(code)

			elif read[0] == "LIST":
				code = LIST(read)
				if code == "ERROR":
					conn.send(version +" "+ statuscode[2] +" "+ phrase[2] + "\n") 
				else:
					conn.send(code)
			
			else:
				# Send a Bad request message
				conn.send(version +" "+ statuscode[1] +" "+ phrase[1] + "\n")
		else:
			# Send P2P version not supported
			conn.send(version +" "+ statuscode[3] +" "+ phrase[3] + "\n")
			
	# Delete client's entries from linked list
	DELETE(host_name)
	# Close connection
	conn.close()

while 1:
	c, addr = s.accept()
	thread.start_new_thread(client_thread, (c, addr))

s.close()