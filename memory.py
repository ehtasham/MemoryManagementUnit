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
		if(type(processAllocationStart)==list and type(processAllocationEnd)==list):
			locIndex=0
			for start in processAllocationStart:
				for i in range(start,processAllocationEnd[locIndex]):
					memory[i]=None
				locIndex+=1
		else:
	   		for i in range(processAllocationStart,processAllocationEnd):
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
emptyBlocks=[]
emptyBlocksStart=[]
emptyBlocksEnd=[]
pages=[]
pageStart=[]
pageEnd=[]
segmentStart=[]
segmentEnd=[]
availableSegmentsStart=[]
availableSegmentsEnd=[]
availableSegmentSize=[]
def MMU(processNo,processMemorySize,lifeTime,segments,memoryPolicy,fitnessAlgo):
	spaceAvailable=False
	startEmptyLocations=0
	endEmptyLocations=0
	countEmptyLocations=0 #counter to find empty locations is memory
	if (memoryPolicy==1 and fitnessAlgo==1):
		for i in range(0,memory_size): # Traverse whole memory
			if memory[i] is None: # check if location is empty
				if countEmptyLocations==0: #First Empty Locations
					startEmptyLocations=i #Start of Empty Location
				countEmptyLocations=countEmptyLocations+1 #increment location counter
				if countEmptyLocations==processMemorySize: #block of process size is available
					endEmptyLocations=i #End of Empty Locations
					# print("block available from location: " + str(startEmptyLocations) + " to " + 
					# str(endEmptyLocations))
					processAllocationStart=startEmptyLocations
					processAllocationEnd=endEmptyLocations
					for x in range(processAllocationStart,processAllocationEnd+1):
						memory[x]=1 #inserting block into memory
					print("process No: "+ str(processNo) + " Allocated space from "+
						str(processAllocationStart)+" to "+str(processAllocationEnd))			
					threadLifeTime = lifeTimeThread(1, "Thread-2",lifeTime,processNo,
						processAllocationStart,processAllocationEnd)
					threadLifeTime.daemon = True
					threadLifeTime.start()
					break
			if (i==(memory_size-1) and (countEmptyLocations!=processMemorySize)):
				nonProcessedProcesses.append(processNo)
				print("process No: "+str(processNo)+" space not available")
	elif(memoryPolicy==1 and fitnessAlgo==2):
		# print("processing processNo: "+str(processNo))
		for i in range(0,memory_size):
			if memory[i] is None:
				if countEmptyLocations==0:
					startEmptyLocations=i	
				countEmptyLocations+=1
			else:
				endEmptyLocations=i
				if countEmptyLocations >= processMemorySize:
					emptyBlocksStart.append(startEmptyLocations)
					emptyBlocksEnd.append(endEmptyLocations)
					blockSize=endEmptyLocations-startEmptyLocations
					emptyBlocks.append(blockSize)
					# print("block of size "+ str(blockSize)+" available from location: " + 
					# str(startEmptyLocations) + " to " + str(endEmptyLocations))
				countEmptyLocations=0
			if(i==(memory_size-1)):
				endEmptyLocations=i
				if  countEmptyLocations>=processMemorySize:
					emptyBlocksStart.append(startEmptyLocations)
					emptyBlocksEnd.append(endEmptyLocations)
					blockSize=endEmptyLocations-startEmptyLocations
					emptyBlocks.append(blockSize)
					# print("block of size "+ str(blockSize)+" available from location: " + 
					# str(startEmptyLocations) + " to " + str(endEmptyLocations))
				countEmptyLocations=0
		if len(emptyBlocks)!=0:
			smallestBlockSize=emptyBlocks.index(min(emptyBlocks))
			processAllocationStart=emptyBlocksStart[smallestBlockSize]
			# processAllocationEnd=emptyBlocksEnd[smallestBlockSize]
			processAllocationEnd=processAllocationStart+processMemorySize
			for x in range(processAllocationStart,processAllocationStart+processMemorySize):
				memory[x]=1
			print("process No: "+ str(processNo) + " Allocated space from "+str(processAllocationStart)+" to "+str(processAllocationEnd))
			threadLifeTime = lifeTimeThread(1, "Thread-2",lifeTime,processNo,processAllocationStart,
				processAllocationEnd)
			threadLifeTime.daemon = True
			threadLifeTime.start()	
		else:
			print("process No: "+str(processNo)+" space not available")
			nonProcessedProcesses.append(processNo)
	elif(memoryPolicy==2):
		NoOfPages=processMemorySize/pageSize
		remainderProcessMemory=processMemorySize%pageSize
		pages=[pageSize]*NoOfPages
		if remainderProcessMemory !=0: pages.append(remainderProcessMemory)
		# print("paging: "+str(pageSize)+" "+str(NoOfPages))
		# print pages
		for location in range(0,memory_size):
			if memory[location] is None:
				if countEmptyLocations==0:
					startEmptyLocations=location
				countEmptyLocations+=1
				if countEmptyLocations==processMemorySize:
					endEmptyLocations=location
					spaceAvailable=True
					# print("space: "+ str(processMemorySize)+" Available for proces: "+
					# str(processNo)+ 
						# " from "+ str(startEmptyLocations)+ " to "+ str(endEmptyLocations))
					countEmptyLocations=0
					startEmptyLocations=0
					endEmptyLocations=0
					break
				else:
					spaceAvailable=False
		if spaceAvailable==True:
			for page in pages:
				for loc in range(0,memory_size):
					if memory[loc] is None:
						if countEmptyLocations==0:
							startEmptyLocations=loc	
						countEmptyLocations+=1
						if countEmptyLocations==page:
							endEmptyLocations=loc
							# print("process: "+str(processNo)+" page size available from: "
							# 	+str(startEmptyLocations)+" to "+str(endEmptyLocations))
							pageAllocationStart=startEmptyLocations
							pageAllocationEnd=endEmptyLocations+1
							for x in range(pageAllocationStart,pageAllocationEnd):
								memory[x]=1
							print("process: "+str(processNo)+" page inserted into memory from "
								+str(pageAllocationStart)+" to "+str(pageAllocationEnd))
							pageStart.append(pageAllocationStart)
							pageEnd.append(pageAllocationEnd)
							countEmptyLocations=0
							startEmptyLocations=0
							endEmptyLocations=0
							break
					else:
						startEmptyLocations=0
						endEmptyLocations=0
						countEmptyLocations=0
			# print pageStart,pageEnd
			threadLifeTime = lifeTimeThread(1, "Thread-2",lifeTime,processNo,pageStart,pageEnd)
			threadLifeTime.daemon = True
			threadLifeTime.start()
		else:
			print("process: "+str(processNo)+" space: "+ str(processMemorySize)+" Not  Available")

	elif(memoryPolicy==3 and fitnessAlgo==1):
		for location in range(0,memory_size):
			if memory[location] is None:
				if countEmptyLocations==0:
					startEmptyLocations=location
				countEmptyLocations+=1
				if countEmptyLocations==processMemorySize:
					endEmptyLocations=location
					spaceAvailable=True
					# print("space: "+ str(processMemorySize)+" Available for proces: "+str(processNo)+ 
					# 	" from "+ str(startEmptyLocations)+ " to "+ str(endEmptyLocations))
					countEmptyLocations=0
					startEmptyLocations=0
					endEmptyLocations=0
					break
				else:
					spaceAvailable=False
		if spaceAvailable==True:
			for segment in segments:
				for location in range(0,memory_size):
					if memory[location] is None:
						if countEmptyLocations==0:
							startEmptyLocations=location	
						countEmptyLocations+=1
						if countEmptyLocations==segment:
							endEmptyLocations=location
							segmentAllocationStart=startEmptyLocations
							segmentAllocationEnd=endEmptyLocations+1
							print("process: "+str(processNo)+" segment inserted into memory from "
								+str(segmentAllocationStart)+" to "+str(segmentAllocationEnd))
							for x in range(segmentAllocationStart,segmentAllocationEnd):
								memory[x]=1
							segmentStart.append(segmentAllocationStart)
							segmentEnd.append(segmentAllocationEnd)
							countEmptyLocations=0
							startEmptyLocations=0
							endEmptyLocations=0
							break
					else:
						startEmptyLocations=0
						endEmptyLocations=0
						countEmptyLocations=0
			threadLifeTime = lifeTimeThread(1, "Thread-2",lifeTime,processNo,segmentStart,segmentEnd)
			threadLifeTime.daemon = True
			threadLifeTime.start()
		else:
			print("process: "+str(processNo)+" space: "+ str(processMemorySize)+" Not  Available")
	elif(memoryPolicy==3 and fitnessAlgo==2):
		for location in range(0,memory_size):
			if memory[location] is None:
				if countEmptyLocations==0:
					startEmptyLocations=location
				countEmptyLocations+=1
				if countEmptyLocations==processMemorySize:
					endEmptyLocations=location
					spaceAvailable=True
					# print("space: "+ str(processMemorySize)+" Available for proces: "+str(processNo)+ 
					# 	" from "+ str(startEmptyLocations)+ " to "+ str(endEmptyLocations))
					countEmptyLocations=0
					startEmptyLocations=0
					endEmptyLocations=0
					break
				else:
					spaceAvailable=False
		if spaceAvailable==True:
			for segment in segments:
				for location in range(0,memory_size):
					if memory[location] is None:
						if countEmptyLocations==0:
							startEmptyLocations=location	
						countEmptyLocations+=1
					else:					
						if countEmptyLocations>=segment:
							endEmptyLocations=location
							availableSegmentsStart.append(startEmptyLocations)
							availableSegmentsEnd.append(endEmptyLocations)
							segmentSize=endEmptyLocations-startEmptyLocations
							availableSegmentSize.append(segmentSize)
							countEmptyLocations=0
							startEmptyLocations=0
							endEmptyLocations=0
						else:
							endEmptyLocations=0
							startEmptyLocations=0
							countEmptyLocations=0
					if(location==(memory_size-1)):
						if countEmptyLocations>=segment:
							endEmptyLocations=location
							availableSegmentsStart.append(startEmptyLocations)
							availableSegmentsEnd.append(endEmptyLocations)
							segmentSize=endEmptyLocations-startEmptyLocations
							availableSegmentSize.append(segmentSize)
							countEmptyLocations=0
							startEmptyLocations=0
							endEmptyLocations=0
						else:
							endEmptyLocations=0
							startEmptyLocations=0
							countEmptyLocations=0
				if len(availableSegmentSize)!=0:
					smallestSegmentSize=availableSegmentSize.index(min(availableSegmentSize))
					processAllocationStart=availableSegmentsStart[smallestSegmentSize]
					processAllocationEnd=processAllocationStart+segment
					segmentStart.append(processAllocationStart)
					segmentEnd.append(processAllocationEnd)
					for x in range(processAllocationStart,(processAllocationStart+segment)):
						memory[x]=1
					print("process No: "+ str(processNo) + " segment Allocated from "+
						str(processAllocationStart)+" to "+str(processAllocationEnd))
					# del availableSegmentsStart[:]
					# del availableSegmentSize[:]
					# del availableSegmentsEnd[:]
				# else:
				# 	del availableSegmentsStart[:]
				# 	del availableSegmentSize[:]
				# 	del availableSegmentsEnd[:]
			threadLifeTime = lifeTimeThread(1, "Thread-2",lifeTime,processNo,segmentStart,segmentEnd)
			threadLifeTime.daemon = True
			threadLifeTime.start()
		else:
			print("process No: "+str(processNo)+" space Not  Available")
	# print memory

		# print page
	del emptyBlocks[:]
	del emptyBlocksStart[:]
	del emptyBlocksEnd[:]
	del pageStart[:]
	del pageEnd[:]
	del segmentStart[:]
	del segmentEnd[:]
	del availableSegmentsStart[:]
	del availableSegmentSize[:]
	del availableSegmentsEnd[:]

		# print memory
