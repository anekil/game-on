FROM ubuntu

RUN apt-get update && apt-get install -y python3-pip

WORKDIR app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt && apt-get clean

CMD python3 main.py