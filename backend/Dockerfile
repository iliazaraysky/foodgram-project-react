FROM python:3.8.5
RUN mkdir /code
COPY . /code
WORKDIR /code
RUN pip install --upgrade pip && pip install -r /code/requirements.txt
CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000
