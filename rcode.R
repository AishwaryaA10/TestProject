#auto commit
#test1
fileConn<-file("/data/output12.txt")
writeLines(c("Hello","World!!"), fileConn)
close(fileConn)


