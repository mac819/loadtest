FROM python:3.9-rc-buster

# Setting up docker environment
WORKDIR /code
# Export environment variables
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0
###

COPY requirements.txt requirements.txt

#Run and install all required modules in container
RUN pip3 install -r requirements.txt

#Copy current directory files to containers code directory
COPY . .

#RUN app.
CMD ["flask", "run"]