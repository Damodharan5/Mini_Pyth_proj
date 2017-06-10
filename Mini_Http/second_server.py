#Version 2:
#All problems and accomplishmet are in first_server.py

from socket import *
import os

def func_getorpost(msg):
	spl = msg.find('\n')
	get_list = msg[0:spl].split(' ')
	proc_msg = msg[spl+1:].split('\r\n')[:-2]
	the_dic = dict([i.split(': ') for i in proc_msg])
	return (get_list,the_dic)

user_dic = {}
file_ = input('Html page  to bind: ')
_server = socket(AF_INET,SOCK_STREAM)
print('Server IP: ' +gethostbyname(gethostname()) +',1234')
try:
	_server.bind((gethostbyname(gethostname()),1234))  # we can socket module to get the current ip address. port is default to 1234
except:
	print('Socket Error')
	sys.exit(-1)

_server.listen(10)
flag = True
while True:
	print()
	conn, addr = _server.accept()
	client_msg = conn.recv(4096).decode()
	print(client_msg)
	if 'GET' in client_msg:
		a_list,a_dic = func_getorpost(client_msg) # function to parse client_msg GET
		#print(a_list)
		#print(a_dic)
		#This try is for checking the presence files needed for the website
		try:
			if(a_list[1] == '/'):
				fp1 = open(os.getcwd()+a_list[1]+file_,'rb')
			else:
				fp1 = open(os.getcwd()+'/'+a_list[1],'rb')
		except IOError:
			print(a_list[1][:30]+'.... not found')
			fp1 = open(os.getcwd()+'\\temp','rb') # dont want to leave fp1 an empty thing
		# This try will check the encoding part
		try:
			msg_ = fp1.read()
		except:
			msg_=b''
			print('>>>>>Encode Fail<<<<<<')
		#This try will ensure the accept part in the a_dic ie in get message.
		try:
			conn.send(b'HTTP/1.1 200 OK\nContent-Type: '+a_dic['Accept'].split(',')[0].encode()+b'\n\n')
		#has a "Accept" header contains the file type such as type\html, application\xml etc,.
		except:
			conn.send(b'HTTP/1.0 404 Not Found\nContent-Type: text/plain\n\n')
			print("No accept part")
		conn.sendall(msg_)
		conn.close()
		fp1.close()
	elif 'POST' in client_msg:
		# Separate client_msg to get our msg
		our_msg = client_msg.split('\r\n\r\n')
		print(our_msg)
		if(our_msg[1]==''):
			print('No msg coming')
			conn.send(b'HTTP/1.1 200 OK\nContent-Type: text/html\n\n')		
		else:
			our_msg = our_msg[1].split('=')[1]
			print(our_msg)
			if flag:
				if our_msg in list(user_dic.keys()):
					conn.send(b'HTTP/1.1 200 OK\nContent-Type: text/html\n\n')
					conn.send(b'<html><body><p>Choose different username or u already login to the server using this ip address</p></body></html>')
					#conn.close()
				else:
					user_dic[our_msg] = addr[0]
					flag = False
				conn.send(b'HTTP/1.1 200 OK\nContent-Type: text/html\n\n')
				fp1 = open('4.html','rb')
				a = fp1.read()
				conn.send(a)
				#conn.close()	
				fp1.close()		
			else:
				conn.send(b'HTTP/1.1 200 OK\nContent-Type: text/html\n\n')
				fp1 = open('4.html','rb')
				a = fp1.read()
				conn.send(a)
				fp1.close()
				fp2 = open('post_output','a')
				fp2.write(our_msg+'\n')
				fp2.close()
		conn.close()	
			#print(user_dic)