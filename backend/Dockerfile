FROM ubuntu

RUN apt-get update && apt-get install -y python3-pip
RUN pip3 install PyMySQL

WORKDIR app
COPY requirements.txt requirements.txt

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

CMD python3 main.py