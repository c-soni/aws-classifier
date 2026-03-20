import os
os.environ["KERAS_BACKEND"] = "numpy"

import keras
from keras.applications.efficientnet import EfficientNetB7
import keras
from keras.applications.efficientnet import preprocess_input, decode_predictions
import numpy as np

def get_model():
    return EfficientNetB7(
        include_top=True,
        weights="imagenet",
        input_tensor=None,
        input_shape=None,
        pooling=None,
        classes=1000,
        classifier_activation="softmax",
        name="efficientnetb7",
    )

def predict(model, filepath):
    img = keras.utils.load_img(filepath, target_size=(600, 600))
    x = keras.utils.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    preds = model.predict(x)
    print('Predicted:', decode_predictions(preds, top=3)[0])