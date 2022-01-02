import boto3,json

class dynamofn():
    def __init__(self):
        self.session=boto3.session.Session()
        self.current_region=self.session.region_name
        self.resource = boto3.resource('dynamodb',region_name=self.current_region)
        self.client = boto3.client('dynamodb')
        
    def add(self,table_name,message):
        table=self.resource.Table(table_name)
        response=table.put_item(Item=message)
        return response
    
    def get_data(self,table_name,key):
        response=self.client.get_item(
            TableName=table_name,
            Key= {"url":{"S":key}}
            )
    
    def deletion(self,table_name,key):
        response=self.client.delete_item(
            TableName=table_name,
            Key={"URL": {"S":key}}
            )
            
    def scan(self,table_name):
        response=self.client.scan(
            TableName=table_name)
        return response
    