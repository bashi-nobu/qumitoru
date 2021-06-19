import os
import json

def get_uploaded_file_path(event):
    if os.environ.get('AWS_LAMBDA_RUNTIME_API') is None: # production env
        file_path = json.loads(event['body'])['file_path']
    else: # local env
        file_path = str(event['file_path'])
    return file_path

