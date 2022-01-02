import boto3,os
from bucket import s3bucket as s

def lambda_handler(event,context):
   # s3obj=s3bucket()
#    URLS = s3obj.get_bucket('shanawarbucket')
 #   print('URLS in s3_dynamo_lambda retreived',URLS)
    client = boto3.client('dynamodb')
        #################### S3 event ########################

    BucketName = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    print(str(event))
    print(key)
    print(BucketName)

        ###################### table name #######################
    URLS= s(BucketName,key).get_bucket()
    print('URLS in s3_dynamo_lambda retreived',URLS)
    urltable = os.getenv(key = 'url_table_name')#getting table name
    print('THE URL TABLE NAME:',urltable)
    for link in URLS:
        client.put_item(TableName = urltable,Item=
        {
            'Links':{'S': link}
        })
