file=$1
file2=$2
network=$3
random=$4


#

# word=$(wc input.fasta | awk '{print $1}')
# if [[ $word -gt 1 ]]
# then
# 	python multicrosspipeline.py $network
# 	zip -r ./outputs/Submission Submission
# else
# 
# 	python crosspipeline.py $network
# 	step=$(<./outputs/smooth.txt)
# 	awk -v step=$step 'NR == 1 || NR % step == 0' ./outputs/table.txt | awk -F'\t' 'BEGIN{printf "<tbody>\n"}{printf "\t<tr>\n\t\t<td>%s</td>\n\t\t<td>%s</td>\n\t\t<td>%s</td>\n\t\t<td>%s</td>\n",$1, $2, $3, $4}END{printf "</tbody>\n"}'  > ./outputs/table.html
# fi

cd tmp/$random

awk '{if($1~/>/){printf "\n%s\t", $1}else printf $1 }' $file | awk '(NF>1)' > input.fasta
if (($network!="dataset"))
then
	cp input.fasta input_bis.fasta
	word1=$(wc input_bis.fasta | awk '{print $1}')
	word2=$(wc input2.fasta | awk '{print $1}')
	word=$word1+$word2
fi
awk '{if($1~/>/){printf "\n%s\t", $1}else printf $1 }' $file2 | awk '(NF>1)' > input2.fasta

if [[ $word -gt 2 ]]
then
	python multicrosspipeline.py $network
	zip -r ./outputs/Submission Submission
else

	python crossalignpipe.py $network $file2 > dtw_output.tmp
	awk '(NF==2 && $2~/0./){printf "%.3f\n",$2}' dtw_output.tmp > outputs/score.txt
	python pvalue.py > outputs/pval.txt
fi

if (($network!="fragment" && $network!="dataset"))
then
	
	python pvalue.py > outputs/pval.txt
fi
#awk '(NF==2 && $2~/^[[:digit:]]/){print $2}' dtw_output.tmp > outputs/score.txt

sed 's/]/-/g' dtw_output.tmp | awk '(NF>2 && $1~/-/){$1=""; print $0}' > outputs/matches.txt

if (($network=="obe"))
then
	#for i in `awk '{print $0}' ./outputs/matches.txt | tr " " "\n" | awk '($1!~/]/)' | awk '(length($1)>0)'`; do awk '(NR=="'$i'")' shorter.txt; done > cross_short.txt
	cp shorter.txt cross_short.txt
	start0=$(head -n 1 ./outputs/matches.txt | awk '{print $1}')
	end0=$(wc cross_short.txt | awk '{print $1}')
	final0=$(($end0+$start0))
	echo $final0 > outputs/end.txt
	#end0=$(tail -n 1 ./outputs/matches.txt | awk '{print $1}')
	awk -v start=$start0 -v end=$final0 '($1>=start && $1<=end)' longer.txt > cross_long.txt
	head -n 1 ./outputs/matches.txt | awk '{print $1}' > outputs/start.txt
	#tail -n 1 ./outputs/matches.txt | awk '{print $1}' > outputs/end.txt
	Rscript overlap.r
fi

if (($network=="fragment"))
then
	awk '(NF==2 && $1=="[1]"){printf "%s\t",$2} (NF>2 && $1=="[1]"){printf "%s\t%s\n",$2,$2+200}' dtw_output.tmp | sed 's/"//g' > outputs/table_final.txt
	python multipval.py
# 	for i in `awk '{print $0}' ./outputs/matches.txt | tr " " "\n" | awk '($1!~/]/)'`; do awk '(NR=="'$i'")' shorter.txt; done > cross_short.txt
# 	start0=$(head -n 1 ./outputs/matches.txt | awk '{print $1}')
# 	end0=$(tail -n 1 ./outputs/matches.txt | awk '{print $NF}')
	awk -F '\t' 'BEGIN{printf "<tbody>\n"}{printf "\t<tr>\n\t\t<td>%s</td>\n\t\t<td>%s</td>\n\t\t<td>%s</td>\n\t\t<td>%s</td>\n\t\t<td>%s</td>\n",$1, $3, $4, $5, $6}END{printf "</tbody>\n"}' ./outputs/table_final2.txt  > outputs/table.html
fi

if (($network=="dataset"))
then
	awk '(NF==2 && $1=="[1]"){printf "%s\t",$2} (NF>2 && $1=="[1]"){printf "%s\t%s\n",$2,$2+200}' dtw_output.tmp | sed 's/"//g' > outputs/table_final.txt
	python multipval.py
	awk '{print $1,$2,$3,$4,$6}' ./outputs/table_final2.txt > ./outputs/table_final3.txt
	zip -r ./outputs/Submission ./outputs/table_final3.txt
	#awk -F '\t' 'BEGIN{printf "<tbody>\n"}{printf "\t<tr>\n\t\t<td>%s</td>\n\t\t<td>%s</td>\n\t\t<td>%s</td>\n\t\t<td>%s</td>\n\t\t<td>%s</td>\n",$1, $3, $4, $5, $6}END{printf "</tbody>\n"}' ./outputs/table_final2.txt  > outputs/table.html
fi
cd ../..
