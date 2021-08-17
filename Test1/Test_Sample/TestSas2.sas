data work.ds;
	length string $20;
 
	string = 'abcde';
	count_characters = length(string);
	output;
 
	string = 'abc123';
	count_characters = length(string);
	output;
 
	string = 'A!b %C-9';
	count_characters = length(string);
	output;
run;
 
proc print data=work.ds noobs;
run;