/*  This programs is  written for classification model. here using titanic dataset 
we train a classification model and see what are the important variables are there which help people to survive*/
proc import file="/data/titanic_train.csv" 
out=train dbms=csv replace;
run;
proc import file="/data/titanic_test.csv" 
out=test dbms=csv replace;
run;
/* Show the Dataset */
proc print data=train(obs=10);
title Sample Titanic dataset;
run;
/* Checking the contents of the data*/
proc contents data=train;
run; 
/* Checking the frequency of the Target Variable Survived */ 
proc freq data=train; 
table Survived; 
run;
title "Survived vs Gender";
proc sgplot data=train pctlevel=group;
vbar sex / group=Survived stat=percent missing;
label Embarked = "Passenger Embarking Port";
run;
title "Analysis of embarkation locations";
proc sgplot data=train;
vbar Embarked / datalabel missing;
label Embarked = "Passenger Embarking Port";
run; 
/* Checking the missing value and Statistics of the dataset */
proc means data=train N Nmiss mean std min P25 P50 P75 P90 max;
run;
/* Sorting out the Pclass and Age for creating boxplot */
proc sort data=train out=sorted;
by Pclass descending Age;
run;
title ‘Box Plot for Age vs Class’;
proc boxplot data=sorted;
plot Age*Pclass;
run;
/* Creating Logistic regression model */
proc logistic data=train descending;
class Embarked Parch Pclass Sex SibSp Survived;
model Survived(event='1') = Age Fare Embarked Parch Pclass Sex SibSp /
selection=stepwise expb stb lackfit
outroc = ROC; 
output out = titanic_logistic;  
/*store titanic_logistic; */
score data = test out = Scored_test outroc=troc; 
run;