from domainRetriever import retrieveDomains
from runLSTM import buildRunLSTM
import pickle

"""
a = retrieveDomains() 
generated_data = a.gen_train_test_data()
a.save_data(generated_data)
"""

with open("data/traindata_01.pkl", "rb") as input_file:
    generated_data = pickle.load(input_file)


list_tuples = [x for x in generated_data]


b = buildRunLSTM()
X, y, max_features, maxlen, labels = b.read_data(list_tuples)

print(max_features, maxlen)

final_data = b.run_model(X, y, max_features, maxlen, labels)