import boto3

bucketName = "elasticbeanstalk-us-east-1-559984272434"
Key = "producer.py"
outPutname = "test/producer.py"

s3 = boto3.client('s3')
s3.upload_file(Key,bucketName,outPutname)