import numpy as np
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers.core import Dense
from keras.layers.core import Dropout
from keras.layers.core import Activation
# softmax activation for multi-class classification
# sigmoid activation function for binary classification

from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM
import sklearn
from sklearn.cross_validation import train_test_split
import pickle


class buildRunLSTM(object):

	def build_bin_model(self, max_features, maxlen):
		"""buiilding the binary classification model with sigmoid activation"""
		model = Sequential()
		model.add(Embedding(max_features, 128, input_length=maxlen))

		model.add(LSTM(128))
		model.add(Dropout(0.5))
		model.add(Dense(1))
		model.add(Activation("sigmoid"))

		model.compile(loss="binary_crossentropy", optimizer="rmsprop")
		# to-do: test the performance of different optimizers

		return model

	def build_multi_model(self, max_features, maxlen):
		"""building the multiclassification model with softmax activation function)"""
		model = Sequential()
		model.add(Embedding(max_features, 128, input_length=maxlen))

		model.add(LSTM(128))
		model.add(Dropout(0.5))
		model.add(Dense(1))
		model.add(Activation("softmax"))

		model.complile(loss="categorical_crossentropy", optimizer="rmsprop")
		# to-do: test the performance of different optimizers

		return model


	def read_data(self, list_tuples):
		"""
		incoming data is list of tuples:
		[(domain1, label1), (domain2, label2), ... ]
		"""

		# need to create a holder because zip in python is a generator


		X = [x[0] for x in list_tuples]

		labels = [x[1] for x in list_tuples]

		# generate dict for valid characters
		valid_chars = {x: idx + 1 for idx, x in enumerate(set(''.join(X)))}

		max_features = len(valid_chars) + 1
		maxlen = np.max([len(x) for x in X])

		# convert characters to index and pad them

		X = [[valid_chars[y] for y in x] for x in X]
		X = sequence.pad_sequences(X, maxlen = maxlen)
		y = [0 if x == 'benign' else 1 for x in labels]

		return X, y, max_features, maxlen, labels


	def run_model(self, X, y, max_features, maxlen, labels): 
		"""define parameters here"""
		max_epoch = 25
		nfolds = 10
		batch_size = 128

		#X, y, max_features, maxlen, labels = self.read_data(list_tuples)

		#print (max_features, maxlen)

		final_data = []

		for fold in range(nfolds):
			print ("fold %u/%u" % (fold+1, nfolds))
			
			X_train, X_test, y_train, y_test, _, label_test = train_test_split(X, y, labels, test_size=0.2)

			model = self.build_bin_model(max_features, maxlen)

			#divide training set into k folds and then training the model k times, each time leaving a different
			#fold out of the training data and using as validation set
			#performance metric is averaged across all k tests

			X_train, X_holdout, y_train, y_holdout = train_test_split(X_train, y_train, test_size=0.05)

			best_iter = -1
			best_auc = 0.0
			out_data = {}

			for ep in range(max_epoch):
				#for each epoch get auc, if auc is better than previous, use model parameters 
				#to predict for the true X_test
				model.fit(X_train, y_train, batch_size=batch_size, nb_epoch=1)

				t_probs = model.predict_proba(X_holdout)

				t_auc = sklearn.metrics.roc_auc_score(y_holdout, t_probs)

				print ('Epoch %d: auc = %f (best=%f)' % (ep, t_auc, best_auc))

				if t_auc > best_auc:

					best_auc = t_auc

					best_iter = ep

					probs = model.predict_proba(X_test)

					out_data = {'y':y_test, 'labels': label_test, 'probs':probs, 'epochs': ep, 'confusion_matrix': sklearn.metrics.confusion_matrix(y_test, probs > .5)}

					print (sklearn.metrics.confusion_matrix(y_test, probs > .5))

				else:
					if (ep-best_iter) > 2:
						break

			final_data.append(out_data)

		model.save('data/lstm_dga_01.h5')
		DATA_FILE = 'data/lstm_dga_01.pkl'
		pickle.dump(final_data, open(DATA_FILE, 'wb'))

		return final_data