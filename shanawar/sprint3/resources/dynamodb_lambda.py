import boto3,os
def lambda_handler(event, context):
    db=boto3.client('dynamodb')
    MessageID = event['Records'][0]['Sns']['Message']
    Timestamp = event['Records'][0]['Sns']['Timestamp']
    
    table_name=os.getenv('table_name')

    db.put_item(TableName=table_name,Item=
    {
        'MessageID':{'S':MessageID},
        'TimeStamp':{'S':Timestamp}
        
    })
    
    #print("Dynamo DB Lambda"+MessageID)
    

