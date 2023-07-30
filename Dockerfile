# Runs on python base image
FROM python:3.8-slim-buster

# working directory in the container
WORKDIR /chata

# copy the contents
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .

# Create log directories along with permissions
RUN mkdir /chata/logs
RUN chmod 666 /chata/logs

# Create an empty log file along with permissions
RUN touch /chata/logs/chataAISearch.log
RUN chmod 666 /chata/logs/chataAISearch.log

# start the program
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
