#!/usr/bin/python
mem_size=raw_input("Memory Size: ")
mem_policy=raw_input("1-VSP,2-PAG,3-SEG: ")
if (mem_policy == '1' or mem_policy == '3'):
	fitness_algo=raw_input("1-First Fit, 2-Best Fit: ")
	print("Fitness Algo: "+fitness_algo)
elif(mem_policy=='2'):
	page_size=raw_input("Page/Frame Size: ")
	print("Page Size:"+page_size)
else:
	print("Wrong Input")
	exit(1)
print("Memory Policy: "+mem_policy)
print("Memory Size: "+mem_size)
work_load_name=raw_input("WorkLoad File Name: ")
print("WorkLoad File Name: "+ work_load_name)



fo=open("input1.txt","rw+")
total_processes=int(fo.read(1))
print ("no of process: ",total_processes)

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


#code to extrace chunk information
#chunkinfo[i][0]=no_of_chunks
#loop through no_of_chunks and extract their sizes
# for i in range(0,total_processes):
# 	print ("no of chunks in process no " , i, "are " , int(chunk_info[i][0]))
# 	for j in range(1,int(chunk_info[i][0])+1):
# 		print ("chunk size of process ",i, "are", chunk_info[i][j])




print (process_nos)
print (arrival_time_liness)
print (life_time_liness)
print (chunk_info)


fo.close()