import threading
from flask import Flask, Response
import boto3
import os
os.environ["KERAS_BACKEND"] = "numpy"

import keras
from keras.applications.efficientnet import EfficientNetB7
from keras.applications.efficientnet import preprocess_input, decode_predictions
import numpy as np

S3_BUCKET_NAME = 'test-bucket-redacted'
S3_OBJECT_KEY_ATTR = 's3-key'
SQS_READ_QUEUE_NAME = 'test-queue'
FILE_PATH = 'file.jpg'

def predict(model, filepath):
    img = keras.utils.load_img(filepath, target_size=(600, 600))
    x = keras.utils.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    preds = model.predict(x)
    print('Predicted:', decode_predictions(preds, top=3)[0])

def process(s3, queue, model, filepath):
    while True:
        print('Polling...')
        for message in queue.receive_messages(MessageAttributeNames=[]):
            obj_key = S3_OBJECT_KEY_ATTR
            if message.message_attributes is not None:
                obj_key = message.message_attributes.get(S3_OBJECT_KEY_ATTR).get('StringValue')
                if obj_key:
                    with open(filepath, 'wb') as f:
                        s3.download_fileobj(S3_BUCKET_NAME, obj_key, f)
                    predict(model, filepath)
                    message.delete()

def setup():
    model = EfficientNetB7(
        include_top=True,
        weights="imagenet",
        input_tensor=None,
        input_shape=None,
        pooling=None,
        classes=1000,
        classifier_activation="softmax",
        name="efficientnetb7",
    )

    filepath = FILE_PATH
    s3 = boto3.client('s3')

    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName=SQS_READ_QUEUE_NAME)
    thread = threading.Thread(target=process, args=(s3, queue, model, filepath))
    thread.start()

app = Flask(__name__)

@app.get('/health')
def health():
    return Response()

setup()
