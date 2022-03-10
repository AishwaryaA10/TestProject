
#test1

#test2
fileConn<-file("/data/output12.txt")
writeLines(c("Hello","World!!"), fileConn)
close(fileConn)


