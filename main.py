import glob

import boto3
from botocore.exceptions import NoCredentialsError
import configparser
from datetime import datetime
from os import listdir
from os.path import isfile, join
import sys, getopt

config = configparser.ConfigParser()
config.read('config.ini')

ACCESS_KEY = config['aws']['aws_access_key_id']
SECRET_KEY = config['aws']['aws_secret_access_key']
BUCKET_NAME = config['aws']['bucket_name']
if ACCESS_KEY is None or SECRET_KEY is None or BUCKET_NAME is None:
    print("One or more of the required config variables is missing. Please ensure config.ini is completely filled out!")

argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(argv, "hp:e:", ["path=", "extension="])
except getopt.GetoptError:
    print('== Logs to s3 uploader ==')
    print('\tVersion: 1.0')
    print('\tMaintainer: Chat Sumlin (chat.sumlin@banyanhills.com)')
    print('== Usage Instructions ==')
    print('\tmain.py -p <pathToLogsFolder>')
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print('main.py -p <pathToLogsFolder> -')
        sys.exit()
    elif opt in ("-p", "--path"):
        pathToLogs = arg
        print(f"Path set to: {pathToLogs}")
    elif opt in ("-e", "--extension"):
        extension = arg
        print(f"Extension set to: {extension}")
if 'extension' not in locals():
    extension = ".log"
    print(f"Extension defaulted to: {extension}")
if 'pathToLogs' not in locals():
    pathToLogs = "./"
    print(f"Extension defaulted to: {pathToLogs}")


def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)

    try:
        s3.upload_file(local_file, bucket, s3_file)
        print(f"{local_file} uploaded to {bucket} SUCCESSFULLY")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False


filesToUpload = glob.glob(f"{pathToLogs}*{extension}", recursive=True)
fileNames = []
for files in filesToUpload:
    pathList = files.split("/")
    fileNames.append(pathList.pop())
index = 0
for files in filesToUpload:
    uploaded = upload_to_aws(files, BUCKET_NAME, fileNames[index])
    index += 1
