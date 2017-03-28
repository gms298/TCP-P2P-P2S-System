import csv
import thread
import socket

filename = "text.txt"
results = ""
writefile = open("newtext.txt", "w")

with open('text.txt') as readfile:
	for line in readfile:
		results = str(line.strip().split('\n')[0])

		#write to file 
		writefile.write(results)
		writefile.write('\n')

writefile.close() 		

#DO over a connection and then over the whole thing  