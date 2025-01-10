import threading
import time
import os

# Define directory paths
CONFIG_DIR = "/container_fs/config"
DATA_DIR = "/container_fs/data"
BIN_DIR = "/container_fs/bin"

# File setup tasks

def setup_config_files():
    print("Setting up configuration files...")
    time.sleep(1)  # Wait for setting up config files
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(os.path.join(CONFIG_DIR, "app.conf"), "w") as f:
        f.write("config_key=config_value\n")
    print("Configuration files setup completed.")

def setup_data_files():
    print("Setting up data files...")
    time.sleep(1.5)  # Wait for setting up data files
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(os.path.join(DATA_DIR, "data.db"), "w") as f:
        f.write("sample_data=12345\n")
    print("Data files setup completed.")

def setup_binary_files():
    print("Setting up binary files...")
    time.sleep(2)  # Wait for setting up binaries
    os.makedirs(BIN_DIR, exist_ok=True)
    with open(os.path.join(BIN_DIR, "app_binary"), "w") as f:
        f.write("#!/bin/bash\necho 'Hello, world!'\n")
    print("Binary files setup completed.")

# Non-optimized file system setup
def setup_file_system_sequential():
    print("\nStarting sequential file system setup...")
    start_time = time.time()
    
    setup_config_files()
    setup_data_files()
    setup_binary_files()
    
    end_time = time.time()
    print(f"Total file system setup time (sequential): {end_time - start_time:.2f} seconds\n")

# Multi-threaded file system setup
def setup_file_system_multithreaded():
    print("\nStarting multi-threaded file system setup...")
    start_time = time.time()

    # Create threads for each setup task
    config_thread = threading.Thread(target=setup_config_files)
    data_thread = threading.Thread(target=setup_data_files)
    binary_thread = threading.Thread(target=setup_binary_files)

    # Start threads
    config_thread.start()
    data_thread.start()
    binary_thread.start()

    # Wait for all threads to complete
    config_thread.join()
    data_thread.join()
    binary_thread.join()

    end_time = time.time()
    print(f"Total file system setup time (multi-threaded): {end_time - start_time:.2f} seconds\n")

setup_file_system_sequential()
setup_file_system_multithreaded()

