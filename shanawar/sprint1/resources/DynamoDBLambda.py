import boto3,os
def lambda_handler(event, context):
    # BOTO3 CLIENT
    db=boto3.client('dynamodb')
    # SEPARATE MESSAGE ID and TIMESTAMP
    Message = event['Records'][0]['Sns']['MessageId']
    Timestamp = event['Records'][0]['Sns']['Timestamp']
    table_name=os.getenv('table_name')
    # UPDATE TABLE WITH ITEMS
    db.put_item(TableName=table_name,Item={
        'MessageID':{'S':Message},
        'TimeStamp':{'S':Timestamp}
    })