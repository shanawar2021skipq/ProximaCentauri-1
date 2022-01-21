
<h1 align="center">  Sprint 5: Create a dockerized container for API test clients.
  
## Description
Use docker-compose to build API test clients using pyresttest. These tests will exercise the web crawler's CRUD endpoint built in the previous sprint. Publish built images to Elastic Container Registry (ECR). Deploy API test clients from Sprint 4 on an EC2 instance/ AWS Fargate. Build and push API test dockers through CodePipeline. Push API test results into CloudWatch. Setup alarming and notification on API test metrics.
## Concepts
*	Learn AWS services: ECR 
*	Learn docker: DockerFile, Image, Containers. Docker commands [build, start/stop container, deleting container]. 
*	Learn container registries: Working with images (Pull/Push), auto-updates to pull new images once published 
*	Learn API functional testing framework: pyresttest 
*	Learn AWS Services: EC2 and AWS Fargate  
*	Extend tests and prod/beta Cl/CD pipelines in CodeDeploy / CodePipeline
  
## Technologies
* AWS ECS
*  AWS ECR
* AWS EC2
*  Docker
* pyresttest
*  Dynamodb
*  AWS Cloudwatch
*  AWS SNS
 ## Docker Commands
 *  `docker build -t <docker image name> .`
 * `docker run <image name> <apiurl> <test.yaml>`
### Push Image to ECR
Create a repo in ECR.
Retrieve an authentication token and authenticate your Docker client to your registry.
Use the AWS CLI:
 * `aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin <reponame> `
 * `docker push <imagename>`
## Installing and Running Project

* `git clone https://github.com/shanawar2021skipq/ProximaCentauri.git`
* `cd ProximaCentauri`
* `cd shanawar`
* `cd sprint5`
* `source .venv/bin/activate`
* `pip install -r requirements.txt`
* `cdk bootstrap --qualifier <qualifier> --toolkit-stack-name <nametoolkit> --cloudformation-execution-policies arn:aws:iam::aws:policy/AdministratorAccess <account>/<region>`
* `cdk deploy <pipelinename>`
* `pyresttest <apiurl> <test.yaml> --log debug`

## Support
  Email: shanawar.ali.chouhdry.s@skipq.org 
