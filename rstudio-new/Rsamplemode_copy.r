data.frame=read.csv('/data/train.csv',na.strings = '')
library(dplyr)
data.frame = select(data.frame, Survived, Pclass, Age, Sex, SibSp, Parch)
View(data.frame)
data.frame = na.omit(data.frame)
data.frame$Survived = factor(data.frame$Survived)
data.frame$Pclass = factor(data.frame$Pclass, order=TRUE, levels = c(3, 2, 1))


#split dataset
library(caTools)
set.seed(3000)
spl = sample.split(data.frame$Survived, SplitRatio = 0.7)
Train = subset(data.frame, spl==TRUE)
Test = subset(data.frame, spl==FALSE)
library(rpart)
library("rpart.plot")
fit = rpart(Survived~., data = Train, method = 'class')
rpart.plot(fit, extra = 0)

predicted = predict(fit, Test, type = 'class')
table = table(Test$Survived, predicted)
y_true = Test$Survived
y_pred = predicted

library(mosaicrml)
#library(mosaicml)

# Make predictions
#PredictForest = predict(StevensForest, newdata = Test)

# Make predictions
score <- function(fit, request_path){
  stevens <- read.csv(request_path)
  stevens = select(stevens, Survived, Pclass, Age, Sex, SibSp, Parch)
  stevens$Survived = factor(stevens$Survived)
  stevens$Pclass = factor(stevens$Pclass, order=TRUE, levels = c(3, 2, 1))
  
  #bet <- read.table(request_path)
  PredictForest <- predict(fit, newdata = stevens)
  return (toJSON(PredictForest))
}
library(reticulate)
library(devtools)
library(randomForest)
library(rjson)


help(fit)
help(predict_proba)
predict_prob <- predict(fit, Test, type="prob")


value <- register_model(
  fit,
  score,
  name="Titanicdatata",
  description="R Model",
  flavour="r",
  input_type="file",
  y_true=y_true,
  y_pred=y_pred,
  prob=predict_prob,
  labels=list("survived","not-survived"),
  model_type="classification",
  )