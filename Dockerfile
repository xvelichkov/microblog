FROM python:3

WORKDIR /app
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . ./

EXPOSE 8000

ARG CACHEBUST=1
RUN python manage.py collectstatic

CMD python manage.py collectstatic && python manage.py migrate && python manage.py runserver 0.0.0.0:8000