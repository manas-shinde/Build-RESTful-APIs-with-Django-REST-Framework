# Build-RESTful-APIs-with-Django-REST-Framework

The repository covers topics such as setting up a Django project, creating serializers, implementing authentication and permissions, handling requests and responses, versioning, pagination, and filtering. It also covers advanced topics such as handling file uploads, implementing nested resources, and creating custom renderers.

### Features :

1. Category
2. Products
3. Cart
4. User
5. create a order, update order status(only admin can do that)
6. Image Upload ( for products)
7. Generate a JSON Token to access specific API's
8. performance tests
9. Implemented caching
10. Running background tasks

• Authentication : JWT

• Parallel Tasking -> Celery

• Cache -> Redis

• Database -> PostgreSQL

## when you start locally :

```bash
mysql -u root -p

create database storefront3;

docker run -d -p 6379:6379 redis

python manage.py runserver
```

Docker File coming soon !

## Prerequisites

1. Basic understanding of Django structure

2. python version 3.8 or higher

3. Virtualization should be enable to run docker container

4. mysql server (in docker container also works)

## Table of Contents

[Installation](#installation)

[Usage](#usage)

[Contributing](#contributing)

[Pytest](#running-the-tests)

## Installation

To install the code in this repository, follow these steps:

1. Clone the repository:

   ```bash
    git clone https://github.com/manas-shinde/Build-RESTful-APIs-with-Django-REST-Framework.git

   ```

2. Create a virtual environment:

   ```bash
   python -m venv env

   ```

3. Activate the virtual environment:

   ```bash
   source env/bin/activate (Unix-based systems) or env\Scripts\activate (Windows)

   ```

4. Install the required packages:

   ```bash
    pip install -r requirements.txt

   ```

5. Create database in MySQL:

   ```bash
   CREATE DATABASE storefront3;

   ```

6. Migrate the database:

   ```bash
   python manage.py migrate
   ```

## Usage

To run the application, follow these steps:

6. Activate the virtual environment:

   ```bash
   source env/bin/activate (Unix-based systems) or env\Scripts\activate (Windows)

   ```

7. Run the development server:

   ```bash
   python manage.py runserver

   ```

8. Open a web browser and go to http://localhost:8000 to see the API homepage.

## Contributing

Contributions to this project are welcome! To contribute, follow these steps:

1. Fork this repository

2. Create a new branch for your feature:

   ```bash
   git checkout -b feature/my-feature

   ```

3. Make your changes and commit them:

   ```bash
   git commit -am 'Add some feature'

   ```

4. Push to the branch:

   ```bash
    git push origin feature/my-feature

   ```

5. Submit a pull request

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
