FROM ubuntu:16.04
RUN apt-get update -y && apt-get install -y python-pip python-dev curl
COPY app.py /app/app.py
COPY start.sh /app/start.sh
COPY templates /app/templates
WORKDIR /app
RUN pip install flask
CMD ./start.sh
