# Set base image (host OS)
FROM python:3.9.7


# Add flask app and dependencies to Dockerfile5
ADD app.py /
ADD requirements.txt /


ENV TZ = "Australia/NSW"

ADD this_folder /

# Install any dependencies
RUN pip install -r /requirements.txt 
RUN pip install awscli


# By default, listen on port 5000
EXPOSE 5000


# Copy the dependencies file to the working directory
COPY . .

# Specify app environment
ENV FLASK_APP=app.py

RUN chmod + x gunicorn_starter.sh

ENTRYPOINT ["./gunicorn_starter.sh"]

