FROM python:latest

LABEL Maintainer="wDANDANw"

COPY requirements.txt /usr/app/src/requirements.txt
WORKDIR /usr/app/src
RUN pip3 install -r requirements.txt

COPY ./ ./

CMD [ "python", "-u", "./webhook_server_discord.py"]