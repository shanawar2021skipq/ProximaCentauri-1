import pytest 
from aws_cdk import core
from sprint3.sprint3_stack import Sprint3Stack

app=core.App()
Sprint3Stack(app,'TestStack')
template=app.synth().get_stack_by_name('TestStack').template

#### Unit Test that checks number of tables ##########    
def test_table():
    tables=[resource for resource in template['Resources'].values() if resource['Type']=='AWS::DynamoDB::Table']
    assert len(tables)==2    

#######################################################
#### Unit Test that checks Lambda Functions ##########    

def test_lambda():

    template=app.synth().get_stack_by_name('TestStack').template
    lambdas=[resource for resource in template['Resources'].values() if resource['Type']=='AWS::Lambda::Function']

    assert len(lambdas)==3    
####################################################

def test_api():
    
    template=app.synth().get_stack_by_name('TestStack').template
    api=[resource for resource in template['Resources'].values() if resource['Type']=='AWS::ApiGateway::RestApi']
    assert len(api)==1
