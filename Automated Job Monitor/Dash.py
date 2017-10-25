
##############################################################---COMMENT SECTION---############################################################################
##############################################################---------------------############################################################################
"""

All LPARS Except AMP6 and DREADELP is added. Because it has different starting screen and different password than the others.. 
If anything goes wrong,(For Damo, logon to the system and cross check screens and codings start from LINE 102 till 207 using print statement and raw_input like I commented below few "prints statements" for debugging) others can close and reopen it or contact me or edit the codes if you know or understand or write your own script from scratch.

Below table is function key table. 
"""

"""
--$$--IMPORTANT POINT TO ADD IN THE PROCEDURE: CLOSE THE SCRIPT AFTER OR BEFORE PERFORMING THE IPL DURING WEEKLY BACKUP.. BECUASE ONCE THE ADR7 SYSTEM IS UP MY SCRIPT WILL OBVIOUSLY TRY TO LOG IN ADR7 WITH GUNA'S CREDENTIAL. BUT AFTER IPL, WE NEED TO LOG IN FIRST WITH THE SPECIAL CREDENTIALS TO START SOME 500 JOBS.--$$--

"""

"""

Need to add timeout in every command to so that if sys down in between it will reflect. - Added.. Need to Check
If wrong revert back to file ASP_need_check.py

"""

"""
FUNCTION KEY TABLE
F1 => '\x1bOP'
F2 => '\x1bOQ'
F3 => '\x1bOR'
F4 => '\x1bOS'
F5 => '\x1b[15~'
F6 => '\x1b[17~'
F7 => '\x1b[18~'
F8 => '\x1b[19~'
F9 => '\x1b[20~'
F10 => '\x1b[21~'
F11 => '\x1b[23~'
F12 => '\x1b[24~'
Up Arrow => '\x1b[A'
Down Arrow => '\x1b[B'
Page up => '\x1b[5~'
Page Down = '\x1b[6~'


"""
###############################################################################################################################################################
import getpass
import sys
import os
import time
import telnetlib
import subprocess
import threading
import socket
############################################################---LOOKUP TABLE INITIALIZATION---##################################################################
ASP_Table = {"ADR3":"","ADR8":"","ADR1":"","ADR4":"","ADR7":"","ADR2":"","RAMP10":"","AMP0":"","RAMP12":"","ABK1":"","ABX1":"","AMP5":"","ALH1":"","AMP4":"","AMP2":"","AMP3":"","AMP9":"","RAMP11":""}
prbdic = {"ADR3":"","ADR8":"","ADR1":"","ADR4":"","ADR7":"","ADR2":"","RAMP10":"","AMP0":"","RAMP12":"","ABK1":"","ABX1":"","AMP5":"","ALH1":"","AMP4":"","AMP2":"","AMP3":"","AMP9":"","RAMP11":""}
PRB_Table = {"ADR3":"","ADR8":"","ADR1":"","ADR4":"","ADR7":"","ADR2":"","RAMP10":"","AMP0":"","RAMP12":"","ABK1":"","ABX1":"","AMP5":"","ALH1":"","AMP4":"","AMP2":"","AMP3":"","AMP9":"","RAMP11":""}
chck_flag = 1
Q_Table = {"ADR3":"NOT HELD  ","ADR8":"NOT HELD  ","ADR1":"NOT HELD  ","ADR4":"NOT HELD  ","ADR7":"NOT HELD  ","ADR2":"NOT HELD  ","RAMP10":"NOT HELD  ","AMP0":"NOT HELD  ","RAMP12":"NOT HELD  ","ABK1":"NOT HELD  ","ABX1":"NOT HELD  ","AMP5":"NOT HELD  ","ALH1":"NOT HELD  ","AMP4":"NOT HELD  ","AMP2":"NOT HELD  ","AMP3":"NOT HELD  ","AMP9":"NOT HELD  ","RAMP11":"NOT HELD  "}
syssts = {"ADR3":"","ADR8":"","ADR1":"","ADR4":"","ADR7":"","ADR2":"","RAMP10":"","AMP0":"","RAMP12":"","ABK1":"","ABX1":"","AMP5":"","ALH1":"","AMP4":"","AMP2":"","AMP3":"","AMP9":"","RAMP11":""}
JOB_Table = {"ADR3":"", "ADR8":"", "ADR1":"","ADR4":"","ADR7":"","ADR2":"","RAMP10":"","AMP0":"","RAMP12":"","ABK1":"","ABX1":"","AMP5":"","ALH1":"","AMP4":"","AMP2":"","AMP3":"","AMP9":"","RAMP11":""}
COUNT_Table = {"ADR3":"", "ADR8":"", "ADR1":"","ADR4":"","ADR7":"","ADR2":"","RAMP10":"","AMP0":"","RAMP12":"","ABK1":"","ABX1":"","AMP5":"","AMP4":"","AMP2":"","AMP3":"","AMP9":"","RAMP11":""}
ID_Status = {}
B_ASP = {"ADR3":"", "ADR8":"", "ADR1":"","ADR4":"","ADR7":"","ADR2":"","RAMP10":"","AMP0":"","RAMP12":"","ABK1":"","ABX1":"","AMP5":"","AMP4":"","AMP2":"","AMP3":"","AMP9":"","RAMP11":""}
WAIT_List = ["MSGW","LCKW"]
_flag = 0
###############################################################################################################################################################
###################################################---FUNCTION TO CHECK SYSTEM STATUS---#######################################################################
class DevNull():
	def write(self,masg):
		pass

