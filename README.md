This scrapy framework is built on pythonanywhere and AWS.

# Prerequisite

1. Set up [pythonanywhere](https://www.pythonanywhere.com/), i.e., mysql and app server.
2. Install [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html), get credential created, and deploy cloudformation template.
3. Create a email sender's gmail account and setup App Password.
4. Update secrets.cfg. Then run ddl.sql to create tables in database.
5. For devtest, install mysql server on your local machine.

# AWS setup

## Deploy AWS resources

Install the required dependencies.

```
$ pip install -r requirements-dev.txt
```

Run Bootstrap for first time deployment.

```
$ cdk bootstrap
```

Synthesize the CloudFormation template for this code.

```
$ cdk synth
```

Deploy the CloudFormation template.

```
$ cdk deploy --all
```

# Docker setup for AWS ECR (x86_64)

1. Install [Docker](https://docs.docker.com/desktop/install/mac-install/)
2. Pull Amazon Linux image: `docker pull amazonlinux`, only need for the first time.
3. Build our docker image: `docker build -t rent-spider .`
4. Publish docker image to ECR with commands provided by AWS ECR.

# Test Docker locally

```
# Start docker service
sudo systemctl start docker.service

# Build a image with DockerFile in current folder ., add a tag rent_spider
docker build -t rent-spider .

# Run a image in a container with interactive mode
docker run -it --name rent-spider rent-spider bash

# If container already exist, start it
docker start -i rent-spider
```

Run the script to see if it works

```
cd rent_spider; git pull; xvfb-run -- python3 main.py -u -r -a
```

# Test run ECS task (once)

Replace your task revision if needed.

```
aws ecs run-task\
	--cluster rent-spider\
	--launch-type FARGATE\
	--task-definition rent-spider:3\
	--network-configuration "awsvpcConfiguration={subnets=[subnet-eee2b1c0],securityGroups=[sg-0dcba158481062d20],assignPublicIp=ENABLED}"
```

# Local setup

## Pip libraries Install

```
pip install -U pip
pip install -r requirements.txt
python3 -m playwright install firefox
```

## Test Fetch

```
python3 main.py
```

Debug mode: `export DEBUG=pw:api`

## Test SQL database

```
mysql -u root -p
use ppttzhu$default
```

## Test Web App

```
python3 flask_app/app.py
```

Then go to: http://127.0.0.1:3000/

## Test Download

```
python3 download.py
```

## Run Unit Test

```
python3 -m unittest
```

# References

- How access mysql in pythonanywhere from local machine: https://help.pythonanywhere.com/pages/AccessingMySQLFromOutsidePythonAnywhere/
- How to use selenium in pythonanywhere: https://help.pythonanywhere.com/pages/selenium/
- Mysql API guide: https://mysqlclient.readthedocs.io/user_guide.html#mysql-c-api-function-mapping
- How to setup gmail smtp: https://stackoverflow.com/questions/28421887/django-email-with-smtp-gmail-smtpauthenticationerror-534-application-specific-pa
- Gmail smtp App password troubleshooting: https://kinsta.com/blog/gmail-smtp-server/
- Playwright python doc: https://playwright.dev/python/docs/intro
