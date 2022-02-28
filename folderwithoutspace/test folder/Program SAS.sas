#auto commitdata race;
pr = probnorm(-15/sqrt(325));
run;

#manual
proc print data=race;
var pr;
run;
