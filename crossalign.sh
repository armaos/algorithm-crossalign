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
awk '{if($1~/>/){printf "\n%s\t", $1}else printf $1 }' $file2 | awk '(NF>1)' > input2.fasta

python crossalignpipe.py $network > dtw_output.tmp
#awk '(NF==2 && $2~/^[[:digit:]]/){print $2}' dtw_output.tmp > outputs/score.txt
awk '(NF==2 && $2~/0./){printf "%.3f\n",$2}' dtw_output.tmp > outputs/score.txt
sed 's/]/-/g' dtw_output.tmp | awk '(NF>2 && $1~/-/){$1=""; print $0}' > outputs/matches.txt

if [[$network=="obe"]]
then
	for i in `awk '{print $0}' ./outputs/matches.txt | tr " " "\n" | awk '($1!~/]/)'`; do awk '(NR=="'$i'")' shorter.txt; done > cross_short.txt
	start0=$(head -n 1 ./outputs/matches.txt | awk '{print $1}')
	end0=$(wc cross_short.txt | awk '{print $1}')
	awk -v start=$start0 -v end=$end0 '($1>=start && $1<=end)' longer.txt > cross_long.txt
	head -n 1 ./outputs/matches.txt | awk '{print $1}' > outputs/start.txt
	wc cross_short.txt | awk '{print $1}' > outputs/end.txt
fi

# step=$(<./outputs/smooth.txt)
# awk -v step=$step 'NR == 1 || NR % step == 0' ./outputs/table.txt | awk -F '\t' 'BEGIN{printf "<tbody>\n"}{printf "\t<tr>\n\t\t<td>%s</td>\n\t\t<td>%s</td>\n\t\t<td>%s</td>\n\t\t<td>%s</td>\n",$1, $2, $3, $4}END{printf "</tbody>\n"}'  > ./outputs/table.html
# 
cd ../..
