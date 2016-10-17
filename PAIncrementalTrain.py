from sklearn.linear_model import SGDClassifier
import numpy as np
import pandas as pd 
from sklearn import preprocessing,cross_validation,neighbors,svm
import sys
from sklearn.model_selection import cross_val_predict
from sklearn import metrics
from sklearn.model_selection import StratifiedKFold
import sklearn



df=pd.read_csv(sys.argv[1])
#'mean_rate', try without mean_rate
df.columns=['sigma1','sigma2','sigma4','sigma8','sigma16','duration','class']

X=np.array(df.drop(['class'],1))
y=np.array(df['class'])

#X_train,X_t,y_train,y_t=cross_validation.train_test_split(X,y,test_size=0.2)
X_train,X_train2,y_train,y_train2=cross_validation.train_test_split(X,y,test_size=0.2)

df2=pd.read_csv(sys.argv[2])
df2.columns=['sigma1','sigma2','sigma4','sigma8','sigma16','duration','class']
X2=np.array(df.drop(['class'],1))
y2=np.array(df['class'])


C_2d_range = [1e-2,1e-1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2,3,4,5,6,7,
8,9,1e1,1e2]

## could try to set warm_start=True
#clf = SGDClassifier(loss="hinge", penalty="l2",n_iter=5)
# clf = sklearn.linear_model.PassiveAggressiveClassifier(C=1.0,loss="hinge")
# clf.fit(X_train, y_train)

for C in C_2d_range:
	clf = sklearn.linear_model.PassiveAggressiveClassifier(C=C,loss="hinge",n_iter=5000)
	#clf.fit(X_train, y_train)
	clf.fit(X_train,y_train)
	clf.partial_fit(X_train2,y_train2)

	# skf = StratifiedKFold(n_splits=10)
	# tempCount=0
	# for train, test in skf.split(X, y):
	# 	X_train, X_test, y_train, y_test = X[train], X[test], y[train], y[test]
	# 	if(tempCount==0):
	# 		clf.fit(X_train,y_train)
	# 	else:
	# 		clf.partial_fit(X_train,y_train)
	# 	tempCount+=1
		# accuracy += clf.score(X_test,y_test)
		# count+=1
	#accuracy=accuracy/count
	print("C=",C)
	#accuracy = clf.score(X_test,y_test)
	accuracy = clf.score(X2,y2)
	print('accuracy:{}'.format(accuracy))

# skf = StratifiedKFold(n_splits=10)
# accuracy=0
# count=0
# for train, test in skf.split(X, y):
# 	X_train, X_test, y_train, y_test = X[train], X[test], y[train], y[test]
# 	clf.partial_fit(X_train,y_train)
# 	# accuracy += clf.score(X_test,y_test)
# 	# count+=1

# #accuracy=accuracy/count
# accuracy = clf.score(X_test,y_test)
# print('accuracy:{}'.format(accuracy))












