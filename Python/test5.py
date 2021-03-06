# -*- coding: utf-8 -*- 

# MLP, word frequency/word occurancy using grid search

from sklearn.datasets import load_files
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer
import numpy as np
# New library: Multi Layer Perceptron
from sklearn.neural_network import MLPClassifier
# from sklearn import metrics
# New library: GridSearchCV to optimize the SVM classifier
# from sklearn.grid_search import GridSearchCV

# Dictionary containing the paths of the training (as key) and test (as value): {train1:test1, train2:test2}
files = {'/veu4/usuaris30/speech00/corpus/train/spanishlit_ninc_v1': ['/veu4/usuaris30/speech00/corpus/testc/spanishlit_ninc_v1', 'Not all books in training corpus']}#, 
	#'/veu4/usuaris30/speech00/corpus/train/spanishlit_inc_v1': ['/veu4/usuaris30/speech00/corpus/testc/spanishlit_inc_v1', 'All books in training corpus']}


# Do we consider 'lope'?
inp = raw_input('Do you want to consider Lope de Vega, Calderon de la Barca or both [l/c/b]? ')
if inp == 'l':
	all_categ = ['cervantes', 'garcia', 'lope', 'perez', 'pardo','quevedo']
elif inp == 'c':
	all_categ = ['calderon', 'cervantes', 'garcia', 'perez', 'pardo','quevedo']
elif inp == 'b':
	all_categ = ['calderon','cervantes','garcia','perez','pardo','lope','quevedo']
	#all_categ = ['calderon', 'cervantes', 'garcia', 'lope', 'perez', 'pardo']

# Iterate for all train-test pair
for file in files:
	print "-----------------------------"
	print files[file][1]

	# Initial considered category
	categ = ['becquer'] 

	# Loop considering from 2 to 7 labelings
	for newcateg in all_categ:
		# Add new category
		categ.append(newcateg)

		# Classifier definition using Pipeline
		classifier = Pipeline([('vect', CountVectorizer()),('clf', MLPClassifier(algorithm='l-bfgs', alpha=1e-5, hidden_layer_sizes=(15,), random_state=1))])
		#parameters = {'vect__ngram_range': [(1, 1), (1, 2)], 'clf__alpha': (1e-2, 1e-3)}

		# LOAD THE TRAINING CORPUS
		text_train_subset = load_files(file, description = 'Training: Some extracts of spanish literature books', 
			categories = categ, load_content = True, encoding = 'utf-8', shuffle = False)
		
		# Train the SVM classifier using the training set
		classifier = classifier.fit(text_train_subset.data, text_train_subset.target)
		# Find the best parameters using GridSearch
		#classifier = GridSearchCV(classifier, parameters, n_jobs=10)
		# Train again the SVM classifier with the resulting "optimal" parameters
		#classifier = classifier.fit(text_train_subset.data, text_train_subset.target)

		# LOAD THE TEST CORPUS
		text_test_subset = load_files(files[file][0], description = 'Test: Some extracts of spanish literature books', 
			categories = categ, load_content = True, encoding = 'utf-8', shuffle = False)

		# Print the considered categories
		print "> Categories:", categ
		# Print table containing recall, precision, f1 score etc. using the target, the target_names and the prediction done by the classifier
		#print(metrics.classification_report(text_test_subset.target, classifier.predict(text_test_subset.data),target_names=text_test_subset.target_names))
		# Print the performance of the classifier using the test set (data and labels)
		print(">> Testing score: {0:.1f}%".format(classifier.score(text_test_subset.data, text_test_subset.target) * 100)), "\n" 

# grep -c ^processor /proc/cpuinfo
# Detected conflict: Lope de Vega and Calderon de la Barca (note that both belong to barroc theater in 16/17 century)
