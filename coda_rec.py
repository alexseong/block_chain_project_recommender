import tensorflow as tf
import tensorrec as tr
import numpy as np
import matplotlib.pyplot as plt
import tensorrec_util
import pandas as pd

class CodaRecommender(object):
    
    def __init__(self):
        self._features = None
        self._model = None
        self._investor_dic = None
        self._project_dic = None
        self._investor_features = None
        self._project_features = None
        self._interaction_data = None
        self._prediction = None

    def data_preparation(self, feature_data_path):
        features = pd.read_csv(feature_data_path, header=0)
        features = features.iloc[:,0]
        self._features = features 

        interaction_data, investor_features, project_features = \
            tensorrec_util.generate_dummy_project_data(num_investors=1500, 
	    					       num_projects=1000, 
						       interaction_density=0.5, 
						       n_features=features.size) 
        self._interaction_data = interaction_data
        self._investor_features = investor_features
        self._project_features = project_features
 
        investor_dic = {}
        for i in range(investor_features.shape[0]):
            investor_dic[i] = "Investor_" + str(i) 
        self._investor_dic = investor_dic

        project_dic = {}
        for i in range(project_features.shape[0]):
            project_dic[i] = "PROJECT_" + str(i)
        self._project_dic = project_dic

    def model_train(self, epochs=200, verbose=True):
        model = tr.TensorRec()
        model.fit(self._interaction_data, self._investor_features, self._project_features, epochs=epochs, verbose=verbose) 
        self._model = model

    def predict(self):
        self._predictions = self._model.predict(user_features=self._investor_features, item_features=self._project_features)

    def recommend_projects(self):
        var = ""

        while(var != 'q' and var != 'Q'):
            var = raw_input("Enter a investor number: ('q' to quit)")

            if var.isdigit():
                investor_num = int(var.strip())
                i_f = self._investor_features[investor_num]
                _, non_zero_features = i_f.nonzero()

                print "Investor Name: " + self._investor_dic[investor_num]

                for i in non_zero_features:
                    print("    " + self._features[i])

                args = np.argsort(self._predictions[investor_num])
                print ""
                print "[Recommended project list: ]"

                top_5_projects = args[::-1][:5]
                rank = 0

                for i in top_5_projects:
                    rank += 1
                    print "[" + str(rank) + "] "+ self._project_dic[i]
                    p_f = self._project_features[i]
                    _, non_zero_features = p_f.nonzero()

                    for p in non_zero_features:
                        print "    ", self._features[p]
                    print ""
            else:
                print("Please enter a valid investor number or 'q/Q'")

def main():
    feature_data_path = "data/coin_project.csv"
    rec_model = CodaRecommender()
    rec_model.data_preparation(feature_data_path)
    rec_model.model_train(epochs=50)
    rec_model.predict()
    rec_model.recommend_projects()


if __name__ == "__main__":
    main()
