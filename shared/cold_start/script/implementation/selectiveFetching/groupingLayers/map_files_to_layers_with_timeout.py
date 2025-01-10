import subprocess
import os

NON_CRITICAL_FILES = "non_critical_files.txt"
DOCKER_IMAGE = "jupyter/scipy-notebook"
OUTPUT_FILE = "non_critical_files_to_layers.txt"
TIMEOUT = 300  # timeout for each file-layer check (in seconds)

def get_layers(image_name):
    """
    Retrieve all layer digests for a Docker image.
    """
    layers = []
    try:
        result = subprocess.run(
            ["docker", "inspect", image_name],
            capture_output=True, text=True, check=True
        )
        data = result.stdout
        for line in data.split("\n"):
            if "sha256:" in line:
                layer = line.strip().strip('"').strip(',')
                layers.append(layer)
    except subprocess.CalledProcessError as e:
        print(f"Error retrieving layers for {image_name}: {e}")
    return layers

def check_file_in_layer(file_path, image_name, layer_digest):
    """
    Check if a file exists in a specific layer with timeout enforcement.
    """
    try:
        result = subprocess.run(
            [
                "docker", "run", "--rm",
                "--entrypoint=/bin/bash",
                f"{image_name}@{layer_digest}",
                "-c", f"test -f {file_path} && echo FOUND || echo NOT_FOUND"
            ],
            capture_output=True, text=True, timeout=TIMEOUT
        )
        if "FOUND" in result.stdout:
            return True
    except subprocess.TimeoutExpired:
        print(f"Timeout while checking {file_path} in layer {layer_digest}")
    except subprocess.CalledProcessError:
        pass
    return False

def map_files_to_layers(non_critical_files, layers, image_name, existing_mapping):
    """
    Map each non-critical file to the layer it was introduced in.
    """
    mapping = existing_mapping.copy()
    with open(OUTPUT_FILE, "a") as f:  
        for file_path in non_critical_files:
            if file_path in mapping:  # skip if it is already processed files
                continue
            for layer in layers:
                print(f"Checking {file_path} in layer {layer}...")
                if check_file_in_layer(file_path, image_name, layer):
                    print("---------IN IF----------")
                    mapping[file_path] = layer
                    f.write(f"{file_path} -> {layer}\n")
                    f.flush()  # written to disk immediately
                    break  # once the layer is found,break to stop
    return mapping

def load_existing_mapping(output_file):
    """
    Load existing mapping from the output file.
    """
    mapping = {}
    if os.path.exists(output_file):
        with open(output_file, "r") as f:
            for line in f:
                try:
                    file_path, layer = line.strip().split(" -> ")
                    mapping[file_path] = layer
                except ValueError:
                    pass
    return mapping

def main():
    # load non-critical files
    try:
        with open(NON_CRITICAL_FILES, "r") as f:
            non_critical_files = [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        print(f"Error: {NON_CRITICAL_FILES} not found.")
        return

    existing_mapping = load_existing_mapping(OUTPUT_FILE)

    layers = get_layers(DOCKER_IMAGE)
    if not layers:
        print("Error: No layers found in the image.")
        return

    #map non-critical files to their layers
    mapping = map_files_to_layers(non_critical_files, layers, DOCKER_IMAGE, existing_mapping)

    print(f"Mapping complete. Results saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()

