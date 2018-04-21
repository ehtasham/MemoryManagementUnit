#!/usr/bin/python
import threading
from collections import deque
class virtualClock (threading.Thread):
   def __init__(self, threadID, threadName,processAllocationStart,processAllocationEnd):
      threading.Thread.__init__(self)
      self.threadID = threadID # Thread ID
      self.threadName = threadName # Thread Name
      self.processAllocationStart=processAllocationStart #start of Process Allocation
      self.processAllocationEnd=processAllocationEnd # end of Process Allocations
   def run(self):
      time_in_memory(self.threadName,1)
      remove_from_memory(self.processAllocationStart,self.processAllocationEnd)

def time_in_memory(threadName, delay):
	i=delay
	while(i<=100):
		i=i+1

non_processed_process=[]
def MMU(processNo,processMemorySize):
	countEmptyLocations=0 #counter to find empty locations is memory
	for i in range(0,memory_size): # Traverse whole memory
		if memory[i] is None: # check if location is empty
			if countEmptyLocations==0: #First Empty Locations
				emptyLocationsStart=i #Start of Empty Location
			countEmptyLocations=countEmptyLocations+1 #increment location counter
			if countEmptyLocations==processMemorySize: #block of process size is available
				endEmptyLocations=i #End of Empty Locations
				print "block available from location: " + str(emptyLocationsStart) + " to " + str(endEmptyLocations)
				processAllocationStart=emptyLocationsStart
				for x in range(emptyLocationsStart,endEmptyLocations+1):
					memory[emptyLocationsStart]=1 #inserting block into memory
					emptyLocationsStart=emptyLocationsStart+1 			
				thread = virtualClock(1, "Thread",processAllocationStart,endEmptyLocations) #Creating Thread for timer
				thread.start() #starting Thread
				break
		if (i==(memory_size-1) and (countEmptyLocations!=processMemorySize)):
			non_processed_process.append(processNo)
			print ("i is: "+str(i)+ "mem size is :" +str(memory_size-1)+ " "+ str(countEmptyLocations)+" space not available")

def remove_from_memory(processAllocationStart,processAllocationEnd):
	for i in range(0,400):
		memory[i]=None


memory_size=1000
# raw_input("Memory Size: ")
# mem_policy=raw_input("1-VSP,2-PAG,3-SEG: ")
# if (mem_policy == '1' or mem_policy == '3'):
# 	fitness_algo=raw_input("1-First Fit, 2-Best Fit: ")
# 	print("Fitness Algo: "+fitness_algo)
# elif(mem_policy=='2'):
# 	page_size=raw_input("Page/Frame Size: ")
# 	print("Page Size:"+page_size)
# else:
# 	print("Wrong Input")
# 	exit(1)
# print("Memory Policy: "+mem_policy)
# print("Memory Size: "+mem_size)
workLoadName="input1.txt"
# raw_input("WorkLoad File Name: ")

memory=[None] * memory_size

fo=open(workLoadName,"rw+")
totalProcesses=int(fo.read(1))

processNoLine=1
processNoLines=[]
processNos=[]

timeLines=[]
arrivalTimeLiness=[]
timeLinesLineNo=2	
lifeTimeLiness=[]

addressSpaceLineNo=3
addressSpace=[]
noOfChunks=[]
chunkSizes=[[]]


while(totalProcesses!=0):
	processNoLines.append(processNoLine)
	timeLines.append(timeLinesLineNo)
	addressSpace.append(addressSpaceLineNo)
	addressSpaceLineNo=addressSpaceLineNo+4
	timeLinesLineNo=timeLinesLineNo+4
	processNoLine=processNoLine+4
	totalProcesses=totalProcesses-1

chunk_info=[]
for i, line in enumerate(fo):
	if i in timeLines:
		new_line=line.split()
		arrivalTimeLiness.append(new_line[0])
		lifeTimeLiness.append(new_line[1])
	if i in processNoLines:
		processNos.append(line)
	if i in addressSpace:
		line=line.split()
		chunk_info.append(line)
fo.close()
processNosStripped=[]
for process in processNos:
	processNosStripped.append(process.strip())

#code to extrace chunk information
#chunkinfo[i][0]=noOfChunks
#loop through noOfChunks and extract their sizes
# for i in range(0,totalProcesses):
# 	print ("no of chunks in process no " , i, "are " , int(chunk_info[i][0]))
# 	for j in range(1,int(chunk_info[i][0])+1):
# 		print ("chunk size of process ",i, "are", chunk_info[i][j])

processNosStripped=map(int,processNosStripped)	
arrivalTimeLiness=map(int,arrivalTimeLiness)	
lifeTimeLiness=map(int,lifeTimeLiness)	

chunkInfoInt=[]
totalChunkSize=[]
for chunk in chunk_info:
	chunk=map(int,chunk)
	chunkInfoInt.append(chunk)
count=0
for chunk in chunkInfoInt:
	del	chunk[0]
	totalChunkSize.append(sum(chunk))

# print (processNosStripped)
# print (arrivalTimeLiness)
# print (lifeTimeLiness)
# print (totalChunkSize)

processNosStripped1=[1,2]
count=0
for p in processNosStripped1:
	current_process_arrival_time=arrivalTimeLiness[count]
	current_process_life_time=lifeTimeLiness[count]
	current_process_memory_size=totalChunkSize[count]
	MMU(p,current_process_memory_size)
	count=count+1






