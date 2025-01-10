import time
import docker
import csv

# Zoe's attempt for measure memory and CPU usage
client = docker.from_env()
images = ["mysql:latest", "mysql:8.0-oracle", "mysql:8.0-debian", "postgres:latest", "postgres:alpine"]

for image in images:
    metrics = []
    
    start_time = time.time()
    container = client.containers.run(image, detach=True)

    time.sleep(1)

    while True:
        try:
            container.reload()
            stats = container.stats(stream=False)
            cpu_usage = stats['cpu_stats']['cpu_usage']['total_usage']
            memory_usage = stats.get('memory_stats', {}).get('usage', None)

            if cpu_usage is not None and memory_usage is not None:
                elapsed_time = time.time() - start_time
                metrics.append([elapsed_time, cpu_usage, memory_usage])

            if container.status == 'running':
                break
        except KeyError:
        # if stats are not yet available
            pass
        time.sleep(0.5)  
    
    end_time = time.time()
    cold_start_time = end_time - start_time
    print(f"Cold Start Time for {image}:", cold_start_time, "seconds")

    file_name = f"{image.replace(':', '_')}_zo.csv"
    with open(file_name, mode='w') as file:
        writer = csv.writer(file)
        writer.writerow(["Time (s)", "CPU Usage", "Memory Usage"])
        writer.writerows(metrics)
    
