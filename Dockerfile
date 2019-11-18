FROM tiangolo/uwsgi-nginx:python3.7

LABEL maintainer="Elias Kassell <eliaskassell@gmail.com>"

COPY requirements.txt ./
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY ./app /app
