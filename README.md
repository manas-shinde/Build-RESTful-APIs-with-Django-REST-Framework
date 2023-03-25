# Build-RESTful-APIs-with-Django-REST-Framework

The repository covers topics such as setting up a Django project, creating serializers, implementing authentication and permissions, handling requests and responses, versioning, pagination, and filtering. It also covers advanced topics such as handling file uploads, implementing nested resources, and creating custom renderers.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Basic understanding of Django structure

python version 3.8 or higher

virtualization should be enable to run docker container

### Installing

### Features :

1. Category
2. Products
3. Cart
4. User , User Group
5. Image Upload ( not configured )

• Authentication : JWT (JSON Token)

• Parallel Tasking -> Celery

• Cache -> Redis

• Database -> MySQL

when you start locally :

```
sudo service postgresql start
docker run -p 6379:6379 redis
python manage.py runserver
```

Docker File coming soon !

## Running the tests

To run tests, run the following command

```bash
  pytest
```

OR
If you are using Vscode then can setup test up pytest in Vscode to Root Directory.

### Break down into end to end tests

To run tests related to collection endpoint only use below command :

```

python -m pytest ./store/tests/test_collections.py

```
