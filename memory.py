#!/usr/bin/python
import threading
from collections import deque
class virtualClock (threading.Thread):
   def __init__(self, threadID, name,start1,stop):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.start1=start1
      self.stop=stop 
   def run(self):
      print "Starting " + self.name
      time_in_memory(self.name,1)

      print "time completed"
      print ("start is : ",self.start1)
      print ("stop is : ",self.stop)
      remove_from_memory(self.start1,self.stop)
      print "Exiting " + self.name + str(self.threadID)

def time_in_memory(threadName, delay):
	i=delay
	while(i<=100):
		i=i+1



non_processed_process=[]
def MMU(proc_no,process_mem_size):
	counter=0
	for i in range(0,mem_size):
		if memory[i] is None:
			if counter==0:
				start=i
			counter=counter+1
			if counter==process_mem_size:
				stop=i
				print "block available from location: " + str(start) + " to " + str(stop)
				new_start=start
				for x in range(start,stop+1):
					memory[start]=1 #inserting block into memory
					start=start+1
				
				thread = virtualClock(1, "Thread-1",new_start,stop)
				thread.start()
				break
		if (i==(mem_size-1) and (counter!=process_mem_size)):
			non_processed_process.append(proc_no)
			print ("i is: "+str(i)+ "mem size is :" +str(mem_size-1)+ " "+ str(counter)+" space not available")

	# for p in non_processed_process:
	# 	if p is not None:
	# 		# print non_processed_process 

def remove_from_memory(start,stop):
	print ("before: ",memory)
	for i in range(0,400):
		memory[i]=None
	print ("after: ",memory)


mem_size=1000
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
work_load_name="inputs1.txt"
# raw_input("WorkLoad File Name: ")
# print("WorkLoad File Name: "+ work_load_name)

memory=[None] * mem_size


fo=open("input1.txt","rw+")
total_processes=int(fo.read(1))
# print ("no of process: ",total_processes)

process_no_line=1
processes_no_lines=[]
process_nos=[]

time_lines=[]
arrival_time_liness=[]
time_lines_line_no=2	
life_time_liness=[]

address_space_line_no=3
address_space=[]
no_of_chunks=[]
chunk_sizes=[[]]


while(total_processes!=0):
	processes_no_lines.append(process_no_line)
	time_lines.append(time_lines_line_no)
	address_space.append(address_space_line_no)
	address_space_line_no=address_space_line_no+4
	time_lines_line_no=time_lines_line_no+4
	process_no_line=process_no_line+4
	total_processes=total_processes-1

chunk_info=[]
for i, line in enumerate(fo):
	if i in time_lines:
		new_line=line.split()
		arrival_time_liness.append(new_line[0])
		life_time_liness.append(new_line[1])
	if i in processes_no_lines:
		process_nos.append(line)
	if i in address_space:
		line=line.split()
		chunk_info.append(line)
fo.close()
process_nos_stripped=[]
for process in process_nos:
	process_nos_stripped.append(process.strip())

#code to extrace chunk information
#chunkinfo[i][0]=no_of_chunks
#loop through no_of_chunks and extract their sizes
# for i in range(0,total_processes):
# 	print ("no of chunks in process no " , i, "are " , int(chunk_info[i][0]))
# 	for j in range(1,int(chunk_info[i][0])+1):
# 		print ("chunk size of process ",i, "are", chunk_info[i][j])

process_nos_stripped=map(int,process_nos_stripped)	
arrival_time_liness=map(int,arrival_time_liness)	
life_time_liness=map(int,life_time_liness)	


# print (chunk_info)
chunk_info_int=[]
total_chunk_size=[]
for i in chunk_info:
	i=map(int,i)
	chunk_info_int.append(i)
count=0
for i in chunk_info_int:
	del	i[0]
	total_chunk_size.append(sum(i))

# print (process_nos_stripped)
# print (arrival_time_liness)
# print (life_time_liness)
# print (total_chunk_size)

process_nos_stripped1=[1,2]
count=0
for p in process_nos_stripped1:
	current_process_arrival_time=arrival_time_liness[count]
	current_process_life_time=life_time_liness[count]
	current_process_memory_size=total_chunk_size[count]
	# print(p, " before: ",current_process_life_time)
	# while(current_process_life_time != 0):
	# print "current_process_memory_size: "+str(current_process_memory_size)
	MMU(p,current_process_memory_size)
	# print("here")
	# print ("count"+str(count))	
		# current_process_life_time=current_process_life_time-1
	# print(p ," after: ",current_process_life_time)

	count=count+1
# print memory
# print non_processed_process





