data race;
pr = probnorm(-15/sqrt(325));
run;
 
proc print data=race;
var pr;
run;

#test2