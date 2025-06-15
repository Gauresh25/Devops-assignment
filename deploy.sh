#!/bin/bash

set -e
APP_NAME="gauresh-devops-app"
BUCKET_NAME="gauresh-devops-bucket"
AWS_REGION="ap-south-1"


echo "Building Docker image..."
docker build -t $APP_NAME .

echo "Stopping existing container..."
docker stop $APP_NAME 2>/dev/null || true
docker rm $APP_NAME 2>/dev/null || true

echo "Running new container..."
docker run -d \
  --name $APP_NAME \
  -p 80:5000 \
  -e S3_BUCKET_NAME=$BUCKET_NAME \
  -e AWS_REGION=$AWS_REGION \
  --restart unless-stopped \
  $APP_NAME

echo "Checking container status..."
docker ps | grep $APP_NAME

echo "=== Deployment Complete ==="
echo "App should be available at http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)"
echo "Container logs: docker logs $APP_NAME"