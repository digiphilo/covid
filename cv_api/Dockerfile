FROM ubuntu:16.04
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV PORT 5000
RUN apt-get update -y && apt-get install -y python3-pip python3-dev curl
COPY app.py /app/app.py
COPY start.sh /app/start.sh
COPY templates /app/templates
WORKDIR /app
RUN pip3 install flask us
CMD ./start.sh
