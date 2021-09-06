fileConn<-file("/test_mosaic/G2/test.txt")
writeLines(c("Hello","World"), fileConn)
close(fileConn)