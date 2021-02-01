# Log_uploader

Upload logs to aws S3


##How to use:
1) First create and IAM programmatic user within AWS with this policy
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
3) Rename `config.ini.example` to `config.ini` and fill in the necessary credentials
4) Run `install.sh` to install all the dependencies and check your python version (3.6.x is required)
5) When running the main.py file you can specify two flags
    -  --path : the path to where all your logs are stored (defaults to "./")
    - --extension : the file extension of your logs that this should look for (defaults to ".log")


Example Crontab Entry 
```
0 0 1 * * cd /home/ec2-user/AWS-Log-uploader/ && /opt/Python-3.8.7/python /home/ec2-user/AWS-Log-uploader/main.py --path /var/log/ --extension .log
```
