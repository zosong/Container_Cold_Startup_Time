#!/bin/bash

# Display all Docker containers
echo "Listing all containers..."
sudo docker ps -a

# Stop all running containers
echo "Stopping all containers..."
sudo docker stop $(sudo docker ps -aq)

# Remove all containers
echo "Removing all containers..."
sudo docker rm $(sudo docker ps -aq)

# Force remove all images
echo "Removing all images..."
sudo docker rmi -f $(sudo docker images -q)

# Remove all unused data, including volumes
echo "Pruning system, including volumes..."
sudo docker system prune -a --volumes -f

echo "Docker cleanup complete!"

