#!/bin/bash

echo "Listing all containers..."
sudo docker ps -a

echo "Stopping all containers..."
sudo docker stop $(sudo docker ps -aq)
echo "Removing all containers..."
sudo docker rm $(sudo docker ps -aq)

echo "Removing all images..."
sudo docker rmi -f $(sudo docker images -q)

echo "Pruning system, including volumes..."
sudo docker system prune -a --volumes -f

echo "Docker cleanup complete!"

