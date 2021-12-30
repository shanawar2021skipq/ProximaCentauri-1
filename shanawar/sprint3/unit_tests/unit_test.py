import pytest 
from aws_cdk import core
from sprint2.sprint2_stack import Sprint2Stack

#### Unit Test that checks permissions ##########    
def test_permission():
    app=core.App()
    Sprint2Stack(app,'TestStack')
    template=app.synth().get_stack_by_name('TestStack').template
    permission=[resource for resource in template['Resources'].values() if resource['Type']=='AWS::Lambda::Permission']

    assert len(permission)==2    

#######################################################
#### Unit Test that checks Lambda Functions ##########    

def test_lambda():

    app=core.App()
    Sprint2Stack(app,'TestStack')
    template=app.synth().get_stack_by_name('TestStack').template
    codebuild=[resource for resource in template['Resources'].values() if resource['Type']=='AWS::Lambda::Function']

    assert len(codebuild)==2    
####################################################