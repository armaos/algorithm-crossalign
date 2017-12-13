args <- commandArgs()
vect1<-as.character(args[5])
vect2<-as.character(args[6])
name1<-as.character(args[7])
name2<-as.character(args[8])


library(dtw)
library(proxy)
#png("outputs/plot.png")
one<-read.table(vect1)
two<-read.table(vect2)
alignment<-dtw(one$V1,two$V1,keep=TRUE,open.begin=TRUE,open.end=TRUE,step.pattern=asymmetric,dist.method="Manhattan")
name1
name2
alignment$normalizedDistance
#alignment$index2
#plot(alignment,type="threeway",col=2,lwd=3,xlab="CROSS profile 1",ylab="CROSS profile 2",main="Structural alignment")
#dev.off()

#OBE

#head(alignment$index2,n=1)
#tail(alignment$index2,n=1)