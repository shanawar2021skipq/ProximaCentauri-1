import pytest ,urllib3,requests,datetime,json,os

#invokeurl=f"https://{a.restApiId}.execute-api.us-east-2.amazonaws.com/prod/"
# Finding the unique ID of API Gateway. The API ID changes everytime the pipeline is deployed.
apis = json.load(os.popen('aws apigateway get-rest-apis'))  # popen runs the cli commands
apis = apis["items"]
for dic in apis:
    if dic["name"] == "SHANAWAR_ALI_API":
        api_ID = dic["id"]
        break

api=(f"https://{api_ID}.execute-api.us-east-2.amazonaws.com/prod/")
print(api)
#api='https://xx7b4z0m61.execute-api.us-east-2.amazonaws.com/prod'


def test_get():
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
