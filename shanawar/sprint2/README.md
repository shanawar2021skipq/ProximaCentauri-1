
<h1 align="center">  Sprint 2: Multi-Stage Pipeline for Webcrawler 
  
## Description
A multistage pipeline having Beta/gamma and Prod stage with unit/integration tests for webcrawler and automated rollback to the last build.
  
## Concepts
  * Introduction to CI/CD
  * AWS Services: Codepipeline for build and test, CodeDeploy for CD
  * Integrate AWS Codepipeline with GitHub
  * Pytest automated testing
  * Operational metric and alarm for webcrawler
  * Automated Rollback to last build
  
## Installing and Running Project


https://user-images.githubusercontent.com/96059754/147419249-7c3fc66a-c0f9-4050-a34c-8a34921d245c.mp4


## Commands
* `git clone https://github.com/shanawar2021skipq/ProximaCentauri.git`
* `cd ProximaCentauri`
* `cd shanawar`
* `cd sprint2`
* `source .venv/bin/activate`
* `cdk bootstrap --qualifier <qualifier> --toolkit-stack-name <nametoolkit> --cloudformation-execution-policies arn:aws:iam::aws:policy/AdministratorAccess <account>/<region>`
* `cdk deploy <pipelinename>`
* `pytest <testfolder>`
  
## Outputs
  

https://user-images.githubusercontent.com/96059754/147419263-6524265a-75a0-4301-8a79-849d0a97dd35.mp4



## Useful commands
 
 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation
## 
Enjoy!
