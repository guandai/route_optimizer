#!/bin/bash

# Set variables
DOCKER_USERNAME="guandai"
IMAGE_NAME="image-processing"
CONTAINER_NAME="image-color"

# Step 1: Update the app.py (skip this if already done manually)
# For example, let's say you're editing it with nano
# nano app.py  # Uncomment this if you want to open it for editing within the script

# Step 2: Build the Docker image
docker build -t $DOCKER_USERNAME/$IMAGE_NAME .

# Step 3: Push the image to Docker Hub
docker push $DOCKER_USERNAME/$IMAGE_NAME

# Step 4: Stop the previous running container
docker stop $CONTAINER_NAME

# Step 5: Remove the old container (optional but recommended)
docker rm $CONTAINER_NAME

# Step 6: Run a new container with the updated image
docker run -d --name $CONTAINER_NAME -p 5020:5020 $DOCKER_USERNAME/$IMAGE_NAME

echo "Deployment complete. The new container is running."
