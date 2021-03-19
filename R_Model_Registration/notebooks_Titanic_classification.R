# Titanic data Analysis 

#install.packages(c("GGally","rpart.plot"))


install.packages("rpart.plot")
install.packages("randomForest")
install.packages("GGally")

library(ggplot2)
library(dplyr)
library(GGally)
library(rpart)
library(rpart.plot)
library(randomForest)


# I loaded the data:

test <- read.csv('/data/titanic_test.csv',stringsAsFactors = FALSE)
train <- read.csv('/data/titanic_train.csv', stringsAsFactors = FALSE)

# Creating a new data set with both the test and the train sets
full <- bind_rows(train,test)
LT=dim(train)[1]
# Checking the structure
str(full)

# Missing values
colSums(is.na(full))

colSums(full=="")

# We have a lot of missing data in the Age feature (263/1309)
# Let's change the empty strings in Embarked to the first choice "C"
full$Embarked[full$Embarked==""]="C"

# Let's see how many features we can move to factors
apply(full,2, function(x) length(unique(x)))


# Let's move the features Survived, Pclass, Sex, Embarked to be factors
cols<-c("Survived","Pclass","Sex","Embarked")
for (i in cols){
  full[,i] <- as.factor(full[,i])
}

# Now lets look on the structure of the full data set
str(full)

# First, let's look at the relationship between Gender and survival:
ggplot(data=full[1:LT,],aes(x=Sex,fill=Survived))+geom_bar()


# Survival as a function of Embarked:
ggplot(data = full[1:LT,],aes(x=Embarked,fill=Survived))+geom_bar(position="fill")+ylab("Frequency")

t<-table(full[1:LT,]$Embarked,full[1:LT,]$Survived)
for (i in 1:dim(t)[1]){
  t[i,]<-t[i,]/sum(t[i,])*100
}
t

#It looks that you have a better chance to survive if you Embarked in 'C' (55% compared to 33% and 38%).

# Survival as a function of Pclass:
ggplot(data = full[1:LT,],aes(x=Pclass,fill=Survived))+geom_bar(position="fill")+ylab("Frequency")


# It looks like you have a better chance to survive if you in lower ticket class.
# Now, let's devide the graph of Embarked by Pclass:
ggplot(data = full[1:LT,],aes(x=Embarked,fill=Survived))+geom_bar(position="fill")+facet_wrap(~Pclass)


###############################################################

# Extra Features created using original features

# There are a lot of missing values in the Age feature, so I'll put the mean instead of the missing values.
full$Age[is.na(full$Age)] <- mean(full$Age,na.rm=T)
sum(is.na(full$Age))


# The title of the passanger can affect his survive:
full$Title <- gsub('(.*, )|(\\..*)', '', full$Name)
full$Title[full$Title == 'Mlle']<- 'Miss' 
full$Title[full$Title == 'Ms']<- 'Miss'
full$Title[full$Title == 'Mme']<- 'Mrs' 
full$Title[full$Title == 'Lady']<- 'Miss'
full$Title[full$Title == 'Dona']<- 'Miss'
officer<- c('Capt','Col','Don','Dr','Jonkheer','Major','Rev','Sir','the Countess')
full$Title[full$Title %in% officer]<-'Officer'

full$Title<- as.factor(full$Title)

ggplot(data = full[1:LT,],aes(x=Title,fill=Survived))+geom_bar(position="fill")+ylab("Frequency")



###############################################################


# titanic_data = full[1:LT,c("Survived","Pclass","Sex","Age","Fare","SibSp","Parch","Title")]
# 
# # Make example data
# X = select(titanic_data, Pclass,Sex,Age,Fare,SibSp,Parch,Title)
# y = titanic_data["Survived"] 
# 
# library(caret)
# 
# #Extract random sample of indices for test data
# set.seed(42) #equivalent to python's random_state arg
# test_inds = createDataPartition(y = y, p = 0.2, list = F) 
# 
# # Split data into test/train using indices
# X_test = X[test_inds, ]; y_test = y[test_inds] 
# X_train = X[-test_inds, ]; y_train = y[-test_inds]
# 


###############################################################
# Models

## Logistic Regression

# The train set with the important features 
train_im<- full[1:LT,c("Survived","Pclass","Sex","Age","Fare","SibSp","Parch","Title")]

ind<-sample(1:dim(train_im)[1],500) # Sample of 500 out of 891
train<-train_im[ind,] # The train set of the model
test<-train_im[-ind,] # The test set of the model

# Let's try to run a logistic regression
model <- glm(Survived ~.,family=binomial(link='logit'),data=train)
summary(model)

# We can see that SibSp, Parch and Fare are not statisticaly significant. 
# Let's look at the prediction of this model on the test set (train2):
y_prob <- predict(model,test)
y_pred <- ifelse(y_prob > 0.5,1,0)
# Mean of the true prediction 
y_true = test$Survived
mean(y_pred==y_true)

X_train = train[c("Pclass",  "Sex", "Age", "Fare", "SibSp", "Parch", "Title")]
Y_train = train[c("Survived")]



t1<-table(y_pred,y_true)
# Presicion and recall of the model
presicion<- t1[1,1]/(sum(t1[1,]))
recall<- t1[1,1]/(sum(t1[,1]))
presicion
recall

# # F1 score on the initial test set is 0.871. This pretty good.
# 
# # Let's run it on the test set:
# 
# test_im<-full[LT+1:1309,c("Pclass","Sex","Age","SibSp","Parch","Fare","Title")]
# 
# pred.test <- predict(model,test_im)[1:418]
# pred.test <- ifelse(pred.test > 0.5,1,0)
# res<- data.frame(test$PassengerId,pred.test)
# names(res)<-c("PassengerId","Survived")
# write.csv(res,file="res.csv",row.names = F)
# 
# score <- function(model, input) { print( input)}
# 
# library(mosaicrml)
# 
# register_model()
# 
###########################################################


score <- function(model, request_path){
  new_data <- read.csv(request_path)
  predicted_values <- predict(model, newdata = new_data)
  return (toJSON(predicted_values))
}
print("EOC")
library(mosaicrml)
# library(mosaicml)
### Register Model




value <- register_model(
  model,
  score,
  name="Titanic_Classification_Model_Using_R",
  description="Titanic_Classification_Model_Using_R",
  flavour="r",
  input_type="json",
  #explain_ai=TRUE, #  It enables explain_ai feature
  #kyd= TRUE,
  #kyd_score = TRUE,
  #x_train=X_train, # training data of model with feature column
  #y_train=Y_train, # training data of model with target column
  y_true=y_test, # y_true = y_test # test data of model with feature column
  y_pred=y_pred, # predicted values from model
  prob = y_prob, # prabability score
  model_type = "classification",
  #model_display = TRUE,
  #feature_names = c("Pclass","Sex","Age","SibSp","Parch","Fare","Title"),
  #target_names = c("Survived")
)
value









