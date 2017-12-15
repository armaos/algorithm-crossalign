import os


myfile=open("table_big.txt","r").readlines()
tmp=open("./outputs/table_final2.txt","w")
for line in myfile:
	camp=line.split()
	if camp[0]==camp[5] and camp[1]==camp[6]:
		score=camp[2]
		size1=int(camp[7])
		size2=int(camp[8])
		if size1<=300:
			sizeone=200
		if size2<=300:
			sizetwo=200
		if size1>300 and size1<=700:
			sizeone=500
		if size2>300 and size2<=700:
			sizetwo=500
		if size1>700 and size1<=3000:
			sizeone=1000
		if size2>700 and size2<=3000:
			sizetwo=1000
		if size1>3000:
			sizeone=5000
		if size2>3000:
			sizetwo=5000
		distr=open("./distributions/"+str(sizeone)+"_"+str(sizetwo)+"_.dist","r").readlines()	
		i=1
		tot=0
		for elem in distr:
			if float(elem)<=float(score):
				tot=tot+1
			i=i+1
		pval=float(float(tot)/float(i))	
		#tmp.write(line[:-1]+"\t"+("{:.1e}".format(pval))+"\n")
		tmp.write(camp[0]+"\t"+camp[1]+"\t"+score+"\t"+camp[3]+"\t"+camp[4]+"\t"+("{:.1e}".format(pval))+"\n")
tmp.close()