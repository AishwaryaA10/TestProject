


/* Score function for model registry */
%MACRO score(model_object , request);

proc plm restore=&model_object;
score data=&request out= mosaic.predicted_data predicted;
/*pred=predicted lcl=Lower ucl=upper; */
run;

%MEND;



%score(mosaic.scoring_obj, mosaic.request_obj);