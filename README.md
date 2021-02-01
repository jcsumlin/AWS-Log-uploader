# Log_uploader

Upload logs to aws S3


##How to use:
1) First create and IAM programmatic user within AWS with this policy.
    1) You can tweak this if you are experienced in IAM and want more control over access.
### IAM Policy
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListAllMyBuckets",
                "s3:PutObject",
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::*"
            ]
        }
    ]
}
```
2) Copy down the Access key ID and Secret
3) Insure the AWS cli is installed
4) Configure AWS CLI by using `aws configure` in the terminal. It will ask you for your Access Key and Secret from step 1
5) You can use the included config.ini file or cli flags to pass the remainder of the configuration options. 
3) Rename `config.ini.example` to `config.ini` and fill in the name of your bucket
4) Run `install.sh` to install all the dependencies and check your python version (3.8.x is required) (**NOTE:** This assumes that your python PATH is set)
    5) If the installer fails to fetch the dependencies you can alternatively run `/path/to/python -m pip install -r requirements.txt`

### CLI Arguements 
```
usage: main.py [-h] [-p PATH] [-e EXTENSION] [-b BUCKET] [-k]

optional arguments:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  The path to your log files. DEFAULT: current working
                        directory
  -e EXTENSION, --extension EXTENSION
                        The file extension of all your logs. DEFAULT: .log
  -b BUCKET, --bucket BUCKET
                        The S3 Bucket that you want to upload to Can aloe be
                        set in the config.ini file
  -k, --keep            Don't delete files after upload
```

#### Example Crontab Entry 
```
0 0 1 * * cd /home/ec2-user/AWS-Log-uploader/ && /opt/Python-3.8.7/python /home/ec2-user/AWS-Log-uploader/main.py --path /var/log/ --extension .log
```
