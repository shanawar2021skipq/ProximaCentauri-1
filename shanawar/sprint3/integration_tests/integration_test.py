import pytest ,urllib3,requests,datetime

#invokeurl=f"https://{a.restApiId}.execute-api.us-east-2.amazonaws.com/prod/"

api='https://xx7b4z0m61.execute-api.us-east-2.amazonaws.com/prod'


def test_put():
    http=urllib3.PoolManager()
    response=http.request("GET",invokeurl)
    assert response.status == 200
    

def test_latency():
    http=urllib3.PoolManager()
    start=datetime.datetime.now()
    response=http.request("GET",api)
    end=datetime.datetime.now()
    diff=end-start
    latency_sec=round(diff.microseconds * 0.000001,6)
    assert latency_sec<1
