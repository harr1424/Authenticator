# Authenticator

### Account based authenitcation using FastAPI

This repository contains a basic front-end registration page where clients are able to register an account. The registration process involves storing user credentials (passwords are salted and hashed, never stored as cleartext) in a DynamoDB table, provisioned using Terraform. The front-end registration service runs on an nginx server inside of a docker container. The back-end authenitcation service is implemented using FastAPI and also runs inside of a docker container. A `docker-compose.yml` files has been created in order to integrate these containers with Amazon ECS and create a Cloud Formation stack used to run the entire authenitcation suite consisting of the front end registration page, DynamoDB table, and back-end API along with other resources required by AWS. 

More information about this project, completed during a course in Cloud Computing, can be found <a href="https://harr1424.github.io/cloud_computing.html">here</a>. 
