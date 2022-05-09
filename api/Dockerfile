FROM python:alpine

WORKDIR /app

EXPOSE 5000

COPY . .

RUN pip install -r requirements.txt

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]