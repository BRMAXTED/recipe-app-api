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

    #Install the python virtual environment
RUN python -m venv /py && \
    # upgrade PIP
    /py/bin/pip install --upgrade pip && \
    # APK stands for Alpine Linux package keeper (manager)
    # install the postgresql-client linus package
    apk add --update --no-cache postgresql-client && \
    # Creates a virtual build environment 'dependency package'
    # We can remove this later in the RUN command
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    # installs the list of pip requirments inside the virtual environment
    /py/bin/pip install -r /tmp/requirements.txt && \
    # Shell script to install the dev requirements if DEV argument is true
    if [ $DEV = "true" ]; \
    then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    # removes the tmp directory, need to remove everything that is extra before we create the image
    rm -rf /tmp && \
    # Remove the temporary dependency environment
    apk del .tmp-build-deps && \
    # Adds a new user django-user. We do not want to use the root user
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

# Updates the PATH environment variable for python
ENV PATH="/py/bin:$PATH"

# This specifies the user that is switched to as soon as the Dockerfile finishes executing (removes root priveleges)
USER django-user