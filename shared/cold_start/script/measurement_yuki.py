import time
import docker
import json
from threading import Event

client = docker.from_env()

def getContainers():
    # returns a list of running containers
    return client.containers.list()

def dockerLog(images, testType, dataframeN, cardinality, duration=10):

    for image in images:
    
        container = client.containers.run(image, detach=True)
        cpuLog = []
        memLog = []
        startFlag = True
        startEpoch = int(time.time() * 1000)  
        print(f"Started logging for {image}...")
        
        start_time = time.time()
        while time.time() - start_time < duration:
            try:
                status = container.stats(decode=None, stream=False)
                try:
                    # calculate the change for CPU usage of the container between readings
                    cpuDelta = status["cpu_stats"]["cpu_usage"]["total_usage"] - status["precpu_stats"]["cpu_usage"]["total_usage"]
                    systemDelta = status["cpu_stats"].get("system_cpu_usage", 1) - status["precpu_stats"].get("system_cpu_usage", 1)
                    
                    if systemDelta > 0:
                        cpuPercent = (cpuDelta / systemDelta) * (status["cpu_stats"].get("online_cpus", 1)) * 100
                    else:
                        cpuPercent = 0
                    
                    cpuPercent = int(cpuPercent)

                    # fetch memory consumption for the container
                    mem = status["memory_stats"].get("usage", 0)
                    mem = int(mem / 1000000)  # Convert to MB

                    # avoid logging CPU increase 
                    if startFlag and cpuPercent == 0:
                        startFlag = False
                        startEpoch = int(time.time() * 1000)
                        print("Startflag set to False - actual logging started.")
                    if not startFlag:
                        cpuLog.append(cpuPercent)
                        memLog.append(mem)
                except Exception as e:
                    print(f"Error in logging stats for {image}: {e}")
                    break
            except Exception as e:
                print(f"Error fetching container stats: {e}")
                break
            time.sleep(1)

        
        endEpoch = int(time.time() * 1000)
        file_name = f"output/{dataframeN}_{cardinality}_{testType}_{image.replace(':', '_')}_stats.json"
        with open(file_name, "w") as f:
            json.dump({"mem": memLog, "cpu": cpuLog, "timeSpent": float((endEpoch - startEpoch) / 1000)}, f)
        print(f"Logging for {image} completed. Data saved to {file_name}")
        
        # Stop and remove the container
        container.stop()
        container.remove()
    print("################################################### dockerLog ended for all images")


images = ["mysql:latest", "mysql:8.0-oracle", "postgres:latest"]
dockerLog(images, testType="cold_start", dataframeN="df1", cardinality="low", duration=10)

