import os
import json
import reader
import boto3
import lambdafunction

imgReader = reader.ImgReader()

BUCKET_NAME = os.environ.get('BUCKET_NAME')
s3 = boto3.resource('s3')


def handler(event, context):
    file_path = lambdafunction.get_uploaded_file_path(event)
    save_file_path = imgReader.download_file(BUCKET_NAME, file_path)
    img = imgReader.read_img(save_file_path)
    img_size_type, height_rate = imgReader.check_pixel_size(img)

    if img_size_type == 'incompatible':
        reading_result = 'fail'
    else:
        isError, dst = imgReader.inclination_correction(img, img_size_type, height_rate)
        if isError:
            reading_result = 'fail'
        else:
            reading_result, point = imgReader.check_reading_questionnaire_topics(dst)
    if reading_result == 'fail':
        s3.Object(BUCKET_NAME, file_path).delete()
    os.remove(save_file_path)
    return {
        'statusCode': 200,
        'body': json.dumps({'reading_result': reading_result})
    }
