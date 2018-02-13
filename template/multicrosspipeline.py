import os
import sys
import numpy
import math
import random
import subprocess
import pickle
import scipy
import sklearn
from sklearn import svm
from sklearn.externals import joblib
import IPython

# FRAGMENTS: using a file or a sequence fragments the sequences in 13 window fragments and save all in a fragments.txt

print "Fragmenting the input RNA ..."

file=open("multi.input.fasta","r").readlines()
#seq="ACGTGACCTGTGCGAAAACCCGTGTTTTAACCACTTTATGAACTGGGGAC"
#seq=str(sys.argv[1])
IPython.embed()
for line in file:
	fragments=open("fragments.txt","w")
	namerna2=line.split("\t")[0][1:]
	namerna=namerna2.split("|")[0]
	seq=line.split("\t")[1][:-1]
	rnastruct_fasta=open("rnastr.fasta","w")
	#circularization of the sequence
	seqa=seq[-6:]
	seqb=seq[0:6]
	seq2=seqa+seq+seqb
	rnastruct_fasta.write(line.split("\t")[0]+"\n")
	rnastruct_fasta.write(line.split("\t")[1])
	rnastruct_fasta.close()
	#end of circularization
	#print seq
	valid_dna = 'AaCcGgTtUu'
	condition = all(x in valid_dna for x in seq)
	wind=13
	half=int((wind-1)/2)
	wind=half
	while (wind+half+1)<=len(seq2):
		window=seq2[wind-half:wind+half+1]
		#fragments.write(line.split("\t")[0]+"\t"+wind+"\t"+window+"\n")
		fragments.write(">name1\t"+str(wind-half+1)+"\t"+window+"\n")
		wind=wind+1

	fragments.close()

###############################
# BINARY CONVERSION: converts each standard nucleotide inside the fragments and save all inside NNinput.txt

	print "Binary converting fragments ..."
	fragments=open("fragments.txt","r").readlines()
	#print line.split("\t")[0],scores[wind],window
	#ann=open("./input/NNinput.txt","w")
	ann=open("./input/train.0.dat","w")
	# valid_dna = 'AaCcGgTtUu'
	# condition = all(x in valid_dna for x in seq)
	#if condition:
	wind=0
	ann.write(str(len(seq))+" 52 1\n")
	for line in fragments:
		window=line.split("\t")[-1]
		wind=wind+1
		for nt in window:
			if nt=="A" or nt=="a":
				ann.write("1 -1 -1 -1 ")
			if nt=="T" or nt=="t" or nt=="U" or nt=="u":
				ann.write("-1 -1 1 -1 ")
			if nt=="C" or nt=="c":
				ann.write("-1 1 -1 -1 ")
			if nt=="G" or nt=="g":
				ann.write("-1 -1 -1 1 ")
		##########add if need a random output because the structure is unknown
		if wind%2==0:
			ann.write("\n1\n")
		else:
			ann.write("\n-1\n")
	# if condition=="False":
	# 	os.system("echo 'Invalid character inside the sequence. Please see that only ACTGU are allowed.'")# > outputs/log.txt")
	ann.close()

#################################
# NEURAL NETWORK: launch first the normalise.sh Gian's script to normalize the input, then launch the selected ANN and saves the profile in a 1 column file

	net=str(sys.argv[1])
	print  "Creating the predictions ..."
	#os.system("sh normalise.sh NNinput.txt 0 0")
	os.system("gcc -o test simple_test.c -lfann -lm") #compile the simple_test.c script to run fann
	if net=="human":
		os.system("./test ./input/train.0.dat ./Networks/human | awk '(NF==3){print $3}' | awk '{print NR,$1}' > profile.txt")
	if net=="yeast":
		os.system("./test ./input/train.0.dat ./Networks/yeast | awk '(NF==3){print $3}' | awk '{print NR,$1}' > profile.txt")
	if net=="pdb":
		os.system("./test ./input/train.0.dat ./Networks/PDBfiltered | awk '(NF==3){print $3}' | awk '{print NR,$1}' > profile.txt")
	if net=="icshape":
		os.system("./test ./input/train.0.dat ./Networks/icall | awk '(NF==3){print $3}' | awk '{print NR,$1}' > profile.txt")
	if net=="hiv":
		os.system("./test ./input/train.0.dat ./Networks/hiv | awk '(NF==3){print $3}' | awk '{print NR,$1}' > profile.txt")
	##### SVM using all the 5 scores of the 5 models
	if net=="global":
		os.system("./test ./input/train.0.dat ./Networks/hiv | awk '(NF==3){print $3}' | awk '{print NR,$1}' > profile1.txt")
		os.system("./test ./input/train.0.dat ./Networks/human | awk '(NF==3){print $3}' | awk '{print NR,$1}' > profile4.txt")
		os.system("./test ./input/train.0.dat ./Networks/PDBfiltered | awk '(NF==3){print $3}' | awk '{print NR,$1}' > profile3.txt")
		os.system("./test ./input/train.0.dat ./Networks/icall | awk '(NF==3){print $3}' | awk '{print NR,$1}' > profile2.txt")
		os.system("./test ./input/train.0.dat ./Networks/yeast | awk '(NF==3){print $3}' | awk '{print NR,$1}' > profile5.txt")
		os.system("paste profile1.txt profile2.txt profile3.txt profile4.txt profile5.txt | awk '{print $1,$2,$4,$6,$8,$10}' > svm_input.txt")

	###LOADING AND TESTING OF THE SVM
		testname=open("svm_input.txt","r").readlines()
		clf = joblib.load('svm_proba.pkl')
		result=open("profile_tmp.txt","w")
		data_test=[[]]
		datay_test=[]
		for line in testname:
			camp=line.split(" ")
			datay_test.append(camp[0])
			x_test=[]
			for elem in camp[1:]:
				x_test.append(float(elem))
			#print camp[0],(clf.predict_proba(x_test))[0]
			result.write(str(camp[0])+" "+str((clf.predict_proba(x_test))[0])+"\n")
		result.close()
		#$3 prob to be negative, $4 prob to be positive
		os.system("awk '{print $0}' profile_tmp.txt | sed 's/]//g' | awk '{print $1,((2*$4)-1)}' > profile.txt")

		#RNAstructure
		tablepath=os.path.dirname(os.path.realpath(__file__))

	smooth=int(float(float(len(seq))/90)+7-0.22)
	#subprocess.call("cat multiautoplot.r | R --slave --vanilla --args "+namerna+" "+str(smooth),shell=True) #call autoplot.r to build the smoothing profile

##############
# TABLE creates the table in output in the webserver
	os.system("paste profile.txt smooth.txt | sed 's/NA/-/g' > profile_try.txt")
	predo=open("profile_try.txt","r").readlines()
	table=open("./custom_dataset/"+namerna,"w")
	#table.write("Position\tNucleotide\tPropensity\n")
	for line in predo:
		camp=line.split()
		if float(camp[1])>0:
			table.write(camp[0]+"\t"+seq[int(camp[0])-1]+"\t"+camp[1][:5]+"\t"+camp[2]+"\n")
		if float(camp[1])<0:
			table.write(camp[0]+"\t"+seq[int(camp[0])-1]+"\t"+camp[1][:6]+"\t"+camp[2]+"\n")
		if float(camp[1])==0 and len(line)>1:
				table.write(camp[0]+"\t"+seq[int(camp[0])-1]+"\t"+camp[1]+"\t"+camp[2]+"\n ")
	table.close()

#####################
# VIENNA
