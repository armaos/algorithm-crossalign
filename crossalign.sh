file=$1
file2=$2
network=$3
random=$4




cd tmp/$random

awk '{if($1~/>/){printf "\n%s\t", $1}else printf $1 }' $file | awk '(NF>1)' > input.fasta
cat input.fasta

if [ $network == "normal" ]
then
	echo "normal"
	cp input.fasta input_bis.fasta
	awk '{if($1~/>/){printf "\n%s\t", $1}else printf $1 }' $file2 | awk '(NF>1)' > input2.fasta
	python crossalignpipe.py $network $file2 > dtw_output.tmp
	awk '(NF==2 && $2~/0./){printf "%.3f\n",$2}' dtw_output.tmp > outputs/score.txt
	python pvalue.py > outputs/pval.txt
	sed 's/]/-/g' dtw_output.tmp | awk '(NF>2 && $1~/-/){$1=""; print $0}' > outputs/matches.txt

fi


if [ $network == "obe" ]
then
	echo "obe"
	cp input.fasta input_bis.fasta
	awk '{if($1~/>/){printf "\n%s\t", $1}else printf $1 }' $file2 | awk '(NF>1)' > input2.fasta
	python crossalignpipe.py $network $file2 > dtw_output.tmp
	awk '(NF==2 && $2~/0./){printf "%.3f\n",$2}' dtw_output.tmp > outputs/score.txt
	python pvalue.py > outputs/pval.txt
	sed 's/]/-/g' dtw_output.tmp | awk '(NF>2 && $1~/-/){$1=""; print $0}' > outputs/matches.txt
	#for i in `awk '{print $0}' ./outputs/matches.txt | tr " " "\n" | awk '($1!~/]/)' | awk '(length($1)>0)'`; do awk '(NR=="'$i'")' shorter.txt; done > cross_short.txt
	cp shorter.txt cross_short.txt
	length=`wc cross_short.txt | awk '{print $1}'`
	awk '{for(i=1;i<=NF;i++){print $i}}' outputs/matches.txt > matches.col
	for ((i=1;i<=$length;i++));do pos=`awk '(NR=="'$i'")' matches.col`; awk '(NR=='$pos')' longer.txt | awk '{print "'$i'", $2}'; done > cross_long.txt
	start0=$(head -n 1 ./outputs/matches.txt | awk '{print $1}')
	end0=$(wc cross_short.txt | awk '{print $1}')
	final0=$(($end0+$start0))
	echo $final0 > outputs/end.txt
	#awk -v start=$start0 -v end=$final0 '($1>=start && $1<=end)' longer.txt > cross_long.txt
	head -n 1 ./outputs/matches.txt | awk '{print $1}' > outputs/start.txt
	Rscript overlap.r
	paste -d " "  cross_short.txt  cross_long.txt|  awk '{printf "%s\t%s\t%s\t%s\n", $1, $2, '$start0'+$3, $4}' >outputs/aligned.profiles.txt
	awk -F '\t' 'BEGIN{printf "<tbody>\n"}{printf "\t<tr>\n\t\t<td>%s</td>\n\t\t<td>%s</td>\n\t\t<td>%s</td>\n\t\t<td>%s</td>\n",$1, $2, $3, $4}END{printf "</tbody>\n"}' outputs/aligned.profiles.txt > ./outputs/table.html
fi

if [ $network == "fragment" ]
then
	echo "fragment"
	cp input.fasta input_bis.fasta
	awk '{if($1~/>/){printf "\n%s\t", $1}else printf $1 }' $file2 | awk '(NF>1)' > input2.fasta
	python crossalignpipe.py $network $file2 > dtw_output.tmp
	awk '(NF==2 && $2~/0./){printf "%.3f\n",$2}' dtw_output.tmp > outputs/score.txt
	sed 's/]/-/g' dtw_output.tmp | awk '(NF>2 && $1~/-/){$1=""; print $0}' > outputs/matches.txt
	awk '(NF==2 && $1=="[1]"){printf "%s\t",$2} (NF>2 && $1=="[1]"){printf "%s\t%s\n",$2,$2+200}' dtw_output.tmp | sed 's/"//g' > outputs/table_final.txt
	python multipval.py
	awk -F '\t' 'BEGIN{printf "<tbody>\n"}{printf "\t<tr>\n\t\t<td>%s</td>\n\t\t<td>%s</td>\n\t\t<td>%s</td>\n\t\t<td>%s</td>\n\t\t<td>%s</td>\n",$1, $3, $4, $5, $6}END{printf "</tbody>\n"}' ./outputs/table_final2.txt  > outputs/table.html
fi

if [ $network == "dataset" ]
then
	echo "dataset"; echo $file2
	python crossalignpipe.py $network $file2 > dtw_output.tmp
	awk '(NF==2 && $1=="[1]"){printf "%s\t",$2} (NF>2 && $1=="[1]"){printf "%s\t%s\n",$2,$2+200}' dtw_output.tmp | sed 's/"//g' > outputs/table_final.txt
	paste ./outputs/table_final.txt leng.txt > table_big.txt
	python multipval_dat.py
	echo "#short_RNA large_RNA Structural_Score Starting_match p-value" >./outputs/output_table.txt
	awk '{print $1,$2,$3,$4,$6}' ./outputs/table_final2.txt | sed 's/.txt//g' >>./outputs/output_table.txt
	#awk '{print $1,$2,$3,$4,$6}' ./outputs/table_final2.txt > ./outputs/output_table.txt
	zip -r ./outputs/Submission ./outputs/output_table.txt
	#awk -F '\t' 'BEGIN{printf "<tbody>\n"}{printf "\t<tr>\n\t\t<td>%s</td>\n\t\t<td>%s</td>\n\t\t<td>%s</td>\n\t\t<td>%s</td>\n\t\t<td>%s</td>\n",$1, $3, $4, $5, $6}END{printf "</tbody>\n"}' ./outputs/table_final2.txt  > outputs/table.html
fi
cd ../..
