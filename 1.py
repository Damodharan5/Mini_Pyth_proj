####################################################################################
#Don't care filller.                                                               #
#                                                                                  #
####################################################################################
import sys

def filler(a):
	unfilled_list = list(a) 
	
	nx = a.count('x') #Number of don't care in the given binary string.
	
	filled_list = [] #List for final result
	loc_x = [x for x,v in enumerate(a) if v=='x']   #Getting the index of all occurrence of 'x'
	
	bin_list = [bin(i)[2:].zfill(nx) for i in range(0,2**nx)] #bin() - converts the int to binary. And zfill append zeros in front.
#Logic below is self-explanatory. 	
	for __item in bin_list:
		for i,v in enumerate(loc_x):
			unfilled_list[v] = __item[i]
		filled_list.append("".join(unfilled_list))
	return filled_list

if __name__ == '__main__':
		if len(sys.argv) >2:
			print("Need no or one argument.\nUsage: 1.py [-filename]")
		else:
			inp = input("Enter a binary number with dont care: ") # Input with x
			result = filler(inp)
			if len(sys.argv)==2:
				fp = open(sys.argv[1]+".dontcare","w")
				fp.write("Input given:\n"+inp+"\n\nOutput:\n")
				fp.write("\n".join(result))
			else:
				print(inp)
				print(result)