def updown_(hos):
	try:
		socket.setdefaulttimeout(2)
		s = socket.socket()
		s.connect((hos,23))
		s.close()
		return 0
	except Exception, e:
		sys.stderr = DevNull()
		return 1
###############################################################################################################################################################
#############################################################---GENERAL THREAD AS CLASS---#####################################################################
class listener(threading.Thread):
	output_lock = threading.Lock()
	def __init__(self,HOST):
		super(listener,self).__init__()
		self.host = HOST
		if HOST <> "Print":
			resp = updown_(self.host)
			if resp == 0:
				self.tn = telnetlib.Telnet(HOST)
			#time.sleep(1)
		else:
			#print "Printer enabled"
			print "Loading....."
			time.sleep(1)
	def run(self):
		global chck_flag
		global Q_Table
		global syssts
		global JOB_Table
		global prbdic
		global PRB_Table
		global f1
		global ID_Status
		global B_ASP
		global _flag
		while 1:
			response = updown_(self.host)
			if response == 0 or self.host == "Print":
				if self.host <> "Print":
					self.tn = telnetlib.Telnet(self.host)
					global ASP_Table
					self.tn.write('\n') 
					self.ss = self.tn.read_until("*",5)
					#print ss
					#raw_input()
					if self.ss == "":
						ASP_Table[self.host] = " " + (self.host).ljust(6)+"  "+ "    -      "+"  "+ "  -     "
						syssts[self.host]="DOWN"
						JOB_Table[self.host] = "          "
						PRB_Table[self.host] = "-"
						Q_Table[self.host] = "          "
						COUNT_Table[self.host] = str(0).rjust(2)
						self.tn.close()
						#print self.host
						time.sleep(60)
						pass
						#ASP_Table[self.host] = " " + (self.host).ljust(6)+"  "+ "    -      "+"  "+ "  -     "
						#syssts[self.host]="DOWN"
						#continue
					#raw_input()
					self.tn.write(user)
					self.tn.write('\t')
					self.tn.write(password)
					self.tn.write('\r')
					
					self.st_check = self.tn.read_until("started",5)
					if  ('CPF1107' in self.st_check):
						ID_Status[self.host] = "Password wrong for "+self.host+". Closing...."
						while 1:
							ASP_Table[self.host] = " " + (self.host).ljust(6)+"  "+ "    -      "+"  "+ "  -     "
							JOB_Table[self.host] = "          "
							PRB_Table[self.host] = "-"
							Q_Table[self.host] = "          "
							syssts[self.host]="    "
							COUNT_Table[self.host] = str(0).rjust(2)							
							time.sleep(600)
							pass
						#os._exit(1)
						#exit(0)
					elif ('CPF1394' in self.st_check):
						ID_Status[self.host] = "Already Locked "+self.host+". Closing...."
						while 1:
							ASP_Table[self.host] = " " + (self.host).ljust(6)+"  "+ "    -      "+"  "+ "  -     "
							JOB_Table[self.host] = "          "
							PRB_Table[self.host] = "-"
							Q_Table[self.host] = "          "
							syssts[self.host]="    "
							COUNT_Table[self.host] = str(0).rjust(2)							
							time.sleep(600)
							pass
						#os._exit(1)
						#exit(0)
					elif ('CPF1120' in self.st_check):
						ID_Status[self.host] = "Username invalid "+self.host+". Closing...."
						while 1:
							ASP_Table[self.host] = " " + (self.host).ljust(6)+"  "+ "    -      "+"  "+ "  -     "
							JOB_Table[self.host] = "          "
							PRB_Table[self.host] = "-"
							Q_Table[self.host] = "          "
							syssts[self.host]="    "
							COUNT_Table[self.host] = str(0).rjust(2)							
							time.sleep(600)
							pass
						#os._exit(1)
					if self.st_check <> "":
						self.tn.write('\r')
						self.tn.write('\r')
					if self.tn.read_until("started",10) <> "":
						self.tn.write('\r')
						self.tn.write('\r')
						#print self.tn.read_until("Set ")
					#raw_input()
					self.tn.write('\r')
