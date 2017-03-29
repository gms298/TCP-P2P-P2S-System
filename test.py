import socket

TCP_IP = '127.0.0.1'
TCP_PORT = 7734
BUFFER_SIZE = 1024

client_rfcList =[]

def get_input():
	user_input = raw_input('Enter your command (GET/EXIT): ')
	if user_input == "GET":
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((TCP_IP, TCP_PORT))

		host_name = socket.gethostname()
		s.send("127.0.0.4")

		hello = s.recv(BUFFER_SIZE)
		print hello

		rfc_no = raw_input(">> Enter RFC Number: ")
		rfc_title = raw_input(">> Enter RFC Title: ")
		tosend = "LOOKUP RFC "+str(rfc_no)+" P2P-CI/1.0"+"\n"+"Host: 127.0.0.4\n"+"Port: 5678"+"\n"+"Title: "+rfc_title

		s.sendall(tosend)
		data = s.recv(BUFFER_SIZE)

		s.close()

		print "Received data:", data

		read=data.split(' ')
		new_read = data.split('\n')

		print new_read[1]

		temp=new_read[1].split(' ')

		length = len(temp)

		print temp
		client_hostname = temp[length-3]
		client_port = temp[length-2]

		print "PORT number"+client_port
		print "Hostname"+client_hostname

		c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		c.connect((str(client_hostname), int(client_port)))

		c.send('HELLO from test!')

		hel = c.recv(BUFFER_SIZE)
		print hel

		tosend = "GET RFC "+str(rfc_no)+" P2P-CI/1.0"+"\n"+"Host: "+host_name+"\n"+"OS: Mac OS 10.4.1"

		c.sendall(tosend)

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
			client_rfcList.append(rfc_no)

			c.close()

		get_input()
	elif user_input == "EXIT":
		print "SHUTTING DOWN!"
	else:
		print "INVALID REQUEST! Try again ... \n"
		get_input()

get_input()

