a<-read.table("cross_short.txt")
b<-read.table("cross_long.txt")
png("outputs/plot2.png")
plot(b$V2,type="l",col=2,lwd=3,ylim=c(-1,1),xlab="Sequence",ylab="CROSS score",main="")
lines(a$V2,col="darkgray",lwd=3)
abline(h=0,lty="dashed", col="black",lwd=2)
dev.off()

