#!/bin/bash

# this is for testing mutiple images
#  images to test
images=(
  "mysql:8.0-debian"
  "jupyter/scipy-notebook"
  "bitnami/spark"
  "bde2020/hadoop-datanode"
  "tomcat"
)

# output file for the results
output_file="cpu_memory_usage_results.txt"
> "$output_file"  # clear file

# calculate average
calculate_average() {
  local sum=0
  local count=$#
  for value in "$@"; do
    sum=$(echo "$sum + $value" | bc)
  done
  echo "scale=2; $sum / $count" | bc
}

# extract numeric values from CPU/MEM stats
extract_numeric_value() {
  echo "$1" | sed 's/[^0-9.]//g'
}

for image in "${images[@]}"; do
  echo "Testing image: $image" | tee -a "$output_file"
  cpu_usages=()
  memory_usages=()

  for run in {1..5}; do
    echo "Run $run for $image" | tee -a "$output_file"

    # clean up any existing containers and images to make sure this is cold startup time not warm
    sudo docker container rm -f test-container > /dev/null 2>&1
    sudo docker image rm -f "$image" > /dev/null 2>&1
    sudo docker run --name test-container -d "$image" > /dev/null 2>&1

    # allow initialization
    sleep 0.2

    # get CPU and memory usage
    stats=$(sudo docker stats --no-stream --format "{{.Name}}: CPU={{.CPUPerc}}, MEM={{.MemUsage}}" test-container)
    cpu_usage=$(extract_numeric_value "$(echo "$stats" | awk '{print $1}')")
    mem_usage=$(extract_numeric_value "$(echo "$stats" | awk '{print $2}')")
    cpu_usages+=("$cpu_usage")
    memory_usages+=("$mem_usage")

    echo "Run $run: CPU=${cpu_usage}%, MEM=${mem_usage}" | tee -a "$output_file"

    # clean up
    sudo docker container rm -f test-container > /dev/null 2>&1
    sudo docker image rm -f "$image" > /dev/null 2>&1
  done

  # averages
  avg_cpu_usage=$(calculate_average "${cpu_usages[@]}")
  avg_memory_usage=$(calculate_average "${memory_usages[@]}")

  echo "Average for $image: CPU=${avg_cpu_usage}%, Memory=${avg_memory_usage}" | tee -a "$output_file"
  echo "--------------------------------------------" | tee -a "$output_file"
done

echo "Testing complete. Results saved in $output_file."