#From here Re-write to get anything

					#raw_input()
					self.tn.read_until("                                                                                ",3)
					syssts[self.host] = "UP  "
					print self.host+" "+"Logged on"	
					while syssts["ADR1"] == "" or syssts["ADR8"] == "" or syssts["ADR3"]== "" or syssts["ADR4"] == "" or syssts["ADR7"] == "" or syssts["ADR2"]== "" or syssts["RAMP10"]=="" or syssts["AMP0"]=="" or syssts["RAMP12"]=="" or syssts["ABK1"]=="" or syssts["ABX1"]=="" or syssts["AMP5"]=="" or syssts["ALH1"]=="" or syssts["AMP4"]=="" or syssts["AMP2"]=="" or syssts["AMP3"]=="" or syssts["AMP9"]=="" or syssts["RAMP11"]=="":
						pass
					while 1:
						try:
							if self.tn.read_until('QSYSOPR',2) <> "":
								self.tn.write('\r\r')
							self.tn.write("dspsyssts")
							self.tn.write('\r')
							wn = self.tn.read_until("% temp addresses",3)
							self.tn.write("\r")
							self.tn.write("wrkjobq")
							self.tn.write("\r")
							dsp =  self.tn.read_until("=>",3)
							dsp =  self.tn.read_until("=>",3)
							while dsp.find("Bottom",6) == -1:
								if ("HLD " in dsp):# for x in lsts):
									f = dsp.find("HLD",3)
									Q_Table[self.host] = dsp[f-57:f-47]
									break
								else: 
									Q_Table[self.host] = "NOT HELD  "	
								self.tn.write('\x1b[6~')
								dsp =  self.tn.read_until("=>",3)
								#print dsp
								#raw_input("Enter")
							if ("HLD " in dsp ):#for x in lsts):
								f = dsp.find("HLD",3)
								Q_Table[self.host] = dsp[f-57:f-47]
							else: 
								Q_Table[self.host] = "NOT HELD  "
							self.tn.write("\x1bOR")	
							self.tn.read_until("=>",3)
							self.tn.write("wrkactjob sbs(qbatch)\r")
							jbs = self.tn.read_until("=>",3)
							JOB_Table[self.host] = "N         "
							count_j = 0
							while jbs.find("Bottom",6) == -1:
								#print jbs
								#raw_input("ENter")
								if any(x in jbs for x in WAIT_List):
									f = jbs.find("LCKW",4)
									if f <> -1:
										JOB_Table[self.host] = jbs[f-55:f-45]
									else:
										f = jbs.find("MSGW",4)
										if f <> -1:
											JOB_Table[self.host] = jbs[f-55:f-45]
								count_j = count_j + sum(jbs.count(xx) for xx in WAIT_List)		
								self.tn.write('\x1b[6~')
								jbs =  self.tn.read_until("=>",3)
							#print jbs
							if any(x in jbs for x in WAIT_List):
								f = jbs.find("LCKW",4)
								if f <> -1:
									JOB_Table[self.host] = jbs[f-55:f-45]
								else:
									f = jbs.find("MSGW",4)
									if f <> -1:
										JOB_Table[self.host] = jbs[f-55:f-45]
							count_j = count_j + sum(jbs.count(xx) for xx in WAIT_List)
							COUNT_Table[self.host] = str(count_j).rjust(2)							
							self.tn.write("\x1bOR")
							self.tn.read_until("=>",3)
							self.tn.write("wrkprb\r")
							self.tn.write("\x1b[23~")
							prbs = self.tn.read_until("F12=",3)
							prbs = self.tn.read_until("F12=",3)
							prbs = self.tn.read_until("F12=",3)
							#print prbs
							#raw_input()
							p = prbs.find(time.strftime("%m/%d/%y"),8)
							if p <> -1:
								pp = prbs[p-12:p-2]
								self.tn.write("\x1b[23~")
								prbs = self.tn.read_until("F12=",3)
								self.tn.write("\x1b[23~")
								prbs = self.tn.read_until("F12=",3)
								p = prbs.find(pp,10)
								prbdic[self.host] = prbs[p:p+70]
								PRB_Table[self.host] = "Y"
							else:
								PRB_Table[self.host] = "N"
								prbdic[self.host] = "No Recent Problems"
							f = wn.find("% system ASP used",15)
							t = wn.find(time.strftime("%m/%d/%y"),8)
							ASP_Table[self.host] = " "+(self.host).ljust(6) + "   " +wn[f+26:f+35]+"   "+wn[t+10:t+18]
							#print self.host
							#temp_ = B_ASP[self.host]
							#print B_ASP[self.host][22:29]
							if int(wn[f+28]) >= 9 and wn[f+28:f+35] <> B_ASP[self.host][22:29]:
								B_ASP[self.host] = "ASP Peak -"+ASP_Table[self.host]+"\n"
								#print B_ASP
							else:
								B_ASP[self.host] = ""
								#print wn[f+28:f+34]
								#print temp_[12:18]
							time.sleep(60)
							self.tn.write("\x1bOR")
							d = self.tn.read_until("=>",3)
							if d == "" or ("Password" in d):
								ASP_Table[self.host] = " " + (self.host).ljust(6)+"  "+ "    -      "+"  "+ "  -     "
								JOB_Table[self.host] = "          "
								PRB_Table[self.host] = "-"
								Q_Table[self.host] = "          "
								syssts[self.host]="DOWN"
								COUNT_Table[self.host] = str(0).rjust(2)							
								self.tn.close()
								break
							#syssts[self.host] = "UP  "
							response = updown_(self.host)
							if response <> 0:
								ASP_Table[self.host] = " " + (self.host).ljust(6)+"  "+ "    -      "+"  "+ "  -     "
								JOB_Table[self.host] = "          "
								PRB_Table[self.host] = "-"
								Q_Table[self.host] = "          "
								syssts[self.host]="DOWN"
								COUNT_Table[self.host] = str(0).rjust(2)							
								break
						except 	socket.timeout:
							sys.stderr = DevNull()
							#print e
							break
