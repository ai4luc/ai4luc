"""
Software Open Source
©Copyright Mateus de Souza Miranda, 2023
mateus.miranda@inpe.br; mateusmirandaa2@hotmail.com
National Institute for Space Research (INPE)
São José dos Campos, São Paulo, Brazil

Version 4:  January, 2023
"""

# -------- Library --------
# Directory manage
import numpy as np

# Machine & Deep Learning
from keras.models import load_model

# Py imports
import tools


# -------- Cerranetv3 --------
def cerranet_module(data, trained_model_path):
    # Model rgba_data
    path_model = trained_model_path
    # Starting the model
    cerranetv3 = load_model(path_model)
    # Data Visualization
    # print('Data shape: ', np.shape(data))

    # Prediction
    pred = cerranetv3.predict(data)
    # Take the maxximun probability of the prediction
    pred_argmax = np.argmax(pred, axis=1)

    # Return the id of the class (range 0 to up 7)
    return pred_argmax
