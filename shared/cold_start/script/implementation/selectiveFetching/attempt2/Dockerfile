FROM bitnami/spark:latest
USER root

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN adduser --disabled-password --gecos "" sparkuser

WORKDIR /home/sparkuser

COPY datasets /home/sparkuser/datasets

RUN chown -R sparkuser:sparkuser /home/sparkuser/datasets

USER sparkuser

EXPOSE 7077 8080 4040

ENTRYPOINT ["/opt/bitnami/scripts/spark/entrypoint.sh"]
CMD ["spark-class", "org.apache.spark.deploy.master.Master"]
