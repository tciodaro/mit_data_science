
from service.settings import WINE_MODEL_WORKDIR

from sklearn.externals import joblib

model_file = WINE_MODEL_WORKDIR + '/Data/Modeling/wine_model.jbl'

# Loading models at the service initialization
if 'globalTrainResults' not in dir():
    print('READING MODELS FROM ', model_file)
    globalTrainResults = joblib.load(model_file)
