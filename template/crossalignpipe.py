import os
import sys
import random
import time
import numpy
import subprocess
from shutil import copyfile


#LAUNCHING CROSS


os.system("python crosspipeline.py global")
#input1=os.listdir("./Submission/Profiles/")[0]
input1=((open("input.fasta","r").readline()).split("\t"))[0][1:]
copyfile("./outputs/table.txt", "./outputs/table1.txt")
#copyfile("./outputs/smooth.txt", "./outputs/smoothvalue1.txt")
file1=open("./outputs/table.txt","r").readlines()
os.system("awk '($4!=\"-\"){print $4}' ./outputs/table.txt > outputs/smooth1.txt")

# os.system("cp input2.fasta input.fasta")
# os.system("python crosspipeline.py global")
# input2=((open("input.fasta","r").readline()).split("\t"))[0][1:]
# #input2=os.listdir("./Submission/Profiles/")[0]
# file2=open("./outputs/table.txt","r").readlines()
# os.system("awk '($4!=\"-\"){print $4}' ./outputs/table.txt > outputs/smooth2.txt")




#DTW ALGORITHM

mode=str(sys.argv[1])

#print filez

if mode!="fragment" and mode!="dataset":

	os.system("cp input2.fasta input.fasta")
	os.system("python crosspipeline.py global")
	input2=((open("input.fasta","r").readline()).split("\t"))[0][1:]
	copyfile("./outputs/table.txt", "./outputs/table2.txt")
	#copyfile("./outputs/smooth.txt", "./outputs/smoothvalue2.txt")
	#input2=os.listdir("./Submission/Profiles/")[0]
	file2=open("./outputs/table.txt","r").readlines()
	os.system("awk '($4!=\"-\"){print $4}' ./outputs/table.txt > outputs/smooth2.txt")
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

if mode=="obe":
	if len(hum1)<len(mou1):
		subprocess.call("cat dtw_obe.r | R --slave --vanilla --args "+name1+" "+name2+" "+input1+" "+input2,shell=True)
		os.system("awk '{print NR,$1}' tmp1.txt > shorter.txt")
		os.system("awk '{print NR,$1}' tmp2.txt > longer.txt")
	else:
		subprocess.call("cat dtw_obe.r | R --slave --vanilla --args "+name2+" "+name1+" "+input2+" "+input1,shell=True)
		os.system("awk '{print NR,$1}' tmp2.txt > shorter.txt")
		os.system("awk '{print NR,$1}' tmp1.txt > longer.txt")



if mode=="fragment":
	os.system("cp input2.fasta input.fasta")
	os.system("python crosspipeline.py global")
	input2=((open("input.fasta","r").readline()).split("\t"))[0][1:]
	#input2=os.listdir("./Submission/Profiles/")[0]
	file2=open("./outputs/table.txt","r").readlines()
	os.system("awk '($4!=\"-\"){print $4}' ./outputs/table.txt > outputs/smooth2.txt")
	hum1=[]
	mou1=[]
	for line2 in file2:
		camp2=line2.split("\t")
		#camp2=line2.split(" ")
		#print camp2
		if len(camp2)==4:
			if camp2[1]!="-\n":
				mou1.append(float(camp2[2]))
			else:
				mou1.append(0)
	for line in file1:
		camp=line.split("\t")
		#camp=line.split(" ")
		#print camp
		if len(camp)==4:
			if camp[1]!="-\n":
				hum1.append(float(camp[2]))
			else:
				hum1.append(0)

	tmp2=open("tmp2.txt","w")
	for y in mou1:
		tmp2.write(str(y)+"\n")
	tmp2.close()

	n=200
	i=1
	while (i*n)<=len(hum1):
		hum2=[]
		hum2=hum1[(n*(i-1)):(n*(i))]


		# for elem in hum1:
# 			if hum1.index(elem)>=(n*(i-1)) and hum1.index(elem)<(n*(i)):
# 				hum2.append(elem)

		tmp1=open("tmp1.txt","w")

		for x in hum2:
			tmp1.write(str(x)+"\n")

		name1="tmp1.txt"
		name2="tmp2.txt"
		tmp1.close()
		subprocess.call("cat dtw_obe.r | R --slave --vanilla --args "+name1+" "+name2+" "+input1+"_"+str(n*i)+" "+input2,shell=True)
		os.system("awk '{print NR,$1}' tmp1.txt > shorter.txt")
		os.system("awk '{print NR,$1}' tmp2.txt > longer.txt")
		i=i+1

if mode=="dataset":
	org=str(sys.argv[2])
	hum1=[]
	for line in file1:
		camp=line.split("\t")
		if len(camp)==4:
			if camp[1]!="-\n":
				hum1.append(float(camp[2]))
			else:
				hum1.append(0)
	files=os.listdir("../../organisms/"+org+"/")
	#print os.listdir("organisms/try/")
	leng=open("leng.txt","w")

	for filey in files:

		if filey!=".txt" and filey!=".DS_Store" and filey[:3]=="ENS":
			mou1=[]
			file2=open("../../organisms/"+org+"/"+filey,"r").readlines()
			for line2 in file2:
				camp2=line2.split("\t")
				if len(camp2)==4:
					if camp2[1]!="-\n":
						mou1.append(float(camp2[2]))
					else:
						mou1.append(0)
			#print hum1,mou1
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
			#print filez,filey

			if len(hum1)<len(mou1):
				subprocess.call("cat dtw_obe.r | R --slave --vanilla --args "+name1+" "+name2+" "+input1+" "+filey,shell=True)
				leng.write(input1+" "+filey+" "+str(len(hum1))+" "+str(len(mou1))+"\n")
			else:
				subprocess.call("cat dtw_obe.r | R --slave --vanilla --args "+name2+" "+name1+" "+filey+" "+input1,shell=True)
				leng.write(filey+" "+input1+" "+str(len(mou1))+" "+str(len(hum1))+"\n")
	leng.close()
