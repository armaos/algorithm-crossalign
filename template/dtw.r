args <- commandArgs()
vect1<-as.character(args[5])
vect2<-as.character(args[6])
name1<-as.character(args[7])
name2<-as.character(args[8])


suppressMessages(library(dtw))
suppressMessages(library(proxy))
png("outputs/plot.png")
one<-read.table(vect1)
two<-read.table(vect2)

alignment<-dtw(one$V1,two$V1,keep=TRUE)
name1
name2
#alignment$distance
alignment$normalizedDistance
one<-read.table("outputs/smooth1.txt")
two<-read.table("outputs/smooth2.txt")
alignment<-dtw(one$V1,two$V1,keep=TRUE)
plot(alignment,type="threeway",col=2,lwd=3,xlab="CROSS profile 1",ylab="CROSS profile 2",main="Structural alignment")
dev.off()
alignment_table=paste(alignment$index1, one[alignment$index1,1], alignment$index2, two[alignment$index2,1],sep='\t')
write.table(alignment_table, "./outputs/alignment_table.txt", sep="\t",quote=FALSE,col.names=c("# Pos_RNA1 CROSS_score_RNA1 Pos_RNA2 CROSS_score_RNA2"))
#OBE
#alignment<-dtw(one$V1,two$V1,keep=TRUE,open.begin=TRUE,open.end=TRUE,step.pattern=asymmetric,dist.method="Manhattan")
#alignment$normalizedDistance
alignment$index2
#head(alignment$index2,n=1)
#tail(alignment$index2,n=1)
