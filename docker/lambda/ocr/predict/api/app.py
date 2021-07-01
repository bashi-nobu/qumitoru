import ocr
import boto3
import lambdafunction
import json

ocr = ocr.ocrQuestionare()
s3 = boto3.resource('s3')

def handler(event, context):
    scale_patarn, img_path = lambdafunction.get_params(event)
    ocr_result = ocr.questionareOcr(scale_patarn, img_path, s3)
    return {
        'statusCode': 200,
        'body': json.dumps({'score': str(ocr_result)})
    }
