# https://stackoverflow.com/questions/6153860/in-python-how-can-i-detect-whether-the-computer-is-on-battery-power #
# https://msdn.microsoft.com/en-us/library/windows/desktop/aa373232(v=vs.85).aspx
import ctypes
from ctypes import wintypes

class SYSTEM_POWER_STATUS(ctypes.Structure):
    _fields_ = [
        ('ACLineStatus', wintypes.BYTE),
        ('BatteryFlag', wintypes.BYTE),
        ('BatteryLifePercent', wintypes.BYTE),
        ('Reserved1', wintypes.BYTE),
        ('BatteryLifeTime', wintypes.DWORD),
        ('BatteryFullLifeTime', wintypes.DWORD),
    ]
class power_status:
	def __init__(self):
		self.GetSystemPowerStatus = ctypes.windll.kernel32.GetSystemPowerStatus
	def get_battery(self):
		self.status = SYSTEM_POWER_STATUS()
		if not self.GetSystemPowerStatus(ctypes.pointer(self.status)):
			raise ctypes.WinError()
		print('ACLineStatus', self.status.ACLineStatus)
		print('BatteryFlag', self.status.BatteryFlag)
		print('BatteryLifePercent', self.status.BatteryLifePercent)
		print('BatteryLifeTime', self.status.BatteryLifeTime)
		print('BatteryFullLifeTime', self.status.BatteryFullLifeTime)
		return self.status
