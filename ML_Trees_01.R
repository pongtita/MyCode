# ML_Trees_01 script
# This is the first script for the Machine Learning R workshop
# This script installs rpart using the library function 
#  and examines the dataset. This script assumes you loaded the 
#  dataset using the 'import dataset' button (GUI)
# MR 4/20/18

# The str(dataobject) function in R is very good for showing
#  you what the data looks like. I use it instead of head

# The following line displays some summary statistics about the 
#  german dataset. 
# The dataset must be loaded, or you will get an error when running 
#  this script
str(german)

# This command loads the rpart package into the library. 
# You must load the package before using it
library(rpart)
# If this command produced an error, try installing the package first



