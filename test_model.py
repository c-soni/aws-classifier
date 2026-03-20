import threading
from utils.model import get_model, predict

FILE_PATH = 'file.jpg'

def setup():
    model = get_model()

    filepath = FILE_PATH
    thread = threading.Thread(target=predict, args=(model, filepath))
    thread.start()
    thread.join()

setup()
