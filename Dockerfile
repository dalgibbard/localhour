FROM ubuntu:14.04
MAINTAINER Darren Gibbard (dalgibbard@gmail.com)
RUN apt-get update && apt-get upgrade -y
RUN apt-get install python python-dev python-distribute python-pip git
RUN git clone https://github.com/dalgibbard/localhour /localhour
RUN pip install -r /localhour/requirements.txt
EXPOSE 80
WORKDIR /localhour
CMD gunicorn --workers 4 --bind 0.0.0.0:80 localhour
