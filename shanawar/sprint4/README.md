
<h1 align="center">  Sprint 4: Build a Front-End user-interface for the CRUD API Gateway using ReactJS
  
## Description
Build a Front-End user-interface for the CRUD API Gateway using ReactJS. The user interface should allow users to see and search the database (DynamoDB) and should load URLs with pagination. Login should be enabled through React with authentication using AWS Cognito or equivalent OAuth method. The React app can be rendered with an AWS Lambda Function. Use the library of foundational and advanced components and design system in Chakra UI to develop your React application
  
## Concepts
*	Learn how to create a Front-End app with ReactJS 
* Learn how to enable authentication using OAuth method 
* Write accessible React apps using readily available UI libraries. 
  
## Technologies
* AWS API Gateway
*  AWS Amplify
*  AWS Cognito
*  Dynamodb
* S3 buckets
* AWS Lambda
*  AWS Cloudwatch
*  AWS SNS

  
## Installing and Running Project

* `git clone https://github.com/shanawar2021skipq/ProximaCentauri.git`
* `cd ProximaCentauri`
* `cd shanawar`
* `cd sprint4`
* `source .venv/bin/activate`
* `pip install -r requirements.txt`
* `cdk bootstrap --qualifier <qualifier> --toolkit-stack-name <nametoolkit> --cloudformation-execution-policies arn:aws:iam::aws:policy/AdministratorAccess <account>/<region>`
* `cdk deploy <pipelinename>`
* `pytest <testfolder>`
  
## Outputs
 ### Cognito Login
![image](https://user-images.githubusercontent.com/96059754/148870758-b8e91154-ccbf-4870-a035-0b6525f0a9d7.png)
### UI
![image](https://user-images.githubusercontent.com/96059754/148871975-0882d13b-7791-48fa-be85-83db85d14b1b.png)

## Support
  Email: shanawar.ali.chouhdry.s@skipq.org 
