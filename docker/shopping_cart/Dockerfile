FROM --platform=linux/amd64 python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

EXPOSE 4005

CMD ["python", "run_waitress.py"]