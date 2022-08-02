This scrapy framework is built on pythonanywhere.

# Prerequisite

1. Set up pythonanywhere, like mysql and app server.
2. Create a email sender's gmail account and setup App Password.
3. Update secrets.cfg. Then run ddl.sql to create tables in database.
4. For devtest, install mysql server on your local machine.

# Docker (for x86_64)

5. Install [Docker](https://docs.docker.com/desktop/install/mac-install/)
6. Install [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
7. Pull Amazon Linux image: `docker pull amazonlinux`
8. Build our docker image: `docker build -t rent_spider .`
9. Publish docker image to ECR with commands provided by AWS ECR.
10. Set ECS command to `cd rent_spider; git pull; xvfb-run -- python3 main.py -r -i QLIC SkylineTower`

# Install

```
pip install -U pip
pip install -r requirements.txt
python3 -m playwright install firefox
```

# Test Fetch

```
python3 main.py
```

# Test Web App

```
export FLASK_APP=flask_app/app.py && export FLASK_ENV=development && python3 -m flask run -p 3000
```

Then go to: http://127.0.0.1:3000/

# Run Unit Test

```
python3 -m unittest
python3 -m unittest tests/test_database.py
```

# References

- How access mysql in pythonanywhere from local machine: https://help.pythonanywhere.com/pages/AccessingMySQLFromOutsidePythonAnywhere/
- How to use selenium in pythonanywhere: https://help.pythonanywhere.com/pages/selenium/
- Mysql API guide: https://mysqlclient.readthedocs.io/user_guide.html#mysql-c-api-function-mapping
- How to setup gmail smtp: https://stackoverflow.com/questions/28421887/django-email-with-smtp-gmail-smtpauthenticationerror-534-application-specific-pa
- Gmail smtp App password troubleshooting: https://kinsta.com/blog/gmail-smtp-server/
