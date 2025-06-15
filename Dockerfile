FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

ENV FLASK_APP=app.py
ENV S3_BUCKET_NAME=gauresh-assignment
ENV AWS_REGION=ap-south-1

CMD ["python", "app.py"]