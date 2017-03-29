
import thread
import socket

NEWCLIENT_IP = '127.0.0.1'
SERVER_IP = '127.0.0.1'
CLIENT_IP = '127.0.0.1'

NEWCLIENT_PORT = 7734
CLIENT_PORT = 4368
BUFFER_SIZE = 1024

RFCLIST = [1234, 4567, 7890]

# filename = "text.txt"
# results = ""
# writefile = open("newtext.txt", "w")

# with open('text.txt') as readfile:
# 	for line in readfile:
# 		results = str(line.strip().split('\n')[0])

# 		#write to file 
# 		writefile.write(results)
# 		writefile.write('\n')
# writefile.close() 		

# If running in different machines, uncomment the lines below & comment the line above!
# host_name = socket.gethostname()
# s.send(host_name)

#Create socket for someone to connect to in order to request an RFC
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((NEWCLIENT_IP, NEWCLIENT_PORT))
s.listen(1)
#accept from server 352
c, addr = s.accept()

c.connect()


while 1:

	#Recieve request from peer with RFC Number
	peer_info = c.recv(BUFFER_SIZE)
	# Value Passed as "GET RFC "+str(rfc_no)+" P2P-CI/1.0"+"\n"+"Host: "+CLIENT_IP+"\n"+"OS: Mac OS 10.4.1"
	print "RECEIVED DATA FROM PEER:" + peer_info
	#Hard Code
	#peer_info = "GET RFC 1234 P2P-CI/1.0\nHost: 127.0.0.1\nOS: Mac OS 10.4.1"

	#Split input by spaces to get rfcnum which is spot 2
	peer_info = peer_info.split(' ')

	#Send the appropriate text file back
	rfcnum = int(peer_info[2])

	print rfcnum

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

	#hardcode for now
	#rfcnum = 1234

	match = searchrfc(RFCLIST, rfcnum)

	#newfile = 9123

	if match == "TRUE":
		access = open( str(rfcnum) + ".txt", "r")
		#newfile = open(str(newfile)+".txt", "w")
		file = access.read()
		#newfile.write(file)
		access.close()
		#newfile.close()
		c.sendall(file)
		c.close()
		print file 
	else:
		file = "FALSE"
		print file 
		c.send(file)
		c.close()


