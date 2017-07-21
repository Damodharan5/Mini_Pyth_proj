#Use putty or any terminal to see the result across the local network.
#Sent my laptop battery and available ram status thru local network.
#need to improve the interface on the client end.
from socket import *
from battery import *
from ram_usage import *
import os

_server = socket(AF_INET,SOCK_STREAM)
print('Server IP: 192.168.1.72' +',1234') #Replace the address of your system.
try:
	_server.bind(('192.168.1.72',1234))  # we can socket module to get the current ip address. port is default to 1234
except:
	print('Socket Error')
	sys.exit(-1)

_server.listen(10)
while True:
	conn, addr = _server.accept()
	a = power_status()
	b = a.get_battery()
	a = ram_usage()
	conn.sendall(b'Battery: '+str(b.BatteryLifePercent).encode()+b' %\r\n')
	b = a.get_ram_usage()
	conn.sendall(b'Available Ram: '+str(b.ullAvailPhys/1024/1024/1024).encode()+b' GB\r\n')
	
