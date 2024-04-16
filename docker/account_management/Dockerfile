# For the shopping cart service
FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 4000

CMD ["flask", "run", "--host=0.0.0.0", "--port=4000"]