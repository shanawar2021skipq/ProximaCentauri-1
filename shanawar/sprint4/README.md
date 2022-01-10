
<h1 align="center">  Sprint 3: Build CRUD API Gateway endpoint for the Web Crawler 
  
## Description
Build a public CRUD API Gateway endpoint for the web crawler to create/read/update/delete the target list containing the list of websites/webpages to crawl along with extended tests in each stage to cover the CRUD operations and DynamoDB read/write time.
  
## Concepts
*	Learn AWS Services: API Gateway, DynamoDB  
*	Write a RESTful API Gateway interface for web crawler CRUD operations 
*	Write a Python Function to implement business logic of CRUD into DynamoDB
*	Extend tests and prod/beta Cl/CD pipelines in CodeDeploy / CodePipeline 
*	Use Cl/CD to automate multiple deployment stages (prod vs beta)

  
## Installing and Running Project


https://user-images.githubusercontent.com/96059754/147419249-7c3fc66a-c0f9-4050-a34c-8a34921d245c.mp4


## Commands
* `git clone https://github.com/shanawar2021skipq/ProximaCentauri.git`
* `cd ProximaCentauri`
* `cd shanawar`
* `cd sprint3`
* `source .venv/bin/activate`
* `pip install -r requirements.txt`
* `cdk bootstrap --qualifier <qualifier> --toolkit-stack-name <nametoolkit> --cloudformation-execution-policies arn:aws:iam::aws:policy/AdministratorAccess <account>/<region>`
* `cdk deploy <pipelinename>`
* `pytest <testfolder>`
  
## Outputs
  
https://user-images.githubusercontent.com/96059754/148003247-1574f012-a32a-4eda-9d8c-30591a34bc33.mp4


## Useful commands
 
 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation
## 
## Support
  Email: shanawar.ali.chouhdry.s@skipq.org 
