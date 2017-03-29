import socket

TCP_IP = '127.0.0.1'
TCP_PORT = 7734
BUFFER_SIZE = 1024


client_rfcList =[]

tosend = "GET RFC 1234 P2P-CI/1.0\nHost: 127.0.0.1\nOS: Mac OS 10.4.1"
rfc_no = 1234

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#port and ip of who want to talk to
c.connect((TCP_IP, TCP_PORT))
c.send(tosend)

client_data = c.recv(BUFFER_SIZE)

print client_data

if client_data == "FALSE":
	print "404 NOT FOUND"
	c.close()
else:
	# Create new .txt file based off of rfc num
	writefile = open(str(rfc_no) + ".txt", "w")

	#write to new file file 
	writefile.write(client_data + "NEW VERSION!!!!!")
	writefile.close() 

	#add new RFC to this clients RFC List
	client_rfcList += rfc_no

	sock.close()
	c.close()