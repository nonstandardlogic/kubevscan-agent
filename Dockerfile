FROM python:3.8-slim-buster

RUN apt update
RUN apt-get install cron -y
RUN apt install curl -y 
RUN curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/master/contrib/install.sh | sh -s -- -b /usr/local/bin

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN mkdir -p /app
WORKDIR /app
COPY ./script.py /app

COPY ./entrypoint.sh /
ENTRYPOINT ["/entrypoint.sh"]
CMD ["script.py"]
