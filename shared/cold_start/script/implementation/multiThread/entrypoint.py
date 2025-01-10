import threading
import subprocess
import time

# Measure the initialization start time
start_time = time.time()

# Define initialization tasks
def load_config():
    print("Loading configuration...")
    subprocess.run(["cat", "/etc/myapp/config"])
    print("Configuration loaded.")

def initialize_db():
    print("Initializing database...")
    subprocess.run(["mysql", "-u", "root", "-e", "CREATE DATABASE IF NOT EXISTS mydb;"])
    print("Database initialized.")

def setup_cache():
    print("Setting up cache...")
    subprocess.run(["redis-cli", "SET", "cache_key", "initial_value"])
    print("Cache setup complete.")

# Multi-threaded initialization
def multi_threaded_startup():
    print("Starting multi-threaded container initialization...")

    # Create and start threads
    config_thread = threading.Thread(target=load_config)
    db_thread = threading.Thread(target=initialize_db)
    cache_thread = threading.Thread(target=setup_cache)

    config_thread.start()
    db_thread.start()
    cache_thread.start()

    config_thread.join()
    db_thread.join()
    cache_thread.join()

    print("Multi-threaded initialization complete.")

if __name__ == "__main__":
    multi_threaded_startup()
    # Measure and print the initialization time
    end_time = time.time()
    print(f"Initialization time inside container: {end_time - start_time:.2f} seconds")
    
    # Start the main MySQL
    subprocess.run(["mysqld"])

