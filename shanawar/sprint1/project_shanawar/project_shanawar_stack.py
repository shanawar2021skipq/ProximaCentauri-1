# IMPORTING LIBRRARIES 
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
import os
from resources import constants
# CLASS FOR PROJECT STACK WHICH YOU CAN SEE AT CLOUDFORMATION
class ProjectShanawarStack(cdk.Stack):
    
    # INITIALIZATION FUNCTION 
    def __init__(self,scope:cdk.Construct, construct_id: str, **kwargs) -> None: 
        super().__init__(scope, construct_id, **kwargs)
        lambda_role=self.create_role()
        # WebHealth LAMBDA FUNCTION
        WebHealth_Lambda = self.create_lambda("WebHealthLambda","./resources","WebHealthLambda.lambda_handler",lambda_role) 
        # DynamoDB Lambda Function
        DBLambda = self.create_lambda("DynamoDBLambda","./resources","DynamoDBLambda.lambda_handler",lambda_role) 
        # Scheduling Lambda to have data for longer period of time
        self.schedule(1,WebHealth_Lambda)
        # Creating Alarm Table in DynamoDB
        self.create_table('Shanawar_Alarms_Table',DBLambda)
        topic =sns.Topic(self,"Web Health Emailing by Shanawar")
        self.snssubscriptions(topic,constants.EMAIL,DBLambda)
      #  for index,url in enumerate(constants.URLS):
        dimension={'Website URL':constants.URL_to_Monitor}
        
        # AVAILABILITY METRIC
        availability_metric = cloudwatch_.Metric(
        namespace=constants.URL_Monitor_Namespace,
        metric_name=constants.URL_Monitor_Name_Availability,
        dimensions_map=dimension,
        period= cdk.Duration.minutes(1))

        # AVAILABILITY ALARM FOR SKIPQ
        availability_alarm= cloudwatch_.Alarm(self,
        id="AvailabilityAlarm ",
        metric= availability_metric,
        comparison_operator=cloudwatch_.ComparisonOperator.LESS_THAN_THRESHOLD,
        datapoints_to_alarm=1,
        evaluation_periods=1,
        threshold=1)
        
          # LATENCY METRIC     
        Latency_metric = cloudwatch_.Metric(
        namespace=constants.URL_Monitor_Namespace,
        metric_name=constants.URL_Monitor_Name_Latency,
        dimensions_map=dimension,
        period= cdk.Duration.minutes(1))
        
        # LATENCY ALARM FOR SKIPQ
        latency_alarm= cloudwatch_.Alarm(self,
        id="LatencyAlarm ",
        metric= Latency_metric,
        comparison_operator=cloudwatch_.ComparisonOperator.GREATER_THAN_THRESHOLD,
        datapoints_to_alarm=1,
        evaluation_periods=1,
        threshold=0.28)
         #############################################################
        # ADD ALARM ACTIONS
        availability_alarm.add_alarm_action(actions_.SnsAction(topic))
        latency_alarm.add_alarm_action(actions_.SnsAction(topic))
        ######################################################
        #############################################################
              ############ SPRINT 2 CODE ADDITION #######
        rollback_metric=cloudwatch_.Metric(
        namespace='AWS/Lambda',
        metric_name='Duration',
        dimensions_map={'FunctionName':WebHealth_Lambda.function_name},
        period= cdk.Duration.minutes(1))
    
        rollback_alarm= cloudwatch_.Alarm(self,
        id="RollbackAlarm",
        metric= rollback_metric,
        comparison_operator=cloudwatch_.ComparisonOperator.GREATER_THAN_THRESHOLD,
        datapoints_to_alarm=1,
        evaluation_periods=1,
        threshold=2400) # THRESHOLD IS IN MILLISECONDS
        
  #      rollback_alarm.add_alarm_action(actions_.SnsAction(newtopic))

        alias = lambda_.Alias(self, "WebHealthLambdaAlias"+construct_id,alias_name="Lambda",
        version=WebHealth_Lambda.add_version("NewVersionWebHealthLambda")
        )

        codedeploy.LambdaDeploymentGroup(self, "WebHealthLambda_DeploymentGroup",
        alias=alias,
        deployment_config=codedeploy.LambdaDeploymentConfig.LINEAR_10_PERCENT_EVERY_1_MINUTE,
        alarms=[rollback_alarm]
        )

        
        

        availability_alarm.add_alarm_action(actions_.SnsAction(topic))
        latency_alarm.add_alarm_action(actions_.SnsAction(topic))
        ######################################################

        
  ################### CREATE LAMBDA FUNCTION ###################
    def create_lambda(self,newid,asset,handler,role):
        return lambda_.Function(self, id=newid,
        runtime=lambda_.Runtime.PYTHON_3_8, 
        handler=handler,
        code=lambda_.Code.from_asset(asset),
        role=role,
        timeout= cdk.Duration.minutes(5))
 ################################################################
    def schedule(self,Duration,handler,):
        lambda_schedule= events_.Schedule.rate(cdk.Duration.minutes(1))
        lambda_target= targets_.LambdaFunction(handler=handler)
        rule= events_.Rule(self,"WebHealthInvoke",description="Periodic Lambda",enabled=True,schedule=lambda_schedule,targets=[lambda_target])
##################################################################        
    def create_table(self,table_name,dblambda):
        # CREATING DYNAMODB TABLE        
        dbtable = dynamodb_.Table(self, "ShanawarDBTable",table_name=table_name,
        partition_key=dynamodb_.Attribute(name="MessageID", type=dynamodb_.AttributeType.STRING))
        dbtable.grant_read_write_data(dblambda)
        dblambda.add_environment('table_name',table_name)
####################################################################
    def create_role(self):
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
#########################################################################
    def snssubscriptions(self,topic,email,dblambda):
        topic.add_subscription(subscriptions_.EmailSubscription(email))
        topic.add_subscription(subscriptions_.LambdaSubscription(dblambda))
################################################################################
""""
    def create_metric(self,namespace,dimension,metric_name):
        metric = cloudwatch_.Metric(
        namespace=namespace,
        metric_name=metric_name,
        dimensions_map=dimension,
        period= cdk.Duration.minutes(1))
        return metric
"""