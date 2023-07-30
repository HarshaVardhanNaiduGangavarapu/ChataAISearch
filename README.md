# Chata.ai Search Service
### Author: Harshavardhan Naidu Ganagvarapu
This project is a Python Developer Coding Exercise as part of hiring process for Chata.ai.

## Table of Contents
- [Getting Started](#getting-started)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
    - [Docker](#docker)
    - [PyCharm](#pycharm)
    - [CLI](#cli)
- [Usage](#usage)


## Getting Started
This is a Flask standalone application which exposes APIs to search the arbitrary string provided by user and return the 
locations and sentence in which the string can be found.

## Prerequisites
We can run this application using Docker, PyCharm and CLI. Hence, we need Docker Desktop or PyCharm IDE along with 
Python runtime environment along with dependencies to be installed on the machine. 

## Installation
Go to the ChataAISearch(link: https://github.com/HarshaVardhanNaiduGangavarapu/ChataAISearch) Repository on GitHub and clone it to the machine.
Once we have the repository we can run the flask application as mentioned below.
 
## Docker
We need to have Docker installed on the Machine. After that, go inside the project root folder and build the docker image using following command:
```bash 
docker build -t chata.ai:1.0 .
```
Now we have build a docker image of the application using `Dockefile` present in root folder.
We can check the image we have built using following command:
```bash
docker images
```
Now lets run the flask application using following command:
```bash
docker run -d -p 5000:5000 chata.ai:1.0
```
If the port `5000` is already in use we can rerun the above command with a different port as shown below:
```bash
docker run -d -p 5001:5000 chata.ai:1.0
```
Now the application is up and running. We can access the API swagger specification at `http://127.0.0.1:5001/swagger/`. 
We test all the APIs in the swagger documentation page.

## PyCharm
Open the PyCharm IDE and import the project. We can run the application by clicking the run button on the tool bar.
We can also start the application by clicking on `Run` button at `app.run()` in `app.py` file.

## CLI
Open CLI and `cd` in to the root folder of the project. Once there then run the following command:
```bash
python -m flask run
```
Use `python3` if python version 3 is installed else use `python`. Make sure we have installed the dependecies along with it in machine.
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
