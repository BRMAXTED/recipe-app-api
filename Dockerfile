# Defines the Docker image 'Python': and the image tag 'alpine3.19'
# Alpin is a stripped down version of linux
FROM python:alpine3.19
# Just some Meta Data
LABEL maintainer="Bradley"

ENV PYTHONUNBUFFERED 1 

# copies the requirements file from the local machine to /tmp/requirements.txt
# this copy will move the requirements file into the docker image
# this is used to install the python requirements
COPY ./requirements.txt /tmp/requirements.txt
# copies the dev requirements (linters, etc)
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
# copies the app directory 
COPY ./app /app
# sets the working directory where the django app will be located
WORKDIR /app  
# this exposes the port 8000 form the container to the machine
EXPOSE 8000


# sets the DEV arguments to false, overriding the docker-compose DEV argument
ARG DEV=false
# run command to install dependancies
# the "&& \" breaks the command into multiple lines
# python -m venv /py                                      || create a new virtual environment where the dependancies are installed
# /py/bin/pip install --upgrade pip                       || upgrades pip for the virtual environment
# /y/bin/pip install -r /tmp/requirements.txt             || installs the list of pip requirments inside the virtual environment
# if [$DEV = "true"]; \                                     
#     then /py/bin/pip install -r requirements.dev.txt ; \|| Shell script to install the dev requirements if DEV argument is true
#   fi && \                                               || 'if' backwards ends the if statement in the shell script

# rm -rf \tmp                                             || removes the tmp directory, need to remove everything that is extra before we create the image
# adduser                                                 || calls the adduser to create a new user inside the image (don't want to use root user)
# --disabled-password                                     || disables password
# --no-create-home                                        || dont need home directory
# django-user                                             || creates a container user called 'django-user'
RUN python -m venv /py && \
  /py/bin/pip install --upgrade pip && \
  /py/bin/pip install -r /tmp/requirements.txt && \
  if [ $DEV = "true" ]; \
    then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
  fi && \
  rm -rf /tmp && \
  adduser \
    --disabled-password \
    --no-create-home \
    django-user && \
  mkdir -p /app/cov && \
  chown -R django-user:django-user /app/cov


# Updates the PATH environment variable for python
ENV PATH="/py/bin:$PATH"

# This specifies the user that is switched to as soon as the Dockerfile finishes executing (removes root priveleges)
USER django-user