FROM python:3.10
ENV PYTHONUNBUFFERED 1
ENV PYTHONIOENCODING "UTF-8"

WORKDIR /code
COPY requirements.txt /code
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /code/
