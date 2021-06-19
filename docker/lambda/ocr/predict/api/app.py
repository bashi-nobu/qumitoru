import ocr
import boto3

ocr = ocr.ocrQuestionare()
s3 = boto3.resource('s3')

def handler(event, context):
    scale_patarn = event['scale_patarn']
    img_path = event['img_path']
    ocr_result = ocr.questionareOcr(scale_patarn, img_path, s3)
    response = {'score': str(ocr_result)}
    return response
