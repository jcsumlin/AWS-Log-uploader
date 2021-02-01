import configparser
import argparse
import fnmatch
import os
from botocore.exceptions import ClientError


import boto3

from ProgressPercentage import ProgressPercentage

config = configparser.ConfigParser()
path_current_directory = os.path.dirname(__file__)
config.read("./config.ini")

ACCESS_KEY = config.get('aws', 'aws_access_key_id')
SECRET_KEY = config.get('aws', 'aws_secret_access_key')
BUCKET_NAME = config.get('aws', 'bucket_name')
REGION_ENDPOINT = config.get('aws', 'aws_s3_host')
if ACCESS_KEY is None or SECRET_KEY is None or BUCKET_NAME is None:
    print("One or more of the required config variables is missing. Please ensure config.ini is completely filled out!")
    exit(0)

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", type=str, help="The path to your log files. DEFAULT: current working directory")
parser.add_argument("-e", "--extension", type=str, help="The file extension of all your logs. DEFAULT: .log")
parser.add_argument("-b", "--bucket", type=str, help="The S3 Bucket that you want to upload to Can aloe be set in the config.ini file")
parser.add_argument("-k", "--keep", action="store_true", help="Don't delete files after upload")
args = parser.parse_args()

if not args.path:
    pathToLogs = "./"
    print("Extension defaulted to:" + pathToLogs)
else:
    pathToLogs = args.path
    print("Path set to: " + pathToLogs)

if not args.extension:
    extension = ".log"
    print("Extension defaulted to: " + extension)
else:
    extension = args.extension
    print("Extension set to: " + extension)
if not args.bucket:
    BUCKET_NAME = config.get('aws', 'bucket_name')
else:
    BUCKET_NAME = args.bucket
print("Bucket set to: " + BUCKET_NAME)


def upload_file(file_name, bucket, object_name=None):
    if object_name is None:
        object_name = file_name

    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name, Callback=ProgressPercentage(file_name))
    except ClientError as e:
        print(e)
        return False
    return True

matches = []
for root, dirnames, filenames in os.walk(pathToLogs):
    for filename in fnmatch.filter(filenames, '*' + extension):
        matches.append(os.path.join(root, filename))
fileNames = []
for files in matches:
    pathList = files.split("/")
    fileNames.append(pathList[-1])
index = 0
for file in matches:
    print(f"Uploading {file} to {BUCKET_NAME}")
    uploaded = upload_file(file, BUCKET_NAME, fileNames[index])
    print("File " + fileNames[index] + " was uploaded")
    index += 1
    if uploaded is not False and not args.keep:
        os.remove(file)
        print("Removed " + file)
