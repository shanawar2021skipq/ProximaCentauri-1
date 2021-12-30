import urllib3,datetime
import constants as constants
from cloudwatch_putdata import CloudWatch_PutMetric

def lambda_handler(events,context):
    values= dict()
    cw= CloudWatch_PutMetric()
    
    avail= get_availability()
    dimensions=[
        {'Name':'URL','Value': constants.URL_to_Monitor},
    ]
    cw.put_data(constants.URL_Monitor_Namespace,constants.URL_Monitor_Name_Availability,dimensions,avail)
    
    
    latency= get_latency()
    dimensions=[
        {'Name':'URL','Value': constants.URL_to_Monitor},
    ]
    cw.put_data(constants.URL_Monitor_Namespace,constants.URL_Monitor_Name_Latency,dimensions,latency)
    
    values.update({"Availability": avail,"Latency":latency})
    return values

def get_availability():
    http=urllib3.PoolManager()
    response=http.request("GET",constants.URL_to_Monitor)
    if response.status==200:
        return 1.0
    else:
        return 0.0
    
def get_latency():
    http=urllib3.PoolManager()
    start=datetime.datetime.now()
    response=http.request("GET",constants.URL_to_Monitor)
    end=datetime.datetime.now()
    diff=end-start
    latency_sec=round(diff.microseconds * 0.000001,6)
    return latency_sec
