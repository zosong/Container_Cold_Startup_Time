import docker
import subprocess
import time

# Initialize Docker client
client = docker.from_env()

# Remove all Docker data for a fresh start
def clean_docker():
    print("Cleaning Docker environment...")
    client.containers.prune()
    client.images.prune(filters={'dangling': True})
    subprocess.run(["sudo", "docker", "system", "prune", "-a", "--volumes", "-f"])
    print("Docker environment cleaned.")

# Measure cold start time
def measure_cold_start(image_name, container_name):
    clean_docker()  # Remove all cache

    # Start measuring time
    start_time = time.time()
    
    # Pull the image
    print(f"Pulling image {image_name}...")
    client.images.pull(image_name)
    
    # Run the container
    print(f"Running container {container_name}...")
    container = client.containers.run(
        image_name,
        name=container_name,
        environment={"MYSQL_ROOT_PASSWORD": "my-secret-pw"},
        detach=True,
        remove=True  # Automatically remove the container after it stops
    )

    # Wait for the container to finish its initialization
    container.wait()
    
    # Measure total cold start time
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Total cold start time: {total_time:.2f} seconds")

# Image and container name
image_name = "mysql-custom:8.0-debian"  
container_name = "cold_start_test"

# Measure the cold start time with multi-threaded initialization
print("\nMeasuring cold start time with multi-threaded setup...")
measure_cold_start(image_name, container_name)

