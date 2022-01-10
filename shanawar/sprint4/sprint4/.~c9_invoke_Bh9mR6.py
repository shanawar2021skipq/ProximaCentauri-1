from aws_cdk import (
    core as cdk,
    aws_lambda as lambda_,
    aws_events as events_,
    aws_events_targets as targets_,
    aws_iam,
    aws_cloudwatch as cloudwatch_,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions_,
    aws_cloudwatch_actions as actions_,
    aws_dynamodb as dynamodb_,
    aws_codedeploy as codedeploy
) 
from resources import constants as constants
import os

class Sprint2Stack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
    
        lambda_role=self.create_lambda_role()
        
        # WebHealth LAMBDA FUNCTION
        WebHealthLambda = self.create_lambda("WebHealthLambda","./resources","healthweb_lambda.lambda_handler",lambda_role) 
        # DYNAMODB LAMBDA FUNCTION
        DBLambda = self.create_lambda("DynamoDBLambda","./resources","dynamodb_lambda.lambda_handler",lambda_role) 
                
        
        lambda_schedule= events_.Schedule.rate(cdk.Duration.minutes(1))
        lambda_target= targets_.LambdaFunction(handler=WebHealthLambda)
        rule= events_.Rule(self,"WebHealthInvoke",description="Periodic Lambda",enabled=True,schedule=lambda_schedule,targets=[lambda_target])
        
        dbtable = dynamodb_.Table(self, "ShanawarDBTable",
        partition_key=dynamodb_.Attribute(name="MessageID", type=dynamodb_.AttributeType.STRING))
        dbtable.grant_read_write_data(DBLambda)
        DBLambda.add_environment('table_name',dbtable.table_name)
        
        
        newtopic =sns.Topic(self,"Web Health by Shanawar")
        newtopic.add_subscription(subscriptions_.EmailSubscription('shanawar.ali.chouhdry.s@skipq.org'))
        # DYNAMODB SUBSCRIPTION
        newtopic.add_subscription(subscriptions_.LambdaSubscription(DBLambda))
        
     # AVAILABILITY ALARM    
        dimenesion= {'URL':constants.URL_to_Monitor} 
        availability_metric = cloudwatch_.Metric(
        namespace=constants.URL_Monitor_Namespace,
        metric_name=constants.URL_Monitor_Name_Availability,
        dimensions_map=dimenesion,
        period= cdk.Duration.minutes(1))
        
        availability_alarm= cloudwatch_.Alarm(self,
        id="AvailabilityAlarm",
        metric= availability_metric,
        comparison_operator=cloudwatch_.ComparisonOperator.LESS_THAN_THRESHOLD,
        datapoints_to_alarm=1,
        evaluation_periods=1,
        threshold=1)
        
     # LATENCY ALARM     
        dimenesion= {'URL':constants.URL_to_Monitor}
        Latency_metric = cloudwatch_.Metric(
        namespace=constants.URL_Monitor_Namespace,
        metric_name=constants.URL_Monitor_Name_Latency,
        dimensions_map=dimenesion,
        period= cdk.Duration.minutes(1))
        
        latency_alarm= cloudwatch_.Alarm(self,
        id="LatencyAlarm",
        metric= Latency_metric,
        comparison_operator=cloudwatch_.ComparisonOperator.GREATER_THAN_THRESHOLD,
        datapoints_to_alarm=1,
        evaluation_periods=1,
        threshold=0.25)
#############################################################
        ############ SPRINT 2 CODE ADDITION #######
        # DEFININING ROLLBACK METRIC
        rollback_metric=cloudwatch_.Metric(
        namespace='AWS/Lambda',
        metric_name='Duration',
        dimensions_map={'FunctionName':WebHealthLambda.function_name},
        period= cdk.Duration.minutes(1))
        
        # DEFININING ROLLBACK ALARM
        rollback_alarm= cloudwatch_.Alarm(self,
        id="RollbackAlarm",
        metric= rollback_metric,
        comparison_operator=cloudwatch_.ComparisonOperator.GREATER_THAN_THRESHOLD,
        datapoints_to_alarm=1,
        evaluation_periods=1,
        threshold=800) # THRESHOLD IS IN MILLISECONDS
        
        rollback_alarm.add_alarm_action(actions_.SnsAction(newtopic))
        version = WebHealthLambda.add_version("NewVersion")
        alias = lambda_.Alias(self, "Shanawar_WebHealthLambdaAlias"+construct_id,alias_name="Shanawar_Lambda_Alias"+construct_id,version=version)#WebHealthLambda.current_version)
        
        """
        Parameters
        scope (Construct) –
        
        id (str) –
        
        alias (Alias) – Lambda Alias to shift traffic. 
        
        alarms (Optional[Sequence[IAlarm]]) – The CloudWatch alarms associated with this Deployment Group. 
        
        auto_rollback (Optional[AutoRollbackConfig]) – The auto-rollback configuration for this Deployment Group. Default: - default AutoRollbackConfig.
        
        deployment_config (Optional[ILambdaDeploymentConfig]) – The Deployment Configuration this Deployment Group uses. Default: LambdaDeploymentConfig.CANARY_10PERCENT_5MINUTES
        
        """
        # Linear: Traffic is shifted in equal increments with an equal number of minutes between each increment. 
        # linear options specify the percentage of traffic that's shifted in each increment and the number of minutes between each increment.

        codedeploy.LambdaDeploymentGroup(self, "Shanawar_WebHealthLambda_DeploymentGroup",
        alias=alias,
        deployment_config=codedeploy.LambdaDeploymentConfig.LINEAR_10_PERCENT_EVERY_1_MINUTE,   
        alarms=[rollback_alarm]
        )

############################################################
 
        availability_alarm.add_alarm_action(actions_.SnsAction(newtopic))
        latency_alarm.add_alarm_action(actions_.SnsAction(newtopic))
        
 ############ LAMBDA ROLE ##############################       
    
    def create_lambda_role(self):
        lambdaRole=aws_iam.Role(self,"lambda-role",
        assumed_by=aws_iam.CompositePrincipal(
            aws_iam.ServicePrincipal("lambda.amazonaws.com"),
            aws_iam.ServicePrincipal("sns.amazonaws.com")
            ),
        managed_policies=[
            aws_iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole'),
            aws_iam.ManagedPolicy.from_aws_managed_policy_name('CloudWatchFullAccess'),
            aws_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonDynamoDBFullAccess"),
            aws_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSNSFullAccess")
            ])
        return lambdaRole

 #############################################################       
  ################### CREATE LAMBDA FUNCTION ################
    def create_lambda(self,newid,asset,handler,role):
        return lambda_.Function(self, id=newid,
        runtime=lambda_.Runtime.PYTHON_3_6, 
        handler=handler,
        code=lambda_.Code.from_asset(asset),
        role=role)
 ########################################################    