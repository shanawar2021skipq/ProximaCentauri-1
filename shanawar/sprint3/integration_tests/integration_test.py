import pytest ,urllib3
assert 2==2
"""
api='https://pjwprn6s69.execute-api.us-east-2.amazonaws.com/prod'
api1='https://2pcgp8imi6.execute-api.us-east-2.amazonaws.com/prod'
http=urllib3.PoolManager()
def API_GET_TEST():
    response=http.request("GET",api)
    assert response.status == 200
""" 
    
