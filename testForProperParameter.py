import numpy as np
import pandas as pd 
from sklearn import preprocessing,cross_validation,neighbors,svm
import sys
from sklearn.model_selection import cross_val_predict
from sklearn import metrics
from sklearn.model_selection import StratifiedKFold

#import pickle ##used for save the trained classifier
#from sklearn.externals import joblib

df=pd.read_csv(sys.argv[1])
#'mean_rate', try without mean_rate
df.columns=['sigma1','sigma2','sigma4','sigma8','sigma16','duration','class']
#df.replace('nan',-99999,inplace=True)
#df.drop(['id'],1,inplace=True)

# df.columns = ['a', 'b'] to change the labels name
#

X=np.array(df.drop(['class'],1))
y=np.array(df['class'])

#need to use cross_validation so comment it
X_train,X_test,y_train,y_test=cross_validation.train_test_split(X,y,test_size=0.2)

#SVC() support vector classifier
#svm.linearSVC()
#svm.SVC(kernel='linear') svm.SVC(kernel='rbf')
#clf=svm.SVC(kernel='linear')
#clf=svm.SVC(kernel='rbf')
#clf = svm.SVC()
#clf = svm.LinearSVC() # the default for LinearSVC is one vs rest
#clf = svm.SVC(decision_function_shape='ovo') ## one vs one
#clf = svm.LinearSVC(multi_class='crammer_singer')
#X_train,y_train must be an numpy array
#np.reshape() , change the form of 2d list,
#eg. np.array([[1,2,3],[4,5,6]]).reshape(3,-1) #-1 means inferred from the dataset
#we get [[1,2],[3,4],[5,6]]

################test for the two key 
# the gamma parameter defines how far the influence of a single training example reaches, 
# with low values meaning 'far' and high values meaning 'close'. The gamma parameters can be seen 
# as the inverse of the radius of influence of samples selected by the model as support vectors.

# The C parameter trades off misclassification of training examples against simplicity of the 
# decision surface. A low C makes the decision surface smooth, while a high C aims at classifying 
# all training examples correctly by giving the model freedom to select more samples as support vectors.

# skf = StratifiedKFold(n_splits=10)
# accuracy=0
# for train, test in skf.split(X, y):
# 	X_train, X_test, y_train, y_test = X[train], X[test], y[train], y[test]
# 	clf = svm.SVC(C=0.01,kernel='linear',decision_function_shape='ovo')
# 	clf.fit(X_train,y_train)
# 	accuracy+=clf.score(X_test,y_test)
# print(accuracy/10)


###############find the optimal C value, for the parameter
C_2d_range = [1e-2,1e-1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2,3,4,5,6,7,
8,9,1e1,1e2]
gamma_2d_range = [1e-1,0.5, 1,1.5,1e1]
classifiers = []
for C in C_2d_range:
    #for gamma in gamma_2d_range:
	#,class_weight={1:0.5,2:0.5,3:1}
    clf = svm.SVC(C=C,kernel='linear',decision_function_shape='ovo')
    #clf = svm.SVC(C=C,gamma=gamma,kernel='rbf',decision_function_shape='ovo')
    #clf=svm.LinearSVC(C=C,multi_class='ovr')
    # predicted = cross_val_predict(clf, X, y, cv=10)
    # temp=metrics.accuracy_score(y, predicted) 
    # print(temp)
    clf.fit(X_train,y_train)
    classifiers.append((C, clf))
    prediction=clf.predict(X_test)
    print("#######################")
    print(C)
    print('actual value:{}'.format(y_test))
    print('prediction:{}'.format(prediction))
    accuracy=clf.score(X_test,y_test)
    print('accuracy:{}'.format(accuracy))


### ovo is better than ovr
### linear is better


##########test for poly and rbf
# C_2d_range = [1e-2,1e-1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2,3,4,5,6,7,
# 8,9,1e1,1e2]
# #1e-1,0.5, 1,1.5,
# gamma_2d_range = [2,5,1e1,1e2]
# classifiers = []
# for C in C_2d_range:
#     for gamma in gamma_2d_range:
# 		#,class_weight={1:0.5,2:0.5,3:1}
# 	    #clf = svm.SVC(C=C,kernel='linear',decision_function_shape='ovo')
# 	    clf = svm.SVC(C=C,gamma=gamma,kernel='poly',decision_function_shape='ovo',degree=5)
# 	    #clf=svm.LinearSVC(C=C,multi_class='ovr')
# 	    # predicted = cross_val_predict(clf, X, y, cv=10)
# 	    # temp=metrics.accuracy_score(y, predicted) 
# 	    # print(temp)
# 	    clf.fit(X_train,y_train)
# 	    classifiers.append((C, gamma,clf))
# 	    prediction=clf.predict(X_test)
# 	    print("#######################")
# 	    print(C)
# 	    print('actual value:{}'.format(y_test))
# 	    print('prediction:{}'.format(prediction))
# 	    accuracy=clf.score(X_test,y_test)
# 	    print('accuracy:{}'.format(accuracy))

# clf.fit(X_train,y_train)

# prediction=clf.predict(X_test)
# print('actual value:{}'.format(y_test))
# print('prediction:{}'.format(prediction))
# #predict()
# #clf.predict(X_test), and get the test result 

# accuracy=clf.score(X_test,y_test)
# print('accuracy:{}'.format(accuracy))


#s=pickle.dumps(clf)
#


# ###for visualization
# plt.figure(figsize=(8, 6))
# xx, yy = np.meshgrid(np.linspace(-3, 3, 200), np.linspace(-3, 3, 200))
# for (k, (C, gamma, clf)) in enumerate(classifiers):
#     # evaluate decision function in a grid
#     Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
#     Z = Z.reshape(xx.shape)

#     # visualize decision function for these parameters
#     plt.subplot(len(C_2d_range), len(gamma_2d_range), k + 1)
#     plt.title("gamma=10^%d, C=10^%d" % (np.log10(gamma), np.log10(C)),
#               size='medium')

#     # visualize parameter's effect on decision function
#     plt.pcolormesh(xx, yy, -Z, cmap=plt.cm.RdBu)
#     plt.scatter(X_2d[:, 0], X_2d[:, 1], c=y_2d, cmap=plt.cm.RdBu_r)
#     plt.xticks(())
#     plt.yticks(())
#     plt.axis('tight')

# scores = grid.cv_results_['mean_test_score'].reshape(len(C_range),
#                                                      len(gamma_range))

# # Draw heatmap of the validation accuracy as a function of gamma and C
# #
# # The score are encoded as colors with the hot colormap which varies from dark
# # red to bright yellow. As the most interesting scores are all located in the
# # 0.92 to 0.97 range we use a custom normalizer to set the mid-point to 0.92 so
# # as to make it easier to visualize the small variations of score values in the
# # interesting range while not brutally collapsing all the low score values to
# # the same color.

# plt.figure(figsize=(8, 6))
# plt.subplots_adjust(left=.2, right=0.95, bottom=0.15, top=0.95)
# plt.imshow(scores, interpolation='nearest', cmap=plt.cm.hot,
#            norm=MidpointNormalize(vmin=0.2, midpoint=0.92))
# plt.xlabel('gamma')
# plt.ylabel('C')
# plt.colorbar()
# plt.xticks(np.arange(len(gamma_range)), gamma_range, rotation=45)
# plt.yticks(np.arange(len(C_range)), C_range)
# plt.title('Validation accuracy')
# plt.show()