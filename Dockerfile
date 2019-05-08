FROM python:3.7-alpine

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD sh -c "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"
