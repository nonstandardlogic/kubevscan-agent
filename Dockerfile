FROM python:3.9.0-alpine

RUN mkdir -p /app
WORKDIR /app

# COPY requirements.txt requirements.txt
# RUN pip install -r requirements.txt

COPY . .

COPY ./entrypoint.sh /
ENTRYPOINT ["/entrypoint.sh"]
CMD ["script.py"]