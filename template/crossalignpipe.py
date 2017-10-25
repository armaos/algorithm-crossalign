import os
import sys
import mlpy
import random
import time
import numpy
import subprocess



#LAUNCHING CROSS


os.system("python crosspipeline.py global")
#input1=os.listdir("./Submission/Profiles/")[0]
input1=((open("input.fasta","r").readline()).split("\t"))[0][1:]
file1=open("./outputs/table.txt","r").readlines()

os.system("cp input2.fasta input.fasta")
os.system("python crosspipeline.py global")
input2=((open("input.fasta","r").readline()).split("\t"))[0][1:]
#input2=os.listdir("./Submission/Profiles/")[0]
file2=open("./outputs/table.txt","r").readlines()



#DTW ALGORITHM

mode=str(sys.argv[1])

#print filez
hum1=[]
mou1=[]
for line in file1:
	camp=line.split("\t")
	#camp=line.split(" ")
	#print camp
	if len(camp)==4:
		if camp[1]!="-\n":
			hum1.append(float(camp[2]))
		else:
			hum1.append(0)
	

#file2=open("./Submission/Profiles/"+input2,"r").readlines()
for line2 in file2:
	camp2=line2.split("\t")
	#camp2=line2.split(" ")
	#print camp2
	if len(camp2)==4:
		if camp2[1]!="-\n":
			mou1.append(float(camp2[2]))
		else:
			mou1.append(0)
			
tmp1=open("tmp1.txt","w")
tmp2=open("tmp2.txt","w")
for x in hum1:
	tmp1.write(str(x)+"\n")
for y in mou1:
	tmp2.write(str(y)+"\n")
name1="tmp1.txt"
name2="tmp2.txt"
tmp1.close()
tmp2.close()
#print file1,file2
if mode=="normal":
	if len(hum1)<len(mou1):
		subprocess.call("cat dtw.r | R --slave --vanilla --args "+name1+" "+name2+" "+input1+" "+input2,shell=True)
		os.system("awk '{print NR,$1}' tmp1.txt > shorter.txt")
		os.system("awk '{print NR,$1}' tmp2.txt > longer.txt")
	else:
		subprocess.call("cat dtw.r | R --slave --vanilla --args "+name2+" "+name1+" "+input2+" "+input1,shell=True)
		os.system("awk '{print NR,$1}' tmp2.txt > shorter.txt")
		os.system("awk '{print NR,$1}' tmp1.txt > longer.txt")
	
	