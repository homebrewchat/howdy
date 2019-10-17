FROM amazeeio/python:3.7-latest

RUN apk add --no-cache gcc libc-dev linux-headers

COPY requirements.txt /tmp/requirements.txt

RUN pip install uwsgi
RUN pip install -r /tmp/requirements.txt

COPY . /app

CMD uwsgi \
    --chdir /app \
    --http 0.0.0.0:8800 \
    --wsgi-file /app/hbcbot/app.py \
    --callable app \
    --processes 4