#To this Re-write to get anything
				else:
					while 1:
						if ASP_Table["ADR1"] == "" or ASP_Table["ADR8"] == "" or ASP_Table["ADR3"]== "" or ASP_Table["ADR4"] == "" or ASP_Table["ADR7"] == "" or ASP_Table["ADR2"]== "" or ASP_Table["RAMP10"]=="" or ASP_Table["AMP0"]=="" or ASP_Table["RAMP12"]=="" or ASP_Table["ABK1"]=="" or ASP_Table["ABX1"]=="" or ASP_Table["AMP5"]=="" or ASP_Table["ALH1"]=="" or ASP_Table["AMP4"]=="" or ASP_Table["AMP2"]=="" or ASP_Table["AMP3"]=="" or ASP_Table["AMP9"]=="" or ASP_Table["RAMP11"]=="":
							while ASP_Table["ADR1"] == "" or ASP_Table["ADR8"] == "" or ASP_Table["ADR3"]== "" or ASP_Table["ADR4"] == "" or ASP_Table["ADR7"] == "" or ASP_Table["ADR2"]== "" or ASP_Table["RAMP10"]=="" or ASP_Table["AMP0"]=="" or ASP_Table["RAMP12"]=="" or ASP_Table["ABK1"]=="" or ASP_Table["ABX1"]=="" or ASP_Table["AMP5"]=="" or ASP_Table["ALH1"]=="" or ASP_Table["AMP4"]=="" or ASP_Table["AMP2"]=="" or ASP_Table["AMP3"]=="" or ASP_Table["AMP9"]=="" or ASP_Table["RAMP11"]=="":
								pass
						#time.sleep(120)		
						os.system('cls')
						print("Refreshing....")
						print ("System   % ASP Used   Time      Jobqs     Online MSGW/LCKW        Problems")
						print "\nProd"
						print ASP_Table["ADR4"] + "  " +Q_Table["ADR4"] + "  " + syssts["ADR4"] + "  " + JOB_Table["ADR4"]+ "("+ COUNT_Table["ADR4"]+")" +"  " + PRB_Table["ADR4"]
						print ASP_Table["ADR7"] + "  " +Q_Table["ADR7"] + "  " + syssts["ADR7"] + "  " + JOB_Table["ADR7"]+ "("+ COUNT_Table["ADR7"]+")" +"  " + PRB_Table["ADR7"]
						print ASP_Table["ADR2"] + "  " +Q_Table["ADR2"] + "  " + syssts["ADR2"] + "  " + JOB_Table["ADR2"]+ "("+ COUNT_Table["ADR2"]+")" +"  " + PRB_Table["ADR2"]
						print ASP_Table["RAMP10"] + "  " +Q_Table["RAMP10"] + "  " + syssts["RAMP10"] + "  " + JOB_Table["RAMP10"]+ "("+ COUNT_Table["RAMP10"]+")" +"  " + PRB_Table["RAMP10"]
						print ASP_Table["ABK1"] + "  " +Q_Table["ABK1"] + "  " + syssts["ABK1"] + "  " + JOB_Table["ABK1"]+ "("+ COUNT_Table["ABK1"]+")" +"  " + PRB_Table["ABK1"]
						print ASP_Table["ABX1"] + "  " +Q_Table["ABX1"] + "  " + syssts["ABX1"] + "  " + JOB_Table["ABX1"]+ "("+ COUNT_Table["ABX1"]+")" +"  " + PRB_Table["ABX1"]
						print "\nNon Prod"
						print ASP_Table["ADR1"] + "  " +Q_Table["ADR1"] + "  " + syssts["ADR1"] + "  " + JOB_Table["ADR1"]+ "("+ COUNT_Table["ADR1"]+")" +"  " + PRB_Table["ADR1"]
						print ASP_Table["ADR8"] + "  " +Q_Table["ADR8"] + "  " + syssts["ADR8"] + "  " + JOB_Table["ADR8"]+ "("+ COUNT_Table["ADR8"]+")" +"  " + PRB_Table["ADR8"]
						print ASP_Table["ADR3"] + "  " +Q_Table["ADR3"] + "  " + syssts["ADR3"] + "  " + JOB_Table["ADR3"]+ "("+ COUNT_Table["ADR3"]+")" +"  " + PRB_Table["ADR3"]
						print ASP_Table["AMP0"] + "  " +Q_Table["AMP0"] + "  " + syssts["AMP0"] + "  " + JOB_Table["AMP0"]+ "("+ COUNT_Table["AMP0"]+")" +"  " + PRB_Table["AMP0"]
						print ASP_Table["RAMP12"] + "  " +Q_Table["RAMP12"] + "  " + syssts["RAMP12"] + "  " + JOB_Table["RAMP12"]+ "("+ COUNT_Table["RAMP12"]+")" +"  " + PRB_Table["RAMP12"]
						print ASP_Table["AMP5"] + "  " +Q_Table["AMP5"] + "  " + syssts["AMP5"] + "  " + JOB_Table["AMP5"]+ "("+ COUNT_Table["AMP5"]+")" +"  " + PRB_Table["AMP5"]
						#print ASP_Table["ALH1"] + "  " +Q_Table["ALH1"] + "  " + syssts["ALH1"] + "  " + JOB_Table["ALH1"]+ "  " + PRB_Table["ALH1"]
						print ASP_Table["AMP4"] + "  " +Q_Table["AMP4"] + "  " + syssts["AMP4"] + "  " + JOB_Table["AMP4"]+ "("+ COUNT_Table["AMP4"]+")" +"  " + PRB_Table["AMP4"]
						print ASP_Table["AMP2"] + "  " +Q_Table["AMP2"] + "  " + syssts["AMP2"] + "  " + JOB_Table["AMP2"]+ "("+ COUNT_Table["AMP2"]+")" +"  " + PRB_Table["AMP2"]
						print ASP_Table["AMP3"] + "  " +Q_Table["AMP3"] + "  " + syssts["AMP3"] + "  " + JOB_Table["AMP3"]+ "("+ COUNT_Table["AMP3"]+")" +"  " + PRB_Table["AMP3"]
						print ASP_Table["AMP9"] + "  " +Q_Table["AMP9"] + "  " + syssts["AMP9"] + "  " + JOB_Table["AMP9"]+ "("+ COUNT_Table["AMP9"]+")" +"  " + PRB_Table["AMP9"]
						print ASP_Table["RAMP11"] + "  " +Q_Table["RAMP11"] + "  " + syssts["RAMP11"] + "  " + JOB_Table["RAMP11"]+ "("+ COUNT_Table["RAMP11"]+")" +"  " + PRB_Table["RAMP11"]
						if chck_flag == 1:
							f1 = open("//walgreens/corp/mtp/itops/TCS - AS400/Damo/LOGs/"+time.strftime("%m-%d-%y.txt"),"a") #LOG FILE
							f1.writelines(time_)
							f1.writelines("\nUsername used is " + user)
							f1.writelines("\n{}\n".format(v) for k,v in ID_Status.iteritems())
							f1.close()
							chck_flag = ""
						f1 = open("//walgreens/corp/mtp/itops/TCS - AS400/Damo/LOGs/"+time.strftime("%m-%d-%y.txt"),"a")
						for k,v in B_ASP.iteritems():
							if v <> "":
								f1.writelines(v)
						f1.close()
						if _flag <> 1:
							directo = "//walgreens/corp/mtp/ITOPS/TCS - AS400/weekly health check/"+time.strftime("%Y")+"/"
