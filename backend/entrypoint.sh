#!/usr/bin/env bash

RUN pip install -r requirements.txt
apt-get clean

exec "$@"