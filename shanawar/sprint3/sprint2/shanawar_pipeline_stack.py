from aws_cdk import (
    core,
    aws_codepipeline_actions as cpactions,
    aws_iam ,
    pipelines
    )
from sprint2.sprint2_stage import Sprint2Stage

class PipelineStack(core.Stack):
    def __init__(self,scope:core.Construct,id:str,**kwargs):
        super().__init__(scope,id,**kwargs)
        pipelineroles=self.createrole()
        iamPolicy=aws_iam.PolicyStatement(resources=['*'],actions=['iam:*'])
        stsPolicy=aws_iam.PolicyStatement(resources=['*'],actions=['sts:*'])

        ############# STEP1: SOURCE is Github ##############
        source =pipelines.CodePipelineSource.git_hub(repo_string='shanawar2021skipq/ProximaCentauri-1',branch='main',
        authentication=core.SecretValue.secrets_manager('pipeline/shanawar',
        json_field="shanawarsecret"),
        trigger=cpactions.GitHubTrigger.POLL)
        
        ############# STEP2: BUILD ###############
        synth = pipelines.CodeBuildStep('Shanawar_synthesizing',input=source,
        commands=["cd shanawar/sprint3","pip install -r requirements.txt", "npm install -g aws-cdk", "cdk synth"],
        primary_output_directory="shanawar/sprint3/cdk.out",
        role=pipelineroles,
        role_policy_statements=[iamPolicy,stsPolicy]
        )
        
        pipeline=pipelines.CodePipeline(self,"ShanawarPipeline",pipeline_name="ShanawarAliPipeline",synth=synth)

        ############# STEP3: TEST ###############      
        beta= Sprint2Stage(self,"ShanawarBeta3",
        env={"account":"315997497220","region":"us-east-2"})
        
        prod= Sprint2Stage(self,"ShanawarProd3",
        env={"account":"315997497220","region":"us-east-2"})
        
        """
        gamma= Sprint2Stage(self,"ShanawarGamma3",
        env={"account":"315997497220","region":"us-east-2"})
        

        unit_test = pipelines.CodeBuildStep(
            'unit_tests',input=source,
            commands=["cd shanawar/sprint3","pip install -r requirements.txt", "npm install -g aws-cdk", "pytest unit_tests"],
            role=pipelineroles,
            role_policy_statements=[iamPolicy,stsPolicy]
            )
            
        integration_test = pipelines.CodeBuildStep(
            'integration_tests',input=source,
            commands=["cd shanawar/sprint3","pip install -r requirements.txt", "npm install -g aws-cdk", "pytest integration_tests"],
            role=pipelineroles,
            role_policy_statements=[iamPolicy,stsPolicy]
            )
        """
        pipeline.add_stage(beta)#, pre=[unit_test],post=[pipelines.ManualApprovalStep("Post-Beta Check")])
  #      pipeline.add_stage(gamma, pre=[integration_test],post=[pipelines.ManualApprovalStep("Post-Gamma Check")]) 
    ################# STEP4: PROD ###################    
        pipeline.add_stage(prod)
        
###########################################################################
    def createrole(self):
        role=aws_iam.Role(self,"pipeline-role",
        assumed_by=aws_iam.CompositePrincipal(
            aws_iam.ServicePrincipal("lambda.amazonaws.com"),
            aws_iam.ServicePrincipal("sns.amazonaws.com"),
            aws_iam.ServicePrincipal("codebuild.amazonaws.com")
            ),
        managed_policies=[
            aws_iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole'),
            aws_iam.ManagedPolicy.from_aws_managed_policy_name('CloudWatchFullAccess'),
            aws_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonDynamoDBFullAccess"),
            aws_iam.ManagedPolicy.from_aws_managed_policy_name("AwsCloudFormationFullAccess"),
            aws_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMFullAccess"),
            aws_iam.ManagedPolicy.from_aws_managed_policy_name("AWSCodePipeline_FullAccess"),
            aws_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess")
            ])
        return role 
############################################################################