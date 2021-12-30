import boto3
import json

client = boto3.client('s3')
#client.create_bucket(Bucket='shanawarbucket',CreateBucketConfiguration={'LocationConstraint': 'us-east-2'})


class s3bucket:
    def __init__(self):
        self.client = boto3.client('s3')        #.get_object(Bucket='shanawar',Key='urls.json')
    def store_urls(self,bucket_name):
        try:
            s3.upload_file("/resources/urls.json", bucket_name,Key='urls.json' )
        except:
            print('Error in Uploading bucket')
        
    def get_bucket(self,bucket_name):
        response = self.client.get_object(Bucket=bucket_name,Key='urls.json')
       # response = self.client.list_objects(
        #              Bucket=bucket_name,
         #             MaxKeys=4,)

        data = response['Body']
        jObj = json.loads(data.read())
        listUrl = list(jObj.values())
        return(listUrl)
