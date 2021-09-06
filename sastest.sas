DATA data_set_name;
INPUT ID $ NAME $ SALARY DEPARTMENT $;
comm = SALARY*2.50;
LABEL ID = 'Emp_ID' comm = 'COMMISION';
DATALINES;
1 Tom 5000 IT
2 Harry 6000 Operations
3 Michelle 7000 IT
4 Dick 8000 HR
5 John 9000 Finance 
;
RUN;

#test commit conflict -1
