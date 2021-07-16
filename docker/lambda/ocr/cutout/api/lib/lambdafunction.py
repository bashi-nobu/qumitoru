import os
import boto3
import json
import requests
import time

OCR_API_URL = os.environ.get('OCR_API_URL')
OCR_API_KEY = os.environ.get('OCR_API_KEY')

def requestToOcrLambda(req_data):
    if os.environ.get('AWS_LAMBDA_EXEC_ENV') is not None: # production env
        return requestToOcrLambdaProductionEnvVersion(req_data)
    else: # local env
        return requestToOcrLambdaLocalEnvVersion(req_data)

def requestToOcrLambdaProductionEnvVersion(req_data):
    isFinished = False
    headers = {"Content-Type" : "application/json", "x-api-key": OCR_API_KEY}
    response = requests.post(OCR_API_URL, headers=headers, data=json.dumps(req_data))
    res = json.loads(response.text)
    if 'score' in res:
        isFinished = True
    else:
        for i in range(0, 5):
            print('retry---')
            response = requests.post(OCR_API_URL, headers=headers, data=json.dumps(req_data))
            res = json.loads(response.text)
            if 'score' in res:
                isFinished = True
                break
    return isFinished, res

def requestToOcrLambdaLocalEnvVersion(req_data):
    lambda_ports = [9020, 9030]
    isFinished = False
    for port in lambda_ports:
        url = 'http://172.17.0.1:'+str(port)+'/2015-03-31/functions/function/invocations'
        response = requests.post(url, data=json.dumps(req_data), verify=False)
        try:
            response = json.loads(response.text)
        except Exception as e:
            print(e)
            continue
        if 'body' in response:
            response = json.loads(response['body'])
            isFinished = True
            break
    return isFinished, response

def predictScore(req_data):
    isFinished, res = requestToOcrLambda(req_data)
    score = res['score'] if isFinished else None
    return score
