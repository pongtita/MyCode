# ML_Trees_03 script
# This is the third script for the Machine Learning R workshop
# This script creates our first tree and plots it 
#  This script assumes you loaded the german and packages rpart and rpart.plot
#  
# MR 4/20/18

# this command creates a model object called credit_model and 
#  assigns to it the result of the rpart command

credit_model <- rpart(formula=V21~., data=german, method='class')
# Formula in the function tells it what the objective is
# Here the objective is to predict V21, which is variable that
#   tells us if the customer defaulted on debt or not
# The dataset we are using is called german, so data=german
# The method tells rpart whether it should use regression 
#   or classification techniques. We are classifyinig default or 
#   not, so we use 'class'

# Now look at a summary of the model created:
summary(credit_model)

# Now create a diagram of the model
rpart.plot(credit_model)

