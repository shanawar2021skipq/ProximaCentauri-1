import urllib3,datetime
import constants as constants
from cloudwatch_putdata import CloudWatch_PutMetric
from bucket import Bucket as s

def lambda_handler(events,context):
    values= dict()
    cw= CloudWatch_PutMetric()
    URLS = s('shanawarbucket','urls.json').get_bucket()
    print( 'URLS IN WEBHEALTH LAMBDA', URLS)
    for url in URLS:
        print(url)
        avail= get_availability(url)
        dimensions=[
            {'Name':'URL','Value': url},
        ]
        cw.put_data(constants.URL_Monitor_Namespace,constants.URL_Monitor_Name_Availability+url,dimensions,avail)
        
        
        latency= get_latency(url)
        dimensions=[
            {'Name':'URL','Value': url},
        ]
        cw.put_data(constants.URL_Monitor_Namespace,constants.URL_Monitor_Name_Latency+url ,dimensions,latency)
        
        values.update({"Availability": avail,"Latency":latency})
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
