# bruvio biotech-dashboard

Creating my own dashboard to visualize and explore a dataset containing drug related simulated data.

The app will read the dataset. The user can interact by choosing a subset of the data to plot, and see an exponential fit.

### 1. Initial Setup

**Quick Setup** (prereq: `git, python3.8`,`docker` )

```bash
git clone <reponame>
python -m venv .env3.8
pip install -r requirements.txt
```

Optional: It is recommended that you first run the Jupyter notebook contained in the repository. This helps explore the data and understand how the dashboard works under the hood.

The Jupyter notebook contains also an initial and untuned xgboost regressor.

#### Project Structure:

Mono-repo style

```
├──app/
    ├── __init__.py
    ├── ─wsgi.py
    ├── data
    │   ├── dataset1.csv
    │   ├── dataset2.csv
    │   ├── dataset3.csv
    ├── templates
    │   ├── core-infrastructure-setup.yml
    │   ├── confecs-webapp-stacktest.yml
    ├── tests
    │   ├── test_app.py
    │   ├── conftest.py
    └── src
        ├── __init__.py
        ├── app.py
        └── utils
            ├── __init__.py
            ├── data.py
            ├── aws_s3.py
            ├── fitting_functions.py
    ├──Dockerfile
    ├──docker-compose.yml
    ├──pytest-compose.yml
    ├──.pylintrc
    ├──.gitignore
    ├──.pre-commit-config.yaml
    ├──isort.cfg
    ├──requirements-dev.txt
    ├──requirements.txt
    ├──README.md
    ├──.github
    ├──AWS_deploy.sh
    ├──docker-task.sh
    ├──run.sh



```

- `app/wsgi.py`: contains the entrypoint for the application.
- `app/tests/`: tests for basic operations on the app.
- `app/utils/`: help functions
- `app/data/`: folder with input datasets
- `app/templates/`: AWS cloudformation scripts
- `app/src/`: source file of the app
- `app/src/app.py`: main file
- `app/src/aws_s3.py`: help script to be used in a later stage when AWS (cloud vendor of choice) will be used to store and read the data
- `Dockerfile`: dockerfile for building an image and future deployment to AWS (or other cloud provider)
- `pytest-Dockerfile`: dockerfile for local testing
- `.github`: folder containing 2 workflows for automation: one tests the app in a github runner, the second builds a docker image
- `docker-task`: script to simplify operations with docker
- `AWS_deploy.sh`: script to deploy on AWS

### 4. Starting the environment

To start the app locally from the terminal run

`./run.sh`

The service will start listening at

`http://127.0.0.1:8000`

### 5. Building Docker image

To create a docker image run

```
docker build -t bruvio-biotech .
```

### 6. Running app from container locally

To run the app from the container locally run from the terminal

```
docker run -i -p 8000:8000 -d bruvio-biotech
```

and then from the browser visit

```
localhost:8000
```

### 7. local testing using a docker container

To run a local test using a docker container run

```
docker-compose up
```

### 8. deploy to AWS

to deploy to AWS, I included two bash script to simplify operation

A prerequisite is to have setup AWS cli and a profile.

Run first

`./docker-task.sh showUsage`

this will display how to use the script

First create a new repository on ECR

`./docker-task.sh createrepo`

then build and push the docker image to ECR

`./docker-task.sh buildpush`

This will push into your ECR repository called biotech (edit the docker-task.sh file to change defaults name)

now just run

`./AWS_deploy.sh`

this will start the creation of two Cloudformation stacks: 1) for the core infrastructure (VPC, SG, subnets..) the other will start a ECS cluster.

After 5/10 minutes you will find on the terminal the DNS of the application load balancer.
Copy and paste it into a browser tab to launch the app.

## Authors

- **Bruno Viola** - _Initial work_ - [bruvio](https://github.com/bruvio)
