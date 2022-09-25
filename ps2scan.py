import os
import sys
import struct

def mask_create(str) :
	mask = [[], []]
	
	if (str[:2] != "0x" or len(str) != 10) :
		print("wrong mask value '" + str + "'")
		exit(-1)
		
	for i in range(4) :
		value = str[2 + (i * 2):4 + (i * 2)].lower()
		
		if (value != "xx") :
			mask[0].append(int(value, 16))
			mask[1].append(0)
		else :
			mask[0].append(0)
			mask[1].append(1)
			
	mask[0].reverse()
	mask[1].reverse()
	
	return mask
	
def main() :
	#banner
	print("\nps2scan v0.23\n")
	
	# data
	file = None
	buffer = None
	fMask = [[], []]
	rMask = [[], []]
	numPatch = 0
	
	# check arguments
	if (len(sys.argv) < 4) :
		print("usage: python ps2scan.py [filepath] [find mask] [replace mask]\n")
		return
		
	# load file into buffer
	file = open(sys.argv[1], "rb")
	buffer = file.read()
	file.close()
	
	# create find and replace mask (BE)
	fMask = mask_create(sys.argv[2])
	rMask = mask_create(sys.argv[3])
	
	# open file for write patches
	file = open(sys.argv[1] + ".txt", "w")
	
	# process now
	for i in range(len(buffer) // 4) :
		offset = i * 4
		numOverlap = 0
		
		# find mask
		
		if (fMask[1][0] == 1 or buffer[offset] == fMask[0][0]) :
			numOverlap += 1
			
		if (fMask[1][1] == 1 or buffer[offset + 1] == fMask[0][1]) :
			numOverlap += 1
			
		if (fMask[1][2] == 1 or buffer[offset + 2] == fMask[0][2]) :
			numOverlap += 1
			
		if (fMask[1][3] == 1 or buffer[offset + 3] == fMask[0][3]) :
			numOverlap += 1
		
		# all 4 bytes is same or mask
		if (numOverlap == 4) :
			patchStr = "patch=1,EE," + '2{:07x}'.format(offset) + ",word,"
			
			# reversed order replace mask (LE)
			
			if (rMask[1][3] == 1) :
				patchStr += format(buffer[offset + 3], "02x")
			else :
				patchStr += format(rMask[0][3], "02x")
				
			if (rMask[1][2] == 1) :
				patchStr += format(buffer[offset + 2], "02x")
			else :
				patchStr += format(rMask[0][2], "02x")
				
			if (rMask[1][1] == 1) :
				patchStr += format(buffer[offset + 1], "02x")
			else :
				patchStr += format(rMask[0][1], "02x")
				
			if (rMask[1][0] == 1) :
				patchStr += format(buffer[offset], "02x")
			else :
				patchStr += format(rMask[0][0], "02x")
				
			# write original value (LE)
			
			hexValue = format(buffer[offset + 3], "02x")
			hexValue += format(buffer[offset + 2], "02x")
			hexValue += format(buffer[offset + 1], "02x")
			hexValue += format(buffer[offset], "02x")
			#intValue = int(hexValue, 16)
			#floatValue = struct.unpack('f', struct.pack('i', intValue))[0]
			
			patchStr += " // " + hexValue
			
			# write patch
			numPatch += 1
			
			print(str(numPatch) + " : " + patchStr)
			file.write(patchStr + "\n")
			
	print("patches: " + str(numPatch) + " / " + str(len(buffer) // 4))
	
	file.close()
	
	return

if __name__=="__main__":
	main()
