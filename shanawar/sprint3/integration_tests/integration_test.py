import pytest ,urllib3,requests,datetime

api='https://am12vc9adf.execute-api.us-east-2.amazonaws.com/prod'
api1='https://z6mdf65yd7.execute-api.us-east-2.amazonaws.com/prod'


def test():
    http=urllib3.PoolManager()
    response=http.request("GET",api)
    assert response.status == 200
    

def test_latency():
    http=urllib3.PoolManager()
    start=datetime.datetime.now()
    response=http.request("GET",api)
    end=datetime.datetime.now()
    diff=end-start
    latency_sec=round(diff.microseconds * 0.000001,6)
    assert latency_sec<1

