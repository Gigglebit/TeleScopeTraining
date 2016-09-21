import numpy as np
import pandas as pd 
from sklearn import preprocessing,cross_validation,neighbors,svm
import sys

#import pickle ##used for save the trained classifier
#from sklearn.externals import joblib

df=pd.read_csv(sys.argv[1])
df.columns=['mean_rate','sigma1','sigma2','sigma4','sigma8','sigma16','duration','class']
#df.replace('nan',-99999,inplace=True)
#df.drop(['id'],1,inplace=True)

#df = pd.DataFrame(data, index = ['Cochice', 'Pima', 'Santa Cruz', 'Maricopa', 'Yuma'])
# df.columns = ['a', 'b'] to change the labels name
#

X=np.array(df.drop(['class'],1))
y=np.array(df['class'])


X_train,X_test,y_train,y_test=cross_validation.train_test_split(X,y,test_size=0.2)

#SVC() support vector classifier
#svm.linearSVC()
#svm.SVC(kernel='linear') svm.SVC(kernel='rbf')
clf=svm.SVC(kernel='linear')
#X_train,y_train must be an numpy array
#np.reshape() , change the form of 2d list,
#eg. np.array([[1,2,3],[4,5,6]]).reshape(3,-1) #-1 means inferred from the dataset
#we get [[1,2],[3,4],[5,6]]
clf.fit(X_train,y_train)

prediction=clf.predict(X_test)
print('actual value:{}'.format(y_test))
print('prediction:{}'.format(prediction))
#predict()
#clf.predict(X_test), and get the test result 

accuracy=clf.score(X_test,y_test)
print('accuracy:{}'.format(accuracy))


#s=pickle.dumps(clf)
#
