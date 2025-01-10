# totally two stages, setup components and build image
# 1: base setup with essential MySQL components for startup
FROM mysql:latest AS base

# update packages and install only critical dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libaio1 \
    && rm -rf /var/lib/apt/lists/*

# then copy essential MySQL configurations and binaries
COPY --from=mysql:latest /etc/mysql /etc/mysql
COPY --from=mysql:latest /usr/bin/mysqld /usr/bin/mysqld

# initialize data directory
RUN mkdir -p /var/lib/mysql && chown -R mysql:mysql /var/lib/mysql

# copy optimization script
COPY sf.py /opt/sf.py

# 2: build the final image with selective loading
FROM mysql:latest AS final

# copy essential files and optimization script from the base stage
COPY --from=base /usr/bin/mysqld /usr/bin/mysqld
COPY --from=base /etc/mysql /etc/mysql
COPY --from=base /opt/sf.py /opt/sf.py

# load only the critical components necessary for MySQL to start
# set up permissions
RUN mkdir -p /var/run/mysqld && chown -R mysql:mysql /var/run/mysqld

# expose MySQL port
EXPOSE 3306

# set environment variables
ENV MYSQL_ALLOW_EMPTY_PASSWORD=true

# run optimization code at startup before starting MySQL
ENTRYPOINT ["sh", "-c", "python3 /opt/sf.py && exec mysqld"]

