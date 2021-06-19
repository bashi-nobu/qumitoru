import os
import db_lib as dbLib
import s3_lib as s3Lib
import lambdafunction
import reader

imgReader = reader.ImgReader()
BUCKET_NAME = os.environ.get('BUCKET_NAME')
SCALE_PATARN_LIST = [10, 10, 5, 5, 5, 5, 5]

def handler(event, context):
    try:
        target_record_id = event['target_id']
        record_data = dbLib.get_questionare_data(target_record_id)
        file_path = record_data['file_path']
        user_id = record_data['user_id']
        # save questionnaire topic img to s3
        img_path_list, download_file_path = imgReader.saveQuestionnaireTopicImg(file_path, user_id)
        # predict score
        score_list = []
        for scale_patarn, img_path in zip(SCALE_PATARN_LIST, img_path_list):
            req_data = {"scale_patarn": scale_patarn, "img_path": img_path}
            score = lambdafunction.predictScore(req_data)
            score_list.append(score)
        print(score_list)
        s3Lib.delete_file(BUCKET_NAME, img_path_list)
        imgReader.uploadEncodeImg(BUCKET_NAME, download_file_path, file_path)
        dbLib.saveOcrResult(score_list, target_record_id)
    except Exception as e:
        print(e)
        s3Lib.delete_file(BUCKET_NAME, img_path_list)
