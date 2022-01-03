import boto3,os
import read 

client = boto3.client('dynamodb')

def lambda_handler(events, context):
    client = boto3.client('dynamodb')
    method = events['httpMethod']
    
    if method == 'GET':
        data = read.ReadFromTable(os.getenv(key = 'table_name'))
        response = f"URLS = {data} "
    
    elif method == 'PUT':
        new_url = events['body']
        client.put_item(
        TableName = os.getenv(key='table_name'),
        Item={
        'Links':{'S' : new_url},
        })
        response = f"Url = {events['body']} is successfully added into the table"
        
    elif method == 'DELETE':
        new_url = events['body']
        print(new_url)
        client.delete_item(
        TableName = os.getenv(key='table_name'),
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