import subprocess

NON_CRITICAL_FILES = "non_critical_files.txt"
DOCKER_IMAGE = "jupyter/scipy-notebook"
OUTPUT_FILE = "non_critical_files_to_layers.txt"

def get_layers(image_name):
    """
    Retrieve all layer digests for a Docker image.
    """
    layers = []
    result = subprocess.run(
        ["docker", "inspect", image_name],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        data = result.stdout
        for line in data.split("\n"):
            if "sha256:" in line:
                layer = line.strip().strip('"').strip(',')
                layers.append(layer)
    return layers

def check_file_in_layer(file_path, image_name, layer_digest):
    """
    Check if a file exists in a specific layer.
    """
    try:
        result = subprocess.run(
            [
                "docker", "run", "--rm",
                "--entrypoint=/bin/bash",
                f"{image_name}@{layer_digest}",
                "-c", f"test -f {file_path} && echo FOUND || echo NOT_FOUND"
            ],
            capture_output=True, text=True
        )
        if "FOUND" in result.stdout:
            return True
    except subprocess.CalledProcessError:
        pass
    return False

def map_files_to_layers(non_critical_files, layers, image_name):
    """
    Map each non-critical file to the layer it was introduced in.
    """
    mapping = {}
    for file_path in non_critical_files:
        for layer in layers:
            if check_file_in_layer(file_path, image_name, layer):
                mapping[file_path] = layer
                break
    return mapping

def main():
    with open(NON_CRITICAL_FILES, "r") as f:
        non_critical_files = [line.strip() for line in f.readlines()]

    layers = get_layers(DOCKER_IMAGE)

    mapping = map_files_to_layers(non_critical_files, layers, DOCKER_IMAGE)

    with open(OUTPUT_FILE, "w") as f:
        for file, layer in mapping.items():
            f.write(f"{file} -> {layer}\n")

    print(f"Mapping complete. Results saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
