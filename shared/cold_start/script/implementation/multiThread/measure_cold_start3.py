import docker
import subprocess
import time

# Initialize Docker client
client = docker.from_env()

# Pull image and run container with timing
def measure_cold_start(image_name, container_name, timeout=120, check_interval=2):

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
        #remove=True  # Automatically remove the container after it stops
    )

    # Intermittently checks
    print("Waiting for MySQL to complete initialization...")
    try:
        start_log_time = time.time()
        while True:
            # Check the most recent log output 
            logs = container.logs(tail=10).decode('utf-8')
            if "ready for connections" in logs:
                print("MySQL is ready.")
                break
            
            # Check for timeout
            if time.time() - start_log_time > timeout:
                raise TimeoutError("MySQL container initialization timed out.")
            
            # Wait before checking again
            time.sleep(check_interval)

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
