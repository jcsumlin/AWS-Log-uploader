import configparser
import getopt
import glob
import os
import sys

import boto3
from botocore.exceptions import NoCredentialsError

config = configparser.ConfigParser()
path_current_directory = os.path.dirname(__file__)
config.read(os.path.join(path_current_directory, 'config.ini'))


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
    print('\tmain.py -p <pathToLogsFolder> -e <extensions of your logs>')
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print('== Logs to s3 uploader ==')
        print('\tVersion: 1.0')
        print('\tMaintainer: Chat Sumlin (chat.sumlin@banyanhills.com)')
        print('== Usage Instructions ==')
        print('\tmain.py -p <pathToLogsFolder> -e <extensions of your logs>')
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
for file in filesToUpload:
    uploaded = upload_to_aws(file, BUCKET_NAME, fileNames[index])
    index += 1
    if uploaded is not False:
        os.remove(file)
        print(f"Removed {file}")


