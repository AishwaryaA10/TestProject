#manual
data race;
pr = probnorm(-15/sqrt(325));
run;

#auto commit
proc print data=race;
var pr;
run;

