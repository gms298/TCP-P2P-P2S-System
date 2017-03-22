#!/usr/bin/env python

import socket

TCP_IP = '127.0.0.1'
TCP_PORT = 7734
BUFFER_SIZE = 1024

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

# COMMS
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

host_name = socket.gethostname()
s.send(host_name)

hello = s.recv(BUFFER_SIZE)
print hello

# Actual data to send
tosend = "ADD RFC 1234 P2P-CI/1.0"+"\n"+"Host: "+host_name+"\n"+"Port: 5678"+"\n"+"Title: A Proferred Official ICP"
#tosend = "LOOKUP RFC 123456 P2P-CI/1.0"+"\n"+"Host: "+host_name+"\n"+"Port: 5678"+"\n"+"Title: A Proferred Official ICP"
print tosend

s.sendall(tosend)
data = s.recv(BUFFER_SIZE)
print "Received data:", data

# while 1:
# 	print "Infinite Loop"

s.close()

