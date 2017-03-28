############
#   ------  a
#  |      |
#  | b    | c
#  |      |
#   ------  d
#  |      |
#  | e    | f
#  |      |
#   ------   g
#
#
#Seven segment display is made up of 7 segments such a a,b,c,d,e,f,g. Illuminating the segments in a way will produce a character of our choice.
#For example, to print number 6 we need to highlight the line a,b,e,g,f,d. The pattern is abcdefg=>1101111
#######
try:
	from Tkinter import *
	print("Python 2.x - Seven Segment Display")
except ImportError:
	from tkinter import *
	print("Python 3.x - Seven Segment Display")
class sevenseg:
	def __init__(self,root,n,x,y):
		self.root = root
		self.delay = 1000																   #Delay for custom animation if any
		self.colo_dic = {'0':"",'1':"red"}                                                 #On/Off state of the segment line
		self.l_segments = []
		self.data = []
		self.n = n
		i = 0
		while i<n:
			self.w = Canvas(root, width=x+60, height=y+120)
			self.w.create_line(x+10, y+10, x+60, y+10,fill=self.colo_dic['0'],width=5)	#a
			self.w.create_line(x+10, y+10, x+10, y+60,fill=self.colo_dic['0'],width=5)	#b
			self.w.create_line(x+60, y+10, x+60, y+60,fill=self.colo_dic['0'],width=5)	#c
			self.w.create_line(x+10, y+60, x+60, y+60,fill=self.colo_dic['0'],width=5)	#d
			self.w.create_line(x+10, y+60, x+10, y+110,fill=self.colo_dic['0'],width=5)	#e
			self.w.create_line(x+60, y+60, x+60, y+110,fill=self.colo_dic['0'],width=5)	#f
			self.w.create_line(x+10, y+110, x+60, y+110,fill=self.colo_dic['0'],width=5)#g
			self.w.grid(row = 0, column=i)
			self.l_segments.append([self.w,self.data])											#List of seven segments and its data to show
			i+=1
	def __changestate__(self,x,id=0):
		for index,i in enumerate(self.l_segments[id][0].find_all()):
			self.l_segments[id][0].itemconfig(i,fill=self.colo_dic[x[index]])					#Change the On/Off state of the display based on id
#here comes custom function - Change accordingly to your purposes
	def __animate__(self,id=0,i=0,j=0):															# This custom function is for counting up to 59 then resetting to 00 and again couting up
		if i < len(self.l_segments[id][1]):
			self.__changestate__(self.l_segments[id][1][i],id)
			self.root.after(1000,self.__animate__,id,i+1,j)
		elif j >=5:
			self.__changestate__(self.l_segments[0][1][0],0)
			self.__changestate__(self.l_segments[1][1][0],1)
			self.root.after(0,self.__animate__,1,0,0)
		else:
			self.__changestate__(self.l_segments[id][1][0],id)
			self.__changestate__(self.l_segments[id-1][1][j+1],id-1)
			self.root.after(0,self.__animate__,1,0,j+1)
if __name__ == '__main__':
	root = Tk()
	root.geometry('320x240')
	root.resizable(width=False, height=False)
	a = sevenseg(root,2,10,10)						# the parameter 2 indicates two instances of seven segment display is going to be there
	a.l_segments[0][1] =['1110111','0010010','1011101','1011011','0111010','1101011','1101111','1010010','1111111','1111011'] #Loading the data for inst. 0
	a.l_segments[1][1] =['1110111','0010010','1011101','1011011','0111010','1101011','1101111','1010010','1111111','1111011'] #Lodaing the data for inst. 1
	a.__animate__(1,0,0)
	mainloop()
