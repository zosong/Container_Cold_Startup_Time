import time
import docker
import csv

client = docker.from_env()
images = ["mysql:latest", "mysql:8.0-oracle", "mysql:8.0-debian", "postgres:latest", "postgres:alpine"]

for image in images:
    metrics = []
    
    #measure time
    start_time = time.time()
    container = client.containers.run(image, detach=True)

    while True:
        container.reload()
        stats = container.stats(stream=False)
        cpu_usage = stats['cpu_stats']['cpu_usage']['total_usage']
        memory_usage = stats.get('memory_stats', {}).get('usage', None)
        elapsed_time = time.time() - start_time
        metrics.append([elapsed_time, cpu_usage, memory_usage])

        #make sure that containers is ready before measurement
        if container.status == 'running':
            break
        time.sleep(0.5)  # in case the time is too short to be recor


    end_time = time.time()
    cold_start_time = end_time - start_time
    print(f"Cold Start Time for {image}:", cold_start_time, "seconds")

    # for each image, record to CSV file for later check
    file_name = f"{image.replace(':', '_')}_cold_start_metrics.csv"
    with open(file_name, mode='w') as file:
        writer = csv.writer(file)
        writer.writerow(["Time (s)", "CPU Usage", "Memory Usage"])
        writer.writerows(metrics)
