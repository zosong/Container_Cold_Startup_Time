#!/bin/bash

# run in detached mode
time sudo docker run --name jupyter-test -d jupyter/scipy-notebook

# wait the container until running state
while [ "$(sudo docker inspect -f '{{.State.Running}}' jupyter-test)" != "true" ]; do
  sleep 0.1 
done

# get CPU and memory usage
sudo docker stats --no-stream --format "{{.Name}}: CPU={{.CPUPerc}}, MEM={{.MemUsage}}" > stat.log

# show the recorded stats
sudo cat stat.log
