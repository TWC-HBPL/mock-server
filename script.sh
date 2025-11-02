#!/bin/bash

set -e

ECR_REPO="835126668815.dkr.ecr.ap-south-1.amazonaws.com/ecr-testing-api"
# ECR_REPO="zubair05/mockserver"
DEPLOYMENT_FILE="kubernetes/mock-server-deployment.yaml"

# Generate a unique tag using timestamp
TAG="mocker_server$(date +%Y%m%d%H%M%S)"

# Build and push the Docker image
docker buildx build --platform linux/amd64 -t $ECR_REPO:$TAG .
docker push $ECR_REPO:$TAG

# Deploy to Kubernetes, replacing the placeholder with the actual tag
# sed "s/__IMAGE_TAG__/$TAG/g" $DEPLOYMENT_FILE | kubectl apply -f -

echo "Deployment applied with image tag: $TAG"