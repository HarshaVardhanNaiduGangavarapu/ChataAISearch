# Chata.ai Search Service
### Author: Harshavardhan Naidu Ganagvarapu
This project is a Python Developer Coding Exercise as part of hiring process for Chata.ai. We have used `KMP string search` algorithm, 
which effectively searches an `arbitrary string` of length `m` in a large text of length `n` with `O(n+m)` complexity.
We have also use `Flask-Caching` to effectively cache the large text file `king-i-150.txt` in memory and only read the file 
only if there are any modifications or cache-timeout. The default cache time we have used is `1 hour`.

## Table of Contents
- [Getting Started](#getting-started)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
    - [Docker](#docker)
    - [PyCharm](#pycharm)
    - [CLI](#cli)
- [Cloud Deployment](#cloud-deployment)
- [Swagger](#swagger)
- [Testing](#testing)
- [Log Files](#log-files)
- [Future Scope](#future-scope)


## Getting Started
This is a Flask standalone application which exposes APIs to search the arbitrary string provided by user and return the 
locations and sentence in which the string can be found. The large text file `king-i-150.txt` is available under `resources`
 folder.

## Prerequisites
We can run this application using any of the following: Docker, PyCharm and CLI. Hence, we need Docker Desktop or PyCharm IDE along with 
Python runtime environment and other dependencies to be installed on the machine. 

## Installation
Go to the ChataAISearch (https://github.com/HarshaVardhanNaiduGangavarapu/ChataAISearch) Repository on GitHub and clone it to the machine.
Once we have the repository we can run the flask application using steps mentioned below.
 
## Docker
If you prefer using Docker, make sure Docker is installed on your machine. Navigate to the project root folder and 
build the Docker image using the following command:
```bash 
docker build -t chata.ai:1.0 .
```
Now we have build a docker image of the application using `Dockefile` present in root folder.
You can check the image we have built using following command:
```bash
docker images
```
Now you can run the flask application using following command:
```bash
docker run -d -p 5000:5000 chata.ai:1.0
```
If the port `5000` is already in use you can rerun the above command with a different port as shown below:
```bash
docker run -d -p 5001:5000 chata.ai:1.0
```
Now the application is up and running. You can access the API swagger specification at `http://127.0.0.1:5001/swagger/` 
and test all the APIs in the swagger documentation page.

## PyCharm
If you prefer using PyCharm IDE, open the IDE and import the project.
You can run the application by clicking the `run` button on the `toolbar`, 
or by clicking on `Run` at `app.run()` in `app.py` file.

## CLI
For the command line interface, navigate to the root folder of the project and run the following command:
```bash
python -m flask run
```
If you have `Python` version `3` installed, use `python3` instead of `python`. 
Make sure you have installed the dependencies mentioned earlier.
If the dependencies modules are not present, then install using following commands:
````bash 
pip3 install flask
````
````bash 
pip3 install flask-swagger-ui
````
````bash 
pip3 install Flask-Caching
````
## Cloud Deployment
You can use the `Docker Image` built using the `Dockerfile` and push it to Container Registries such as 
`Docker Registry` of `Docker`, `ECR` of `AWS`, `GCR` of `GCP` and `Heroku Container Registry`.
You can then use Container Running Services like `Container Running Services` like `ECS` of `AWS` 
and other respective container services to pull the image from registries and run application in a cloud environment. 

## Swagger
The OpenAPI swagger specification is available in `swagger.json` file and and will be used to render the Swagger UI 
at `http://127.0.0.1:5000/swagger`.

## Testing
All the test cases for the application are available in `test_app.py` under root folder. 
Resources needed for test cases are available under `test_resources` folder.

## Log Files
The `logger` configuration is present in `log_config.py`. All logs are written to the console and also to a log file named 
`chataAISearch.log` available under `logs` folder in the project.

## Future Scope
In the future, we can add new APIs to allow users to upload large text files and store them in `HDFS`. We can also modify 
existing APIs to take the `filename` as input for searching arbitrary strings. This will enhance the functionality and scope of the application.