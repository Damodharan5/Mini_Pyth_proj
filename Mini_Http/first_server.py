#Site:
#	https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html
#	http://greenbytes.de/tech/webdav/rfc2616.html#media.types
#	http://www.binarytides.com/python-socket-programming-tutorial/
#Example sites to give as input for  this program
#	0.html - works fine
#	1.html - works fine
#	2.html - not working fine as it has image and gif
#problems:
#	Can't open image using normal 'open' command in python - 5/21/2017 solved on 5/22/2017
#	Problem with encoding different file - 5/22/2017 - Probably solved
#	Problem with mutliple usage of the server.. need multiprocessing or threading
#	POST not sending the form data from mobile big problem - 5/22/2017
#Accomplished
#	Send the http page over python socket	
#	Send the http page over two different network using college vpn(cisco anyconnect)	
#	Separate parser for get and post request. Now i can get dat from the site to this server program.
#Next version came - 5/22/2017 - check the file second_server.py
from socket import *
import os
a = input('Filename: ')

s = socket(AF_INET,SOCK_STREAM)
s.bind(('192.168.0.7',1234))
s.listen(10)
print('Waiting for the connection')
conn,addr = s.accept()
try:
	fp = open(a,'r',encoding="utf8")
except IOError:
	conn.send(b'HTTP/1.0 404 Not Found\nContent-Type: text/html\n\n')
	print('File not found')
	exit(0)
b = fp.read().encode() # encode is used to convert the str to byte for socket communication
#main html or root html load
print(conn.recv(2048).decode()) # decode is used to convert the byte  to str
conn.send(b'HTTP/1.1 200 OK\nContent-Type: text/html\n\n') #Always send the content-type
conn.send(b)
conn.close()
#other files linked in main/index/root html
while True:
	m = b''
	conn,addr = s.accept()
	g = conn.recv(2048).decode()
	print(g)
	n = g.split('\n')[0].split(' ')[1] #Gives the file name to open
	sendd = g.split('\n')[1:-2]   # Remaining HTTP header
	temp = []
	print(n)
	for i in sendd:
		temp.append(i.split(': '))
	temp = dict(temp) #Has a "Accept" header contains the file type such as type\html, application\xml etc,.
	conn.send(b'HTTP/1.1 200 OK\nContent-Type: '+temp['Accept'].split(',')[0].encode()+b'\n\n') # encode is used to convert the str to byte for socket communication
	#Always send the content-type
	try:
		fp1 = open(os.getcwd()+n,'r',encoding="utf8")
	except:
		print("no file")
	try:
		m = fp1.read().encode()
	except:
		print('Encounter a file>> '+n+'\n')
	conn.send(m)
	try:
		fp1.close()
	except:
		print()
	conn.close()
#Next version came - 5/22/2017 - check the file second_server.py
