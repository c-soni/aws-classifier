```bash
python -m venv <venv_name>
source vm-test/bin/activate
pip install -r requirements.txt

S3_BUCKET_NAME="<bucket-name>" SQS_READ_QUEUE_NAME="<queue-name>" flask run
```