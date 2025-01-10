import docker
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# initialize Docker client
client = docker.from_env()

#image name
IMAGE_NAME = "mysql:latest" 

# define layers based on importance,this is one example
CRITICAL_LAYERS = ["layer1", "layer2"]  #layer IDs critical for startup
NON_CRITICAL_LAYERS = ["layer3", "layer4"]  #layer IDs non-critical

# pull Docker image layer
def pull_layer(layer_id):
    try:
        # simulate layer pull
        print(f"Pulling layer {layer_id}...")
        layer = client.images.pull(f"{IMAGE_NAME}@{layer_id}")  # debug
        print(f"Layer {layer_id} pulled successfully.")
        return layer_id, True
    except Exception as e:
        print(f"Error pulling layer {layer_id}: {e}")
        return layer_id, False

# asynchronously pull non-critical layers, need to be updated later, this seems not works
def async_load_non_critical_layers(non_critical_layers):
    results = {}
    with ThreadPoolExecutor() as executor:
        future_to_layer = {executor.submit(pull_layer, layer): layer for layer in non_critical_layers}
        for future in as_completed(future_to_layer):
            layer = future_to_layer[future]
            success = future.result()[1]
            results[layer] = success
    return results

# pull critical and non-critical layers
def selective_layer_fetching():
    start_time = time.time()
    
    # pull critical layers syncly
    print("Starting critical layers fetch...")
    for layer_id in CRITICAL_LAYERS:
        pull_layer(layer_id)
    
    # pull non-critical layers asyncly
    print("Starting non-critical layers fetch asynchronously...")
    non_critical_results = async_load_non_critical_layers(NON_CRITICAL_LAYERS)
    
    print("Non-critical layers fetch completed:")
    for layer, success in non_critical_results.items():
        status = "Success" if success else "Failed"
        print(f"Layer {layer}: {status}")
    
    end_time = time.time()
    print(f"Selective layer fetching completed in {end_time - start_time:.2f} seconds.")


if __name__ == "__main__":
    selective_layer_fetching()

