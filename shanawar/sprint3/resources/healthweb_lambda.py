import urllib3,datetime
import constants as constants
from cloudwatch_putdata import CloudWatch_PutMetric
from resources.bucket import s3bucket 

def lambda_handler(events,context):
    values= dict()
    cw= CloudWatch_PutMetric()
    s3_bucket = s3bucket()
    #s3_bucket.store_urls('shanawarbucket')
    URLS = s3_bucket.get_bucket('shanawarbucket')
    count=1
    for url in URLS:
        avail= get_availability(url)
        dimensions=[
            {'Name':'URL','Value': constants.URL_to_Monitor},
        ]
        cw.put_data(constants.URL_Monitor_Namespace,constants.URL_Monitor_Name_Availability+'  '+url+ str(count),dimensions,avail)
        
        
        latency= get_latency(url)
        dimensions=[
            {'Name':'URL','Value': constants.URL_to_Monitor},
        ]
        cw.put_data(constants.URL_Monitor_Namespace,constants.URL_Monitor_Name_Latency+'  '+url+ str(count),dimensions,latency)
        
        values.update({"Availability": avail,"Latency":latency})
        count+=1
    return values
        

def get_availability(url):
    http=urllib3.PoolManager()
    response=http.request("GET",url)
    if response.status==200:
        return 1.0
    else:
        return 0.0
    
def get_latency(url):
    http=urllib3.PoolManager()
    start=datetime.datetime.now()
    response=http.request("GET",url)
    end=datetime.datetime.now()
    diff=end-start
    latency_sec=round(diff.microseconds * 0.000001,6)
    return latency_sec
