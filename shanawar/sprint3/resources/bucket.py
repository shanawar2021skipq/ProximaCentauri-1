import boto3
import json

client = boto3.client('s3')
res=client.list_buckets()
#print(res)
#client.create_bucket(Bucket='shanawarbucket',CreateBucketConfiguration={'LocationConstraint':'us-east-2'})


class Bucket():
    def __init__(self,bucket_name,key):
        self.client = boto3.client('s3').get_object(Bucket=bucket_name,Key=key)        #.get_object(Bucket='shanawar',Key='urls.json')
    def create(self,bucket_name):
        self.client.create_bucket(Bucket=bucket_name,CreateBucketConfiguration={'LocationConstraint':'us-east-2'})
    def store_urls(self,bucket_name):
        s3res = boto3.resource('s3')
        try:
            s3res.meta.client.upload_file("resources/urls.json", bucket_name,Key='urls.json' )
        except:
            print('Error in Uploading bucket')
        
    def get_bucket(self):
        response = self.client['Body']#.get_object(Bucket=bucket_name,Key=key)
        data = response
        obj = json.loads(data.read())
        listUrl = obj.values()
        print(listUrl)
        return(listUrl)
