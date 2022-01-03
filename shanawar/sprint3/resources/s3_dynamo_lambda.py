import boto3,os
from bucket import Bucket as s

def lambda_handler(event,context):
   # s3obj=s3bucket()
#    URLS = s3obj.get_bucket('shanawarbucket')
 #   print('URLS in s3_dynamo_lambda retreived',URLS)
    client = boto3.client('dynamodb')
        #################### S3 event ########################
    print("HI I'm in S3. Can you see me in cloudwatch?")
    BucketName = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    print(str(event))
    print(key)
    print(BucketName)

    BucketName='shanawarbucket'
    key = 'urls.json'

        ###################### table name #######################
    URLS= s(BucketName,key).get_bucket()
    print('URLS in s3_dynamo_lambda retreived',URLS)
    urltable = os.getenv(key = 'table_name')#getting table name
    print('THE URL TABLE NAME:',urltable)
    u=['www.skipq.org','www.netflix.com','www.slack.com','www.facebook.com']
    for link in u:
        client.put_item(TableName = urltable,Item=
        {
            'Links':{'S': link}
        })
