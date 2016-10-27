import numpy as np
import pandas as pd 
# from sklearn import preprocessing,cross_validation,neighbors,svm
import sys
# from sklearn.model_selection import cross_val_predict
# from sklearn import metrics
# from sklearn.model_selection import StratifiedKFold

#import pickle ##used for save the trained classifier
#from sklearn.externals import joblib


## it links to JVM, so must do it before anything
import weka.core.jvm as jvm
jvm.start()


from weka.core.converters import Loader, Saver
loader = Loader(classname="weka.core.converters.ArffLoader")
data = loader.load_file("27102016815pmTrainingSet.arff")

loader2 = Loader(classname="weka.core.converters.ArffLoader")
dataTestResolutionChange = loader2.load_file("learnTest.arff")

#import weka.core.converters as converters
#data = converters.load_any_file("27102016815pmTrainingSet.arff")
# data=pd.read_csv(sys.argv[1])
# data.columns=['mean_rate','sigma1','sigma2','sigma4','sigma8','sigma16','flowCount','class']

#data=pd.read_csv(sys.argv[1])
#'mean_rate', try without mean_rate
#,'duration'
#data.columns=['mean_rate','sigma1','sigma2','sigma4','sigma8','sigma16','flowCount','class']
#df.replace('nan',-99999,inplace=True)
#df.drop(['id'],1,inplace=True)

from weka.classifiers import Classifier, Evaluation
from weka.core.classes import Random
#data = ...             # previously loaded data
data.class_is_last()   # set class attribute
dataTestResolutionChange.class_is_last()

classifier = Classifier(classname="weka.classifiers.trees.J48", options=["-C", "0.3"])
# evaluation = Evaluation(data)                     # initialize with priors
# evaluation.crossvalidate_model(classifier, iris_data, 10, Random(42))  # 10-fold CV
classifier.build_classifier(data)

for index, inst in enumerate(dataTestResolutionChange):
     pred = classifier.classify_instance(inst)
     dist = classifier.distribution_for_instance(inst)

     print str(pred)
     #print index
     print inst

     print(str(index+1) + ": label index=" + str(pred) + ", class distribution=" + str(dist))
# print(evaluation.summary())
# print("pctCorrect: " + str(evaluation.percent_correct))
# print("incorrect: " + str(evaluation.incorrect))


jvm.stop()




