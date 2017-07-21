#https://msdn.microsoft.com/en-us/library/windows/desktop/aa366770(v=vs.85).aspx #
import ctypes
from ctypes import wintypes

class MEMORYSTATUSEX(ctypes.Structure):
	_fields_ = [
		('dwLength',wintypes.DWORD),
		('dwMemoryLoad',wintypes.DWORD),
		('ullTotalPhys',ctypes.c_ulonglong),
		('ullAvailPhys',ctypes.c_ulonglong),
		('ullTotalPageFile',ctypes.c_ulonglong),
		('ullAvailPageFile',ctypes.c_ulonglong),
		('ullTotalVirtual',ctypes.c_ulonglong),
		('ullAvailVirtual',ctypes.c_ulonglong),
		('ullAvailExtendedVirtual',ctypes.c_ulonglong),
	]
	def __init__(self):
		# have to initialize this to the size of MEMORYSTATUSEX
		#check the site https://msdn.microsoft.com/en-us/library/windows/desktop/aa366770(v=vs.85).aspx    for dwLength description
		self.dwLength = ctypes.sizeof(self)
		super(MEMORYSTATUSEX, self).__init__()
	
class ram_usage:
	def __init__(self):
		self.getramusage = ctypes.windll.kernel32.GlobalMemoryStatusEx
	def get_ram_usage(self):
		self.status = MEMORYSTATUSEX()
		if not self.getramusage(ctypes.pointer(self.status)):
			raise ctypes.WinError()
		print('MEMORYSTATUSEX Structure: ',self.status.dwLength)
		print('percentage of physical memory: ',self.status.dwMemoryLoad)
		print('actual physical memory: ',self.status.ullTotalPhys)
		print('physical memory currently available: ',self.status.ullAvailPhys)
		print('Total Page file: ',self.status.ullTotalPageFile)
		print('Avail Page file: ',self.status.ullAvailPageFile)
		print('Total Virtual: ',self.status.ullTotalVirtual)
		print('Avail Virtual: ',self.status.ullAvailVirtual)
		print('Avail Extended Virtual: ',self.status.ullAvailExtendedVirtual)
		return self.status
