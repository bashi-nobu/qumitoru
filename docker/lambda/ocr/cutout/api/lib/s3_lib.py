import boto3
import random
import string

s3 = boto3.resource('s3')

def randomname():
    randlst = [random.choice(string.ascii_letters + string.digits) for i in range(8)]
    return ''.join(randlst)

def download_file(bucket_name, file_path):
    bucket = s3.Bucket(bucket_name)
    save_file_path = "/tmp/"+ randomname() + ".jpg"
    bucket.download_file(file_path, save_file_path)
    return save_file_path

def upload_file(bucket_name, user_id, file_path):
    bucket = s3.Bucket(bucket_name)
    save_path_in_s3 = str(user_id)+ '/export' + file_path
    bucket.upload_file(file_path, save_path_in_s3)
    return save_path_in_s3

def delete_file(bucket_name, file_path_list):
    for file_path in file_path_list:
        s3.Object(bucket_name, file_path).delete()