memory_size=1500

# raw_input("Memory Size: ")
# memoryPolicy=raw_input("1-VSP,2-PAG,3-SEG: ")
memoryPolicy=3
fitnessAlgo=1
# if (memoryPolicy == '1' or memoryPolicy == '3'):
# 	fitnessAlgo=raw_input("1-First Fit, 2-Best Fit: ")
# 	print("Fitness Algo: "+fitnessAlgo)
# elif(memoryPolicy=='2'):
# 	pageSize=raw_input("Page/Frame Size: ")
pageSize=100
# 	print("Page Size:"+pageSize)
# else:
# 	print("Wrong Input")
# 	exit(1)
# print("Memory Policy: "+memoryPolicy)
# print("Memory Size: "+mem_size)
workLoadName="input1.txt"
# # raw_input("WorkLoad File Name: ")

memory=[None] * memory_size
# print memory
# for i in range(100,300):
# 	memory[i]=1
# for i in range(700,900):
# 	memory[i]=1
# print memory
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

chunkInfo=[]
for i, line in enumerate(fo):
	if i in timeLines:
		new_line=line.split()
		arrivalTimeLiness.append(new_line[0])
		lifeTimeLiness.append(new_line[1])
	if i in processNoLines:
		processNos.append(line)
	if i in addressSpace:
		line=line.split()
		line=map(int,line)
		chunkInfo.append(line)
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

