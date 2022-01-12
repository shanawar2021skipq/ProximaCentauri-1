from aws_cdk import (
    core as cdk,
    aws_lambda as lambda_,
    aws_events as events_,
    aws_events_targets as targets_,
    aws_lambda_event_sources as sources_,
    aws_iam,
    aws_cloudwatch as cloudwatch_,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions_,
    aws_cloudwatch_actions as actions_,
    aws_dynamodb as dynamodb_,
    aws_codedeploy as codedeploy,
    aws_s3 as s3,
    aws_apigateway as apigateway,
    aws_cognito ,
    aws_amplify
) 
from resources import constants as constants
from resources.bucket import Bucket as s
import resources.read as read
import os,boto3

class Sprint4Stack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        # CREating Lambda Roles
        lambda_role=self.create_lambda_role()
        # WebHealth LAMBDA FUNCTION
        WebHealthLambda = self.create_lambda("WebHealthLambda","./resources","healthweb_lambda.lambda_handler",lambda_role) 
        # DYNAMODB LAMBDA FUNCTION
        DBLambda = self.create_lambda("DynamoDBLambda","./resources","dynamodb_lambda.lambda_handler",lambda_role) 
        
        

        ### Class Object ###
       # s3_bucket.create('shanawarbucket')
        s('shanawarbucket','urls.json').store_urls('shanawarbucket')
        URLS = s('shanawarbucket','urls.json').get_bucket()
        #########################
        
        lambda_schedule= events_.Schedule.rate(cdk.Duration.minutes(1))
        lambda_target= targets_.LambdaFunction(handler=WebHealthLambda)
        rule= events_.Rule(self,"WebHealthInvoke",description="Periodic Lambda",enabled=True,schedule=lambda_schedule,targets=[lambda_target])
        
        dbtable = dynamodb_.Table(self, "Shanawar_Alarm_Table",
        partition_key=dynamodb_.Attribute(name="MessageID", type=dynamodb_.AttributeType.STRING))
        dbtable.grant_read_write_data(DBLambda)
        DBLambda.add_environment('table_name',dbtable.table_name)
        
        newtopic =sns.Topic(self,"SNS Topic For Web Health by Shanawar")
        # EMAIL SUBSCRIPTION
        newtopic.add_subscription(subscriptions_.EmailSubscription('shanawar.ali.chouhdry.s@skipq.org'))
        # DYNAMODB SUBSCRIPTION
        newtopic.add_subscription(subscriptions_.LambdaSubscription(DBLambda))
                
        ##################################     SPRINT 4   ###########################################
        ##################################     Cognito    ###########################################
        
        # Creating User pools allow creating and managing your own directory of users that can sign up and sign in
        user_pool = aws_cognito.UserPool(self, 'shanawar_UserPool',
          removal_policy=cdk.RemovalPolicy.DESTROY,
          self_sign_up_enabled=True,
          sign_in_aliases={'email': True},
          auto_verify={'email': True},
          password_policy={
            'min_length': 8,
            'require_lowercase': False,
            'require_digits': False,
            'require_uppercase': False,
            'require_symbols': False,
          },
          account_recovery=aws_cognito.AccountRecovery.EMAIL_ONLY
        )
        
        ## App Client for userpools
        user_pool_client = aws_cognito.UserPoolClient(self, 'UserPoolClient',
          user_pool=user_pool,
          auth_flows={
            'admin_user_password': True,
            'user_password': True,
            'custom': True,
            'user_srp': True},
        #Authentication flows allow users on a client to be authenticated with a user pool. Cognito user pools provide several different types of authentication
            o_auth=aws_cognito.OAuthSettings(
    ##The following code configures an app client with the authorization code grant flow and registers the the app’s UI page as a callback (or redirect) URL. 
            flows=aws_cognito.OAuthFlows(
                implicit_code_grant=True
            ),
            callback_urls=["https://671c0ee4b1de43fa9976038a687a2d5a.vfs.cloud9.us-east-2.amazonaws.com/"]    # Callback URL will redirect after sign up to UI 
          ),
          supported_identity_providers=[aws_cognito.UserPoolClientIdentityProvider.COGNITO]
        )
        
        ## AUTHORIZER FOR API
        auth = apigateway.CognitoUserPoolsAuthorizer(self, 'AuthorizerForApi',cognito_user_pools=[user_pool])
        
        
        
        ##################################     SPRINT 3   ###########################################
        ################################## TABLE FOR URLS ###########################################
        
        urls_table=dynamodb_.Table(self,id='ShanawarUrls',
        partition_key=dynamodb_.Attribute(name="Links", type=dynamodb_.AttributeType.STRING))
        apilambda = self.create_lambda('api',"./resources",'api_lambda.lambda_handler',lambda_role)

        ########## FULL ACCESS TO URLS AND CREATING ENVIRONMENT VARIABLE FOR S3DYNAMO AND WebHealth LAMBDA #########
        
        urls_table.grant_read_write_data(WebHealthLambda)
        WebHealthLambda.add_environment(key = 'table_name', value = urls_table.table_name)
        
        #########################   API #################################
        myapi=apigateway.LambdaRestApi(self,"SHANAWAR_ALI_API",handler=apilambda,default_cors_preflight_options={
        "allow_origins": apigateway.Cors.ALL_ORIGINS})
        
        apilambda.add_environment(key = 'table_name', value = urls_table.table_name)
        
        ######################### creating API gateway ###################
        apilambda.grant_invoke( aws_iam.ServicePrincipal("apigateway.amazonaws.com"))
        urls_table.grant_read_write_data(apilambda) 
                
        items = myapi.root.add_resource("items")
     #    Allowed methods: ANY,OPTIONS,GET,PUT,POST,DELETE,PATCH,HEAD POST /items
     
       # CRUD OPERATIONS
        items.add_method("PUT",authorization_type=apigateway.AuthorizationType.COGNITO,authorizer=auth) # CREATE: ADD URL TO TABLE
        items.add_method("GET",authorization_type=apigateway.AuthorizationType.COGNITO,authorizer=auth) # READ: GET ALL URLS FROM TABLE
        items.add_method("POST",authorization_type=apigateway.AuthorizationType.COGNITO,authorizer=auth) # UPDATE: UPDATE URL IN TABLE
        items.add_method("DELETE",authorization_type=apigateway.AuthorizationType.COGNITO,authorizer=auth) # DELETE: DELETE URL FROM TABLE
        
        
        cdk.CfnOutput(self, 'UserPoolId', value=user_pool.user_pool_id)
        cdk.CfnOutput(self, 'UserPoolClientId', value=user_pool_client.user_pool_client_id)

       
        ##############################################################################################
        
      
        for url in URLS:
             ############################## Availability metrics and alarm for availability ###############################
            #client.put_item(TableName = ,Item={'Links':{'S': url}})
            dimension={'URL': url}
            availability_matric=cloudwatch_.Metric(namespace=constants.URL_Monitor_Namespace,
            metric_name = constants.URL_Monitor_Name_Availability+url,
            dimensions_map=dimension,
            period=cdk.Duration.minutes(1))
            
            availability_alarm= cloudwatch_.Alarm(self,
            id = 'Availability_Alarm:'+url,
            metric = availability_matric,
            comparison_operator= cloudwatch_.ComparisonOperator.LESS_THAN_THRESHOLD,
            datapoints_to_alarm=1,
            evaluation_periods = 1,
            threshold = 1
            )
            
             ############################## Latency Metrics and Latency alarms ##############################
            latency_matric=cloudwatch_.Metric(namespace=constants.URL_Monitor_Namespace,
            metric_name = constants.URL_Monitor_Name_Latency+url,
            dimensions_map=dimension,
            period=cdk.Duration.minutes(1))
            
            latency_alarm= cloudwatch_.Alarm(self,
            id = 'Latency_Alarm:'+url,
            metric = latency_matric,
            comparison_operator= cloudwatch_.ComparisonOperator.GREATER_THAN_THRESHOLD,
            datapoints_to_alarm=1,
            evaluation_periods = 1,
            threshold = 0.25
            )
             
            availability_alarm.add_alarm_action(actions_.SnsAction(newtopic))
            latency_alarm.add_alarm_action(actions_.SnsAction(newtopic))



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
        threshold=2500) # THRESHOLD IS IN MILLISECONDS
        
        rollback_alarm.add_alarm_action(actions_.SnsAction(newtopic))
        alias = lambda_.Alias(self, "Shanawar_WebHealthLambdaAlias"+construct_id,alias_name= 'Shanawar'+construct_id,version=WebHealthLambda.current_version)#)

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
            aws_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSNSFullAccess"),
            aws_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess")
            ])
        return lambdaRole

 #############################################################       
  ################### CREATE LAMBDA FUNCTION ################
    def create_lambda(self,newid,asset,handler,role):
        return lambda_.Function(self, id=newid,
        runtime=lambda_.Runtime.PYTHON_3_6, 
        handler=handler,
        code=lambda_.Code.from_asset(asset),
        timeout=cdk.Duration.minutes(5),
        role=role)
 ########################################################    