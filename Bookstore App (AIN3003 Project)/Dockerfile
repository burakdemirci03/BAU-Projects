FROM python:3.9-slim-buster

WORKDIR /bookstore_app_p2

COPY requirements.txt /bookstore_app_p2/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /bookstore_app_p2/

ENV FLASK_APP=app.py

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]