import os
import boto3
import json
import requests
import time

OCR_FUNCTION_NAME = os.environ.get('OCR_FUNCTION_NAME')

def lambda_invoke(request_data):
    client = boto3.client('lambda')
    response = client.invoke(
            FunctionName = OCR_FUNCTION_NAME,
            InvocationType = 'RequestResponse',
            LogType = 'Tail',
            Payload = json.dumps(request_data)
    )
    response = json.loads(response['Payload'].read())
    return response

def requestToOcrLambda(req_data):
    if os.environ.get('AWS_LAMBDA_RUNTIME_API') is None: # production env
        return requestToOcrLambdaProductionEnvVersion(req_data)
    else: # local env
        return requestToOcrLambdaLocalEnvVersion(req_data)

def requestToOcrLambdaProductionEnvVersion(req_data):
    res = lambda_invoke(req_data)
    if len(res) == 0:
        isFinished = False
        for i in range(0, 5):
            print('retry---')
            res = lambda_invoke(req_data)
            time.sleep(1)
            if len(res) > 0:
                isFinished = True
                break
    else:
        isFinished = True
    return isFinished, res

def requestToOcrLambdaLocalEnvVersion(req_data):
    url = 'http://172.17.0.1:9020/2015-03-31/functions/function/invocations'
    r = requests.post(url, data=json.dumps(req_data), verify=False)
    if len(r.text) == 0 or r.status_code != requests.codes.ok:
        isFinished = False
        for i in range(0, 5):
            print('retry---')
            r = requests.post(url, data=json.dumps(req_data), verify=False)
            time.sleep(1)
            if len(r.text) == 0 or r.status_code != requests.codes.ok:
                isFinished = True
                break
    else:
        isFinished = True
    return isFinished, json.loads(r.text)

def predictScore(req_data):
    isFinished, res = requestToOcrLambda(req_data)
    print(res)
    score = res['score'] if isFinished else None
    return score
