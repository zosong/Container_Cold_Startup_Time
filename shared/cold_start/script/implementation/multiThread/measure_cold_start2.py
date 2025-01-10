import docker
import subprocess
import time

# Initialize Docker client
client = docker.from_env()

# Remove all Docker data
def clean_docker():
    print("Cleaning Docker environment...")
    client.containers.prune()
    client.images.prune(filters={'dangling': True})
    subprocess.run(["sudo", "docker", "system", "prune", "-a", "--volumes", "-f"])
    print("Docker environment cleaned.")

# Pull image and run container with timing
def measure_cold_start(image_name, container_name, timeout=120):
    clean_docker()  # Ensure no cache for a true cold start

    # Start measuring time
    start_time = time.time()
    
    # Pull the image
    print(f"Pulling image {image_name}...")
    client.images.pull(image_name)
    
    # Multi-threaded initialization
    print(f"Running container {container_name}...")
    container = client.containers.run(
        image_name,
        name=container_name,
        environment={"MYSQL_ROOT_PASSWORD": "my-secret-pw"},
        detach=True,
        remove=True  # Automatically remove the container after it stops
    )

    # Logs to detect when MySQL finishes its initialization
    print("Waiting for MySQL to complete initialization...")
    try:
        # Check logs until ready or timeout
        start_log_time = time.time()
        for line in container.logs(stream=True):
            
            print(line.strip().decode('utf-8'))  # Print log output for debugging
            if "ready for connections" in line.decode('utf-8'):
                print("MySQL is ready.")
                break
            # Timeout condition
            if time.time() - start_log_time > timeout:
                raise TimeoutError("MySQL container initialization timed out.")

    except TimeoutError as e:
        print(f"Error: {e}")
        container.stop()
    finally:
        # Measure total cold start time
        end_time = time.time()
        total_time = end_time - start_time
        print(f"Total cold start time: {total_time:.2f} seconds")

# Image and container name
image_name = "mysql:latest"
container_name = "cold_start_test"

# Measure the cold start time
measure_cold_start(image_name, container_name)

