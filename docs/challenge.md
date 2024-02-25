# Challenge

This is a MLE challenge. In this document some details about both techical decisiones and implementations had been provided.

This challenge is solved in four different steps. As follows, some details for each step will be defined:

## Part I

For preprocessing different methods are created, each one per each new feature. Into preproces funtion this methods are called, and features and target dataset defined. In a 
method called train_model all preprocess and fit callings are orchestrated. This train_model
is called in the constructor of the class. 

In fit model a model is choosed and fit based on features and target variable.
In this case, a XGBoost model with Balance is choosed based on next reasons: (i) XGBoost is a pretty good strategy for tabular data, avoiding overfitting problems and with good performance in a lot of contests in Kaggle, for example. Also, as data is unbalanced, and
could still continuous umbalanced, it is a good option to adjust for a unbalanced data respect of target variable, and try to increase metrics as F1-score in this case.

In predict funtion it is pretty simple, just send features and return predictions.

## Part II


## Part III


## Part IV