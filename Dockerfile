FROM python:3.10-alpine
ENV PYTHONUNBUFFERED 1
WORKDIR /opt/app
COPY . .

RUN pip install --upgrade pip \
  && apk add --no-cache gcc musl-dev libpq libpq-dev linux-headers \
  && pip install --no-cache-dir -r requirements.txt \
  && rm requirements.txt \
  && apk del --purge gcc musl-dev libpq-dev linux-headers apk-tools\
  && python manage.py collectstatic --no-input

CMD python manage.py migrate \
  && (python manage.py createsuperuser --no-input || :) \
  && uwsgi uwsgi.ini
