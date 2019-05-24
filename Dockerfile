FROM python:3.7
RUN mkdir logistic-bot/
COPY requirements.txt logistic-bot/
WORKDIR /logistic-bot/
RUN pip install -r requirements.txt
RUN python3 manage.py collectstatic
RUN python3 manage.py makemigrations
RUN python manage.py migrate
ADD . /logistic-bot/
