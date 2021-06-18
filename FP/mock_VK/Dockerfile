FROM ubuntu:latest
MAINTAINER Malakhov Ilya 'froztgal@gmail.com'
RUN apt-get update -y
RUN apt-get install -y python3-pip python-dev build-essential
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
# ENTRYPOINT ['python']
CMD ["python3", "./mock_vk.py"]