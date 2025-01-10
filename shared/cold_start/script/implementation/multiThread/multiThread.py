import docker
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# Initialize Docker client
client = docker.from_env()

# Fetch a specific layer of an image
def fetch_layer(image_name, layer):
    try:
        print(f"Starting fetch for layer: {layer}")
        client.images.pull(image_name, tag=layer)
        print(f"Completed fetch for layer: {layer}")
    except Exception as e:
        print(f"Error fetching layer {layer}: {e}")

# Display image layers
'''def display_image_layers(image_name):
    try:
        # Get the image details
        image = client.images.get(image_name)
        
        # Print out layer information
        print(f"\nLayers for image '{image_name}':")
        if 'rootfs' in image.attrs and 'Layers' in image.attrs['rootfs']:
            layers = image.attrs['rootfs']['Layers']
            for idx, layer in enumerate(layers):
                print(f"Layer {idx + 1}: {layer}")
        else:
            print("No layer information found.")
    except Exception as e:
        print(f"Error fetching layers for {image_name}: {e}")
'''

def display_image_layers(image_name):
    try:
        # Get the image details
        image = client.images.get(image_name)

        # Print out entire metadata
        print(f"\nMetadata for image '{image_name}':\n{image.attrs}\n")

        # Check for layer information in rootfs
        if 'RootFS' in image.attrs and 'Layers' in image.attrs['RootFS']:
            layers = image.attrs['RootFS']['Layers']
            print(f"\nLayers for image '{image_name}':")
            for idx, layer in enumerate(layers):
                print(f"Layer {idx + 1}: {layer}")
        else:
            print("No layer information found.")
    except Exception as e:
        print(f"Error fetching layers for {image_name}: {e}")

def fetch_image_without_multithreading(image_name):
    print("\nStarting single-threaded fetching...")
    start_time = time.time()

    try:
        # Pull the full image
        client.images.pull(image_name)
        print(f"Completed single-threaded fetch for image: {image_name}")
    except Exception as e:
        print(f"Error fetching image {image_name} without multi-threading: {e}")

    end_time = time.time()
    print(f"Total time taken for single-threaded fetching: {end_time - start_time:.2f} seconds\n")

# Multi-threaded layer fetching
def fetch_image_layers_multithreaded(image_name):
    display_image_layers(image_name)  # Display layers before fetching
    
    layers = ["latest"] 
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=len(layers)) as executor:
        futures = [executor.submit(fetch_layer, image_name, layer) for layer in layers]
        
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Error in thread execution: {e}")

    end_time = time.time()
    print(f"\nTotal time taken for multi-threaded fetching: {end_time - start_time:.2f} seconds")

# Image to fetch
image_name = "mysql:latest" 

# Display layers and run the multi-threaded fetching
display_image_layers(image_name)
fetch_image_without_multithreading(image_name)
fetch_image_layers_multithreaded(image_name)
