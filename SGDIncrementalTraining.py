from sklearn.linear_model import SGDClassifier
import numpy as np
import pandas as pd 
from sklearn import preprocessing,cross_validation,neighbors,svm
import sys
from sklearn.model_selection import cross_val_predict
from sklearn import metrics
from sklearn.model_selection import StratifiedKFold



df=pd.read_csv(sys.argv[1])
#'mean_rate', try without mean_rate
df.columns=['sigma1','sigma2','sigma4','sigma8','sigma16','duration','class']

X=np.array(df.drop(['class'],1))
y=np.array(df['class'])

#X_train,X_test,y_train,y_test=cross_validation.train_test_split(X,y,test_size=0.2)
X_train,X_train2,y_train,y_train2=cross_validation.train_test_split(X,y,test_size=0.2)

df2=pd.read_csv(sys.argv[2])
df2.columns=['sigma1','sigma2','sigma4','sigma8','sigma16','duration','class']
X2=np.array(df.drop(['class'],1))
y2=np.array(df['class'])


## could try to set warm_start=True
# The default SGDClassifier n_iter is 5 meaning you do 5 * num_rows steps in weight space. 
#The sklearn rule of thumb is ~ 1 million steps for typical data
clf = SGDClassifier(loss="hinge", penalty="l2",n_iter=10000)
clf.fit(X_train, y_train)

clf.partial_fit(X_train2,y_train2)
# skf = StratifiedKFold(n_splits=10)
# accuracy=0
# count=0
# for train, test in skf.split(X, y):
# 	X_train, X_test, y_train, y_test = X[train], X[test], y[train], y[test]
# 	clf.partial_fit(X_train,y_train)
	# accuracy+=clf.score(X_test,y_test)
	# count+=1

accuracy=clf.score(X2,y2)
#accuracy=accuracy/count
print('accuracy:{}'.format(accuracy))












