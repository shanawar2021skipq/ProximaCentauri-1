import boto3,os
from bucket import s3bucket

def lambda_handler(event,context):
    s3obj=s3bucket()
    URLS = s3obj.get_bucket('shanawarbucket')
    print('URLS in s3_dynamo_lambda retreived',URLS)
    client = boto3.client('dynamodb')
        #################### S3 event ########################
    
    BucketName = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    print(str(event))
    print(key)
    print(BucketName)
    
        ###################### table name #######################
    
    urltable = os.getenv(key = 'url_table_name')#getting table name
    
    for url in URLS:
        client.put_item(TableName = urltable,Item=
        {
            'URLLinks':{'S': url}
        })
    return 'Successfully Added Urls in Dynamo'