FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 4000

CMD ["waitress-serve", "--port=4000", "app:create_app"]