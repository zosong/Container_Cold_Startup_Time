#!/bin/bash

# Define the images to test
images=(
  "mysql:8.0-debian"
  "jupyter/scipy-notebook"
  "bitnami/spark"
  "bde2020/hadoop-datanode"
  "tomcat"
)

# all resultd in output file
output_file="expr/cold_startup_times.txt"
> "$output_file"  # clear`

# calculate average
calculate_average() {
  local sum=0
  local count=$#
  for time in "$@"; do
    sum=$(echo "$sum + $time" | bc)
  done
  echo "scale=2; $sum / $count" | bc
}

for image in "${images[@]}"; do
  echo "Testing image: $image" | tee -a "$output_file"
  times=()  # using array to store times for the current image
  
  for i in {1..5}; do
    echo "Run $i for $image" | tee -a "$output_file"

    #clean up to make sure it is cold start up time
    sudo docker container rm -f tc > /dev/null 2>&1
    sudo docker image rm -f "$image" > /dev/null 2>&1

    #time for pulling and running the image
    start_time=$(date +%s.%N)
    sudo docker run --name tc -d -p 8888:8888 "$image" > /dev/null 2>&1
    end_time=$(date +%s.%N)

    elapsed=$(echo "$end_time - $start_time" | bc)
    times+=("$elapsed")
    echo "Run $i: $elapsed seconds" | tee -a "$output_file"

    # clean up again
    sudo docker container rm -f tc > /dev/null 2>&1
    sudo docker image rm -f "$image" > /dev/null 2>&1
  done

  # average time
  avg_time=$(calculate_average "${times[@]}")
  echo "Average time for $image: $avg_time seconds" | tee -a "$output_file"
  echo "--------------------------------------------" | tee -a "$output_file"
done

echo "Testing complete. Results saved in $output_file."

