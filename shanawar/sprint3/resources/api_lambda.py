import boto3,os
from dynamofunc import dynamofn
def lambda_handler(events,context):
    dynamofunctions=dynamofn()
    method=events['httpMethod']
    body=events['body']
    
    table=os.getenv('url_table_name')
    
    if (method=='GET'):
        response=dynamofunctions.scan(table)
        URLS=[]
        for url in response['Items']:
            URLS.append(url['url']['S'])
        return URLS
        
    elif (method=='PUT'):
        return dynamofunctions.add(table,{'url':body})
        
    elif (method=='DELETE'):
        return dynamofunctions.deletion(table,body)
    else:
        return ("Method UNDEFINED")
            