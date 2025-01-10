import docker
import time

# Initialize Docker client
client = docker.from_env()

# Measure cold start time without pulling or cleaning up the image
def measure_cold_start(image_name, container_name):
    # Start measuring time
    start_time = time.time()
    
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

