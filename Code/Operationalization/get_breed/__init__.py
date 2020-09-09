from sklearn.externals import joblib
import pickle

model_file = 'C:/Users/cammy/OneDrive/MIT IA/git/mit_data_science/Data/Modeling/trained_models.jbl'


# Loading models at the service initialization
if 'globalTrainResults' not in dir():
    print('READING MODELS FROM ', model_file)
    with open(model_file, 'rb') as fid:
        globalTrainResults = pickle.load(fid)
