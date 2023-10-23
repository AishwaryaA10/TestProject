Libname mosaic '/notebooks/notebooks/';

/*  This programs is  written for classification model. here using titanic dataset
we train a classification model and see what are the important variables are there which help people to survive*/
proc import file="/notebooks/notebooks/titanic_train.csv" out=train dbms=csv 
		replace;
run;

proc import file="/notebooks/notebooks/titanic_test.csv" out=test dbms=csv 
		replace;
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
	label Embarked="Passenger Embarking Port";
run;

title "Analysis of embarkation locations";

proc sgplot data=train;
	vbar Embarked / datalabel missing;
	label Embarked="Passenger Embarking Port";
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
	model Survived(event='1')=Age Fare Embarked Parch Pclass Sex SibSp / 
		selection=stepwise expb stb lackfit outroc=ROC;
	output out=titanic_logistic;
	store mosaic.titanic_logistic;
	score data=test out=Scored_test outroc=troc;
run;

/* Create mosaic_score.sas */
/*Register Model*/
/*Model Object name
Name
Description
Scoring_func_name
Flavour*/

%LET MODEL_OBJ_PATH '/notebooks/notebooks/titanic_logistic.sas7bitm';
%LET SCORE_FILE '/notebooks/notebooks/mosaic_score1.sas';
%INCLUDE '/mosaicsasml/SAS/mosaicsasml.sas';
%register_model('titanic_classification_1_SAS', 'test_sas_model');