# Edit this for Location

							if not os.path.exists(directo):
								os.makedirs(directo)
							directo = "//walgreens/corp/mtp/ITOPS/TCS - AS400/weekly health check/"+time.strftime("%Y")+"/"+time.strftime("%B")+"/"
							if not os.path.exists(directo):
								os.makedirs(directo)
							directo = directo+time.strftime("%m-%d-%y %I %p.txt")
							f = open(directo,"w")
							f.writelines("File saved in "+directo + "\n")
							f.writelines("\n% system ASP Used\n-----------------\n")
							f.writelines("System   % ASP Used   Time\n")
							di = ASP_Table
							f.writelines("{}\n".format(v) for k,v in di.iteritems())
							f.writelines("\n\nStatus of the Job Queues\n------------------------\n")
							f.writelines("System    Status\n")
							f.writelines("{}      {}\n".format(k.ljust(6),v) for k,v in Q_Table.iteritems())
							f.writelines("\n\nWork With Problems Status\n--------------------------\n")
							f.writelines("{}      {}\n".format(k.ljust(6),v) for k,v in prbdic.iteritems())
							f.close()
							a =os.system('Notepad' + directo)
							_flag =  1		
						if chck_flag <> time.strftime("%H") and (time.strftime("%H") in ["12","06","00","18"]):
							directo = "//walgreens/corp/mtp/ITOPS/TCS - AS400/weekly health check/"+time.strftime("%Y")+"/"
