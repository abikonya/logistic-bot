FROM python:3.7
RUN mkdir logistic-bot/
COPY requirements.txt logistic-bot/
WORKDIR /logistic-bot/
RUN pip install -r requirements.txt
ADD . /logistic-bot/
