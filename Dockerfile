FROM python:3.7-stretch

COPY requirements.txt /tmp/requirements.txt
RUN pip install uwsgi
RUN pip install -r /tmp/requirements.txt
COPY . /app
CMD uwsgi --chdir /app --http 0.0.0.0:3000 --wsgi-file /app/hbcbot/app.py