# Edit this for Location

							if not os.path.exists(directo):
								os.makedirs(directo)
							directo = "//walgreens/corp/mtp/ITOPS/TCS - AS400/weekly health check/"+time.strftime("%Y")+"/"+time.strftime("%B")+"/"
							if not os.path.exists(directo):
								os.makedirs(directo)
							directo = directo+time.strftime("%m-%d-%y %I %p.txt")
							f = open(directo,"w")
							f.writelines("File saved in "+directo + "\n")
							f.writelines("\n% system ASP Used\n-----------------\n")
							f.writelines("System   % ASP Used   Time\n")
							di = ASP_Table
							f.writelines("{}\n".format(v) for k,v in di.iteritems())
							f.writelines("\n\nStatus of the Job Queues\n------------------------\n")
							f.writelines("System    Status\n")
							f.writelines("{}      {}\n".format(k.ljust(6),v) for k,v in Q_Table.iteritems())
							f.writelines("\n\nWork With Problems Status\n--------------------------\n")
							f.writelines("{}      {}\n".format(k.ljust(6),v) for k,v in prbdic.iteritems())
							f.close()
							a =os.system('Notepad' + directo)
							chck_flag =  time.strftime("%H")
						time.sleep(30)	
			else:
				syssts[self.host] = "DOWN"
				ASP_Table[self.host] = " " + (self.host).ljust(6)+"  "+ "    -      "+"  "+ "  -     "
				JOB_Table[self.host] = "          "
				PRB_Table[self.host] = "-"
				Q_Table[self.host] = "          "
				COUNT_Table[self.host] = str(0).rjust(2)							
				#print ASP_Table          # Check herwe too
				time.sleep(60)
############################################################################################################################################################################################################################---START OF THE MAIN MODULE---####################################################################

if __name__ == "__main__":
	os.system('Title Consolidated Dashboard - AS/400')
	user = raw_input("USER: ")
	os.system('cls')
	print("ID: "+user.upper())
	password = getpass.getpass()
	user_ = os.environ.get("USERNAME")
	time_ = "Started the script at " + time.strftime("%c") + " in the VDI - " + user_
	Systems =  ["Print","ADR2","ADR7","ADR4","ABK1","ABX1","RAMP10","ADR3","ADR8","ADR1","AMP0","RAMP12","AMP5","ALH1","AMP4","AMP2","AMP3","AMP9","RAMP11"]
	thread_holder = []
	for H in Systems:
		thread_holder.append(listener(H))
	for thread in thread_holder:
		thread.start()
	#print thread_holder	
###############################################################################################################################################################
