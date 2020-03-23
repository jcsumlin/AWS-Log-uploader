import ConfigParser
import argparse
import glob
import os

import boto
from boto.s3.key import Key

config = ConfigParser.ConfigParser()
path_current_directory = os.path.dirname(__file__)
config.readfp(open(os.path.join(path_current_directory, 'config.ini')))

ACCESS_KEY = config.get('aws', 'aws_access_key_id')
SECRET_KEY = config.get('aws', 'aws_secret_access_key')
BUCKET_NAME = config.get('aws', 'bucket_name')
if ACCESS_KEY is None or SECRET_KEY is None or BUCKET_NAME is None:
    print("One or more of the required config variables is missing. Please ensure config.ini is completely filled out!")


parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", type=str, help="The path to your log files")
parser.add_argument("-e", "--extension", type=str, help="The file extension of all your logs")
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



def upload_to_s3(aws_access_key_id, aws_secret_access_key, file, bucket, key, callback=None, md5=None,
                 reduced_redundancy=False, content_type=None):
    try:
        size = os.fstat(file.fileno()).st_size
    except:
        # Not all file objects implement fileno(),
        # so we fall back on this
        file.seek(0, os.SEEK_END)
        size = file.tell()

    conn = boto.connect_s3(aws_access_key_id, aws_secret_access_key)
    bucket = conn.get_bucket(bucket, validate=False)
    k = Key(bucket)
    k.key = key
    if content_type:
        k.set_metadata('Content-Type', content_type)
    sent = k.set_contents_from_file(file, cb=callback, md5=md5, reduced_redundancy=reduced_redundancy, rewind=True)

    # Rewind for later use
    file.seek(0)

    if sent == size:
        return True
    return False


filesToUpload = glob.glob(pathToLogs + "*" + extension)
fileNames = []
for files in filesToUpload:
    pathList = files.split("/")
    fileNames.append(pathList.pop())
index = 0
for file in filesToUpload:
    with open(file, 'r+') as file_data:
        uploaded = upload_to_s3(ACCESS_KEY, SECRET_KEY, file_data, BUCKET_NAME, fileNames[index])
    index += 1
    if uploaded is not False:
        os.remove(file)
        print("Removed " + file)