for i in chunkInfo:
	i.pop(0)
chunkInfoInt=[]
totalChunkSize=[]
for chunk in chunkInfo:
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
	segments=chunkInfo[count]
	if p==1:
		thread.start()
	# time.sleep(0.000001)
	currentTime=thread.timePassed()
	# print ("Time is "+str(currentTime))
	# if currentTime > currentProcessArrivalTime:
		# print("process No: "+str(p)+" arrived")
	MMU(p,currentProcessMemorySize,currentProcessLifeTime,segments,memoryPolicy,fitnessAlgo)
	# else:
	# 	nonProcessedProcesses.append(p)
	count=count+1
# print("non processed processes are: ",nonProcessedProcesses)
# print memory
# for i in range(0,memory_size):
# 	memory[i]=None
if  nonProcessedProcesses:
	print("Processsing non processed processes")
	for p in nonProcessedProcesses:
		index=processNosStripped1.index(p)
		currentProcessArrivalTime=arrivalTimeLiness[index]
		currentProcessLifeTime=lifeTimeLiness[index]
		currentProcessMemorySize=totalChunkSize[index]
		MMU(p,currentProcessMemorySize,currentProcessLifeTime,memoryPolicy,fitnessAlgo)
		del nonProcessedProcesses[nonProcessedProcesses.index(p)]
# print("non processed processes are: ",nonProcessedProcesses)








