import boto3
import json


class Bucket:
    def __init__(self):
        self.client = boto3.client('s3')        #.get_object(Bucket='shanawar',Key='urls.json')
        
    def store_urls(self,bucket_name):
        try:
            self.client.create_bucket(Bucket=bucket_name,CreateBucketConfiguration={'LocationConstraint': 'us-east-2'})
            s3.upload_file("resources/urls.json", bucket_name ,"urlsList.json")
        except:
            print('Error in Uploading bucket')
        
    def get_bucket(self,bucket_name):
        response = self.client.get_object(Bucket=bucket_name, Key='urlsList.json',)
        data = self.client['Body']
        jObj = json.loads(data.read())
        listUrl = list(jObj.values())
        return(listUrl)
