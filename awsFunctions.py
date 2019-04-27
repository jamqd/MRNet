import boto3
import botocore
import os

def download(filePath):
    if os.path.isfile(filePath.split("/")[-1]):
        print(filePath.split("/")[-1] + " already exists")
        return
    BUCKET_NAME = 'mrnet'
    KEY = filePath
    print(KEY)
    s3 = boto3.resource('s3')

    try:
        s3.Bucket(BUCKET_NAME).download_file(KEY, filePath.split("/")[-1])
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise

def upload(filePath, bucket_directory=""):
    bucket_name = 'mrnet'
    s3 = boto3.client('s3')
    s3.upload_file(filePath, bucket_name, bucket_directory + filePath)

def uploadDir(dir):

    s3 = boto3.client('s3')

    for root,dirs,files in os.walk(dir):
        for file in files:
            print("upload " + str(os.path.join(root,file)[2:]))
            s3.upload_file(os.path.join(root,file),'mrnet', os.path.join(root,file)[2:])

def downloadDir(remoteDirectoryName):
    s3_resource = boto3.resource('s3')
    bucket = s3_resource.Bucket('mrnet')
    for key in bucket.objects.filter(Prefix = remoteDirectoryName):
        if not os.path.exists(os.path.dirname(key.key)):
            os.makedirs(os.path.dirname(key.key))
        bucket.download_file(key.key,key.key)
