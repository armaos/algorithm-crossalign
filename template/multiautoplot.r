args <- commandArgs()
file<-as.character(args[5])
length<-as.integer(args[6])



a<-read.table("profile.txt")
path<-getwd()
#png(paste("/Submission/Graphs/",file,".png",sep=""))
png(paste(path,"/Submission/Graphs/",file,".png",sep=""))
#x<-c(7:(length(running.mean(a$V2,7))+6))
#plot(smooth.spline(a$V2),type="l",col=2,lwd=3,ylim=c(-1,1),xlab="Sequence",ylab="Score",main="RSS propensity")
plot(as.vector(na.omit(filter(a$V2, rep(1/length,length) ))),type="l",col=2,lwd=3,xlab="Sequence",ylab="Score",main="RSS propensity")
abline(h=0,lty="dashed", col="black",lwd=2)
dev.off()
var<-filter(a$V2, rep(1/length,length))
write(var,file="smooth.txt",sep="\n")