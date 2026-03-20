import threading
from flask import Flask, Response

from utils.model import get_model, predict
from utils.aws_util import get_aws_resources, S3_BUCKET_NAME, S3_OBJECT_KEY_ATTR

FILE_PATH = 'file.jpg'
running = True

def process(s3, queue, model, filepath):
    global running
    while running:
        print('Polling...')
        for message in queue.receive_messages(MessageAttributeNames=[S3_OBJECT_KEY_ATTR]):
            obj_key = S3_OBJECT_KEY_ATTR
            if message.message_attributes is not None:
                obj_key = message.message_attributes.get(S3_OBJECT_KEY_ATTR).get('StringValue')
                if obj_key:
                    with open(filepath, 'wb') as f:
                        s3.download_fileobj(S3_BUCKET_NAME, obj_key, f)
                    predict(model, filepath)
        message.delete()

def setup():
    model = get_model()

    filepath = FILE_PATH
    s3, queue = get_aws_resources()
    thread = threading.Thread(target=process, args=(s3, queue, model, filepath))
    thread.start()
    return thread

app = Flask(__name__)

@app.get('/health')
def health():
    return Response()

thread = setup()
