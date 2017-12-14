#!/usr/bin/env python
import argparse
import IPython
import yaml
import os
import subprocess
import shutil, errno
import sys

# we want to be agnostic to where the script is ran
SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
WORKER_PATH = os.path.realpath(os.curdir)

# Function to copy the output directory content
def copyfolder(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc: # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else: raise

# read the task definition yaml file
with open(os.path.join(SCRIPT_PATH, "crossalign.yaml"), "r") as task_f:
    task_definition = yaml.load(task_f)

parser = argparse.ArgumentParser(
   description='Launches crossalign algorithm with properly parset parameters')

parser.add_argument(
   '-output_dir', type=str, nargs=1,
   help='Directory where the output is going to be stored')

# accept form fields
for item in task_definition['form_fields']:
   nargs = 1 if item['required'] else "?"
   parser.add_argument(
       '-FORM%s'%item['name'], type=str, default="none", nargs=nargs,
       help='Form argument: %s' % item)

# this parse_args stops if any unexpected arguments is passed
args = parser.parse_args()

OUTPUT_PATH = os.path.join(WORKER_PATH, args.output_dir[0])
random_number = (""" "{}" """.format(args.output_dir[0])).split("/")[3]

TMP_PATH = SCRIPT_PATH+"/tmp/"+random_number
#print "tmp path: ", TMP_PATH
#print "src  path: ", SCRIPT_PATH+"/template"
if os.path.exists(TMP_PATH) == True:
    shutil.rmtree(TMP_PATH)
copyfolder(SCRIPT_PATH+"/template", TMP_PATH)
#import IPython
#IPython.embed()
import re
import StringIO
from Bio import SeqIO

Rpat = re.compile('>.*?\n[GATCU]+', re.IGNORECASE)
if Rpat.match(args.FORMsequence_one[0]) == None:
	args.FORMsequence_one[0] = ">input_rna\n"+args.FORMsequence_one[0]
rnaSeq = []
for record in SeqIO.parse(StringIO.StringIO(args.FORMsequence_one[0]), "fasta"):
	rnaSeq.append(record)
	
rnaFile = os.path.join(OUTPUT_PATH.replace("outputs/", ""),"rna.fasta")
output_handle = open(rnaFile, "w")
SeqIO.write(rnaSeq, output_handle, "fasta")
output_handle.close()

if args.FORMfeature[0]!="dataset":
	Rpat = re.compile('>.*?\n[GATCU]+', re.IGNORECASE)
	if Rpat.match(args.FORMsequence_two) == None:
		#print args.FORM
		args.FORMsequence_two = ">input_rna2\n"+args.FORMsequence_two
	rnaSeq2 = []
	for record in SeqIO.parse(StringIO.StringIO(args.FORMsequence_two), "fasta"):
		rnaSeq2.append(record)
	
	rnaFile2 = os.path.join(OUTPUT_PATH.replace("outputs/", ""),"rna2.fasta")
	output_handle = open(rnaFile2, "w")
	SeqIO.write(rnaSeq2, output_handle, "fasta")
	output_handle.close()





os.chdir(SCRIPT_PATH)

args.FORMtitle = "".join([t.replace(' ', '_') for t in args.FORMtitle])
if args.FORMfeature[0]!="dataset":
	print "ok"
	command = """ bash crossalign.sh "{}" "{}" "{}" "{}" """.format(rnaFile,rnaFile2,args.FORMfeature[0],random_number,args.FORMemail[0])
else:
	command = """ bash crossalign.sh "{}" "{}" "{}" "{}" """.format(rnaFile,args.FORMorganism[0],args.FORMfeature[0],random_number,args.FORMemail[0])

p = subprocess.Popen(command, cwd=SCRIPT_PATH, shell=True)
p.communicate()
#os.system("php "+SCRIPT_PATH+"/index.cross.html > "+SCRIPT_PATH+"/index.cross2.html")
if p.returncode == 0:
	TMP_PATH = SCRIPT_PATH+ "/tmp/"+ random_number+"/outputs/"
	dirList=os.listdir(TMP_PATH)
	for file in dirList:
		shutil.copyfile(TMP_PATH+file, OUTPUT_PATH+file)

	from django.template import Template
	from django.template import Context
	from django.conf import settings
	from django.template import Template

	settings.configure(TEMPLATE_DIRS=(os.path.join(SCRIPT_PATH,'./')), DEBUG=True, TEMPLATE_DEBUG=True)

	# read the template file into a variable
	i=0
	myfile=open(TMP_PATH+"score.txt","r").readlines()
	for line in myfile:
		distance=line[:-1]
		
	#P-VALUE	
	if args.FORMfeature[0]!="fragment":
		myfile2=open(TMP_PATH+"pval.txt","r").readlines()
		for line in myfile2:
			pval=line[:-1]
		
	summary_line=''
	
	
	

		
	
	#HTML INDEX DECISION
	if args.FORMfeature[0]=="normal":
		with open(os.path.join(SCRIPT_PATH, "index.crossalign.html"), "r") as template_file:
			   template_string = "".join(template_file.readlines())
			   
	if args.FORMfeature[0]=="obe":
		with open(os.path.join(SCRIPT_PATH, "index.crossalign_obe.html"), "r") as template_file:
			   template_string = "".join(template_file.readlines())
			   
		myfile2=open(TMP_PATH+"start.txt","r").readlines()
		for line in myfile2:
			begin=line[:-1]
		myfile3=open(TMP_PATH+"end.txt","r").readlines()
		for line2 in myfile3:
			finish=line2[:-1]
			
	if args.FORMfeature[0]=="fragment":
		with open(os.path.join(SCRIPT_PATH, "index.crossalign_fragments.html"), "r") as template_file:
			   template_string = "".join(template_file.readlines())
	f args.FORMfeature[0]=="dataset":
		with open(os.path.join(SCRIPT_PATH, "index.crossalign_dataset.html"), "r") as template_file:
			   template_string = "".join(template_file.readlines())
	import datetime

	# create template from the string
	t = Template(template_string)
	
	# context contains variables to be replaced
	
	
	if args.FORMfeature[0]=="normal":
	
		c = Context(
			{
			   "title": args.FORMtitle,
			   "randoms" : random_number,
			   "feature" : args.FORMfeature[0],
			   "value" : distance,
			   "pvalue" : pval,
			   "generated" : str(datetime.datetime.now()),
			   "summary" : summary_line
		   }
		)
	
	if args.FORMfeature[0]=="obe":
	
		c = Context(
		   {
			   "title": args.FORMtitle,
			   "randoms" : random_number,
			   "feature" : args.FORMfeature[0],
			   "value" : distance,
			   "pvalue" : pval,
			   "start" : begin,
			   "end" : finish,
			   "generated" : str(datetime.datetime.now()),
			   "summary" : summary_line
		   }
		)

	if args.FORMfeature[0]=="fragment":
	
		c = Context(
			{
			   "title": args.FORMtitle,
			   "randoms" : random_number,
			   "feature" : args.FORMfeature[0],
			   "generated" : str(datetime.datetime.now()),
			   "summary" : summary_line
		   }
		)
	if args.FORMfeature[0]=="dataset":
	
		c = Context(
			{
			   "title": args.FORMtitle,
			   "randoms" : random_number,
			   "feature" : args.FORMfeature[0],
			   "generated" : str(datetime.datetime.now()),
			   "summary" : summary_line
		   }
		)


	# and this bit outputs it all into index.html
	#print "crosspy OUTPUT_path", OUTPUT_PATH
	with open(os.path.join(OUTPUT_PATH, "index.html"), "w") as output:
	   output.write(t.render(c))

else:
	sys.exit("The execution of the C code  failed.")
