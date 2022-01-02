import boto3,os
import read as dynamo_RW

client = boto3.client('dynamodb')

def lambda_handler(events, context):
    client = boto3.client('dynamodb')
    
    if events['httpMethod'] == 'GET':
        
        data = dynamo_RW.ReadFromTable(os.getenv(key = 'table_name'))
        response_msg = f"data from table is = {data} "
    
    elif events['httpMethod'] == 'PUT':
        
        
        new_url = events['body']
        client.put_item(
        TableName = os.getenv(key='table_name'),
        Item={
        'Links':{'S' : new_url},
        })
        response_msg = f"Url = {events['body']} is successfully added into the table"
        
    elif events['httpMethod'] == 'DELETE':
    
        new_url = events['body']
        print(new_url)
        client.delete_item(
        TableName = os.getenv(key='table_name'),
        Key={
        'Links':{'S' : new_url}
        })
        response_msg = f"Url= {events['body']} is successfully deleted from the table"
    else:
        
        response_msg = 'You can only put a item in table, delete it or get items from table'
    print(response_msg)  
    return {
        
        'statusCode' : 200,
        'body'  :  response_msg
        
    }