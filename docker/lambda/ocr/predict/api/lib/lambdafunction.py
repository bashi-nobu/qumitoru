import os
import json

def get_params(event):
    if os.environ.get('AWS_LAMBDA_EXEC_ENV') is not None: # production env
        scale_patarn = json.loads(event['body'])['scale_patarn']
        img_path = json.loads(event['body'])['img_path']
    else: # local env
        scale_patarn = event['scale_patarn']
        img_path = event['img_path']
    return scale_patarn, img_path

