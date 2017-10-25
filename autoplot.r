args <- commandArgs()
file<-as.character(args[5])



a<-read.table(file)
png("outputs/profile.png",height=8,width=15)
#plot(smooth.spline(a$V2),type="l",col=2,lwd=3,ylim=c(-1,1),xlab="Sequence",ylab="Score",main="RSS propensity")
plot(as.vector(na.omit(filter(a$V2, rep(1/7,7) ))),type="l",col=2,lwd=3,ylim=c(-1,1),xlab="Sequence",ylab="Score",main="RSS propensity")
abline(h=0,lty="dashed", col="black",lwd=2)
dev.off()

