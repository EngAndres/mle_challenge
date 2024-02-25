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

In this case the process is simple.
First, some docstrigs are added just to be alligned with _pylint_ verification.
After, in the predict service next steps had been made:

- Receive body data as a dict, and convert into a dataframe
- Call predict function from the ML model, and save the list predictions in memory
- Create a response dict with the expected key and the list as value
- Return the response

## Part III

This step was pretty simple. After setup __GCP account__, some secrets are defined into __Github__ to avoid the exposure of sensible credentials data.
Then, after a first deployment running, API url is defined into GCP. With this information, _Makefile_ is updated with API url.
Some tests are performe to check API functionality.

## Part IV

In this part, first a __.github__ folder is created, and inside there the __workflows__ folder is copied.

Then, _ci.yml_ file is changed in a simple way. Every time a PR is send to main branch, this
part of the gitflow is activated. The idea is to check the code using python 3.8, just to use
a recent and very stable version. 
Requirements are installed, adding __pylint__ and __black__ just to add both quiality code
and formatter validation for code in order to keep good code practices, good standards, 
independing of the developer. After, using makefile commands some test are scheduled. Finally,
some commands to generate Docket image and deployed in register container in GoogleCloud are
added. In this way, CI validate code quality, perform tests, and deploy image to cloud.

In _cd.yml_ file a similar pipeline is created. Using python 3.8, dependencies had been installed, then some tests using makefiles commands had been performed.
Then, some commands to setup cloud access and deploy a new API version using cloud run are
added. In this way, CD perform tests, and deploy a new API version to be tested using a tool
like __postman__.

Finally, Dockerfile is changed just to generate a container image with the app with 
basic requirements installed, and exposed in __port 80__ to make simple the servling of the model in the cloud run instance.
