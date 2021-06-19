import boto3
import random
import string

def randomname():
    randlst = [random.choice(string.ascii_letters + string.digits) for i in range(8)]
    return ''.join(randlst)

def download_file(bucket_name, file_path):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    save_file_path = "/tmp/"+ randomname() + ".jpg"
    bucket.download_file(file_path, save_file_path)
    return save_file_path
