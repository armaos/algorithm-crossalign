seq1=open("input_bis.fasta","r").readlines()
seq2=open("input2.fasta","r").readlines()
myfile=open("./outputs/score.txt","r").readlines()
for line in myfile:
	score=line[:-1]
	
size1=[]
size2=[]
for line in seq1:
	size1.append(len((line.split("\t"))[1][:-1]))
for line2 in seq2:
	size2.append(len((line2.split("\t"))[1][:-1]))
if size1[0]<=300:
	sizeone=200
if size2[0]<=300:
	sizetwo=200
if size1[0]>300 and size1[0]<=700:
	sizeone=500
if size2[0]>300 and size2[0]<=700:
	sizetwo=500
if size1[0]>700 and size1[0]<=3000:
	sizeone=1000
if size2[0]>700 and size2[0]<=3000:
	sizetwo=1000
if size1[0]>3000:
	sizeone=5000
if size2[0]>3000:
	sizetwo=5000
distr=open("./distributions/"+str(sizeone)+"_"+str(sizetwo)+"_.dist","r").readlines()	
i=1
tot=0
for elem in distr:
	if float(elem)<=float(score):
		tot=tot+1
	i=i+1
pval=float(float(tot)/float(i))	
print pval