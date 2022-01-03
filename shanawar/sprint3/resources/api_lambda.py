import boto3,os
import read 
from bucket import Bucket as s
client = boto3.client('dynamodb')


def lambda_handler(events, context):
    client = boto3.client('dynamodb')
    
    
    URLS= s('shanawarbucket','urls.json').get_bucket()
    print('URLS in API LAMBDA ',URLS)
    
    urltable = os.getenv(key = 'table_name')#getting table name
    print('THE URL TABLE NAME in API LAMBDA:',urltable)
    
    for link in URLS:
        client.put_item(TableName = urltable,Item=
        {
            'Links':{'S': link}
        })
    
    
    
    method = events['httpMethod']
    
    if method == 'GET':
        data = read.ReadFromTable(urltable)
        response = f"URLS = {data} "
    
    elif method == 'PUT':
        new_url = events['body']
        client.put_item(
        TableName = urltable,
        Item={
        'Links':{'S' : new_url},
        })
        response = f"Url = {events['body']} is successfully added into the table"
        
    elif method == 'DELETE':
        new_url = events['body']
        print(new_url)
        client.delete_item(
        TableName =urltable,
        Key={
        'Links':{'S' : new_url}
        })
        response = f"Url= {events['body']} is successfully deleted from the table"
        
    else:
        
        response = 'Indefinite Method Request Error.'
    print(response) 
    
    return {
        'statusCode' : 200,
        'body'  :  response
    }