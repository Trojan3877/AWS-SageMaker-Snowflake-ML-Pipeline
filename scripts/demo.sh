#!/usr/bin/env bash
# scripts/demo.sh
# ----------------
# Builds the Docker image, runs the container, and smoke-tests the /predict endpoint.

set -euo pipefail

IMAGE_NAME="fraud-pipeline"
CONTAINER_NAME="fraud-pipeline-demo"
PORT=8080

echo "==> Building Docker image: ${IMAGE_NAME}"
docker build -t "${IMAGE_NAME}" .

echo "==> Starting container on port ${PORT}"
docker run -d \
  --name "${CONTAINER_NAME}" \
  -p "${PORT}:${PORT}" \
  -e AWS_REGION="${AWS_REGION:-us-east-1}" \
  -e SAGEMAKER_ENDPOINT_NAME="${SAGEMAKER_ENDPOINT_NAME:-fraud-endpoint}" \
  "${IMAGE_NAME}"

echo "==> Waiting for container to be ready..."
sleep 3

echo "==> Sending test prediction request"
curl -s -X POST "http://localhost:${PORT}/predict" \
  -H "Content-Type: application/json" \
  -d @examples/sample_transaction.json | python3 -m json.tool

echo "==> Stopping and removing container"
docker stop "${CONTAINER_NAME}"
docker rm "${CONTAINER_NAME}"

echo "==> Demo complete."
