import boto3,os
import read 
from bucket import Bucket as s
client = boto3.client('dynamodb')

URLS= s('shanawarbucket','urls.json').get_bucket()
print('URLS in API LAMBDA ',URLS)

urltable = os.getenv(key = 'table_name')#getting table name
print('THE URL TABLE NAME in API LAMBDA:',urltable)

for link in URLS:
    client.put_item(TableName = urltable,Item={'Links':{'S': link}})


def lambda_handler(events, context):
    client = boto3.client('dynamodb')
    
    method = events['httpMethod']
    if method == 'GET':
        data = read.ReadFromTable(urltable)
        response = f"URLS = {data} "
    
    elif method == 'PUT':
        newurl = events['body']
        client.put_item(
        TableName = urltable,
        Item={
        'Links':{'S' : newurl},
        })
        response = f"Url = {events['body']} is successfully added into the table"
        
    elif method == 'DELETE':
        url = events['body']
        print(url)
        client.delete_item(
        TableName =urltable,
        Key={
        'Links':{'S' : url}
        })
        response = f"Url= {events['body']} is successfully deleted from the table"
        
    elif method == 'POST':
        url = events['body']
        url_ex_new=url.split(",")
        ex=url_ex_new[0]
        new=url_ex_new[1]
        URLS_LIST=read.ReadFromTable(urltable)  #read table
        if ex in URLS_LIST:                 #if item is avaialble then 
            client.delete_item(TableName= urltable,Key={'Links':{'S' : ex}})
            client.put_item(TableName= urltable,Item={'Links':{'S' : new}})
            response="Successfully updated in DynamoDB table."
        else:                            
            response="Failed to update"

        
    else:
        response = 'Indefinite Method Request Error.'
        
    print(response) 
    
    return {
        'statusCode' : 200,
        'body'  :  response
    }