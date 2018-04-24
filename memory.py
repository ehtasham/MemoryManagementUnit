#!/usr/bin/python
import threading
import time

class lifeTimeThread(threading.Thread):
   	def __init__(self, threadID, name,lifeTime,processNo,processAllocationStart,processAllocationEnd):
   		threading.Thread.__init__(self)
   		self.threadID = threadID
   		self.name = name
   		self.lifeTime=lifeTime
   		self.processNo=processNo
   		self.processAllocationStart=processAllocationStart
   		self.processAllocationEnd=processAllocationEnd
   	def run(self):
   		self.timeInMemory(self.lifeTime,self.processNo)
   		self.removeFromMemory(self.processAllocationStart,self.processAllocationEnd,self.processNo)

	def timeInMemory(self,lifeTime,processNo):
   		print("process No: "+str(processNo)+" time start")
   		while(lifeTime!=0):
			lifeTime=lifeTime-1
		print("process No: "+str(processNo)+" time end")
		return lifeTime

	def removeFromMemory(self,processAllocationStart,processAllocationEnd,processNo):
   		for i in range(processAllocationStart,processAllocationEnd+1):
			memory[i]=None
		print("process No: "+str(processNo)+" removed From Memory")

class myThread(threading.Thread):
	def __init__(self, threadID, name, timeCounter):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.timeCounter = timeCounter
	def run(self):
		self.clock()

   	def clock(self):
   		while True:
			self.timeCounter += 1

	def timePassed(self):
		return self.timeCounter

nonProcessedProcesses=[]
def MMU(processNo,processMemorySize,lifeTime,memoryPolicy,fitnessAlgo):
	emptyLocationsStart=None
	countEmptyLocations=0 #counter to find empty locations is memory
	if (memoryPolicy==1 and fitnessAlgo==1):
		for i in range(0,memory_size): # Traverse whole memory
			if memory[i] is None: # check if location is empty
				if countEmptyLocations==0: #First Empty Locations
					emptyLocationsStart=i #Start of Empty Location
				countEmptyLocations=countEmptyLocations+1 #increment location counter
				if countEmptyLocations==processMemorySize: #block of process size is available
					endEmptyLocations=i #End of Empty Locations
					print "block available from location: " + str(emptyLocationsStart) + " to " + str(endEmptyLocations)
					processAllocationStart=emptyLocationsStart
					processAllocationEnd=endEmptyLocations
					for x in range(processAllocationStart,processAllocationEnd+1):
						memory[x]=1 #inserting block into memory
					print("process No: "+ str(processNo) + " Allocated space from "+str(processAllocationStart)+" to "+str(processAllocationEnd))			
					threadLifeTime = lifeTimeThread(1, "Thread-2",lifeTime,processNo,processAllocationStart,processAllocationEnd)
					threadLifeTime.daemon = True
					threadLifeTime.start()
					break
			if (i==(memory_size-1) and (countEmptyLocations!=processMemorySize)):
				nonProcessedProcesses.append(processNo)
				print ("Empty Locations: "+str(countEmptyLocations)+", space not available")



memory_size=1000

# raw_input("Memory Size: ")
# memoryPolicy=raw_input("1-VSP,2-PAG,3-SEG: ")
memoryPolicy=1
fitnessAlgo=1
# if (memoryPolicy == '1' or memoryPolicy == '3'):
# 	fitnessAlgo=raw_input("1-First Fit, 2-Best Fit: ")
# 	print("Fitness Algo: "+fitnessAlgo)
# elif(memoryPolicy=='2'):
# 	pageSize=raw_input("Page/Frame Size: ")
# 	print("Page Size:"+pageSize)
# else:
# 	print("Wrong Input")
# 	exit(1)
# print("Memory Policy: "+memoryPolicy)
# print("Memory Size: "+mem_size)
workLoadName="input1.txt"
# # raw_input("WorkLoad File Name: ")

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
thread = myThread(1, "Thread-1", 1)
thread.daemon = True
processNosStripped1=[1,2,3,4,5,6,7,8]

count=0
for p in processNosStripped1:
	currentProcessArrivalTime=arrivalTimeLiness[count]
	currentProcessLifeTime=lifeTimeLiness[count]
	currentProcessMemorySize=totalChunkSize[count]
	if p==1:
		thread.start()
	# time.sleep(0.000001)
	currentTime=thread.timePassed()
	print ("Time is "+str(currentTime))
	if currentTime > currentProcessArrivalTime:
		# print("process No: "+str(p)+" arrived")
		MMU(p,currentProcessMemorySize,currentProcessLifeTime,memoryPolicy,fitnessAlgo)
	else:
		nonProcessedProcesses.append(p)
	count=count+1
# timer=thread.timePassed()
# print ("End Time is "+str(timer))
print("non processed processes are: ",nonProcessedProcesses)






