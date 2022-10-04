FROM python:3.10-slim-buster
WORKDIR /bot
COPY requirements.txt /bot/
RUN pip3 install -r requirements.txt
COPY . /bot
CMD python3.10 -u botcmds.py