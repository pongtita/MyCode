# ML_Trees_04 script
# This is the fourth script for the Machine Learning R workshop
# This script divides our data into a training set and a testing set
#  
# MR 4/20/18


# Create integer for number of rows in our dataset german
# Yes, I know it has 1000 and don't really need to do this. 
# Pretend you didn't know it because often you will not.
n <- nrow(german)

# Create an integer for the number of rows in 80% of the data. 
# We use round to ensure it is an integer
n_train <- round(0.80 * n)

# Create a vector of indices which is an 80% random sample
# First we set the seed to guarantee reproducible results
#   the seed determines the random number that is generated
set.seed(123)
# This command draws n_train random integers from the range of 1 to n
train_indices <- sample(1:n, n_train) 

# Create subsets of the data 
german_train <- german[train_indices,]
german_test <- german[-train_indices,]