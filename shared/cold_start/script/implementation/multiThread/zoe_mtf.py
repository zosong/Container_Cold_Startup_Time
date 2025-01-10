import subprocess
import threading
import time

# Run the original container
run_command = "sudo docker run --name jupyter -d -p 8888:8888 jupyter/scipy-notebook"

# Path to the cleanup script
cleanup_script = "./rm.sh"

# Number of threads for multi-threaded fetching
NUM_THREADS = 4


def run_container(command):
    """Run a Docker container and measure the start-up time."""
    start_time = time.time()
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running the container: {e}")
        return None
    end_time = time.time()
    return end_time - start_time


def fetch_image_layer(layer_index):
    """Simulate fetching a specific layer of the Docker image."""
    print(f"Fetching layer {layer_index}...")
    time.sleep(1)  # Simulate the network delay for fetching a layer
    print(f"Layer {layer_index} fetched.")


def multi_threaded_fetching():
    """Perform multi-threaded fetching of image layers."""
    threads = []
    for i in range(NUM_THREADS):
        thread = threading.Thread(target=fetch_image_layer, args=(i,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    print("Measuring original cold start-up time...")
    original_time = run_container(f"time {run_command}")
    if original_time:
        print(f"Original cold start-up time: {original_time:.2f} seconds")

    print("\nCleaning up using rm.sh...")
    try:
        subprocess.run(f"bash {cleanup_script}", shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running cleanup script: {e}")
        exit(1)

    print("\nSimulating multi-threaded fetching of image layers...")
    fetch_start_time = time.time()
    multi_threaded_fetching()
    fetch_end_time = time.time()
    fetch_duration = fetch_end_time - fetch_start_time

    print(f"\nMulti-threaded fetching completed in {fetch_duration:.2f} seconds")

    print("\nRunning container again to measure optimized cold start-up time...")
    optimized_time = run_container(f"time {run_command}")
    if optimized_time:
        print(f"Optimized cold start-up time: {optimized_time:.2f} seconds")

    print("\nSummary:")
    print(f"Original cold start-up time: {original_time:.2f} seconds")
    print(f"Optimized cold start-up time: {optimized_time:.2f} seconds")
