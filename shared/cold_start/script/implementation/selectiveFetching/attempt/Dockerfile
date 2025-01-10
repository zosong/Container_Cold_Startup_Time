#1: Builder
FROM python:3.9-slim AS builder

# set environment variables
ENV PYTHONUNBUFFERED=1
ENV PATH=/home/jovyan/.local/bin:$PATH

# have a non-root user
RUN useradd -ms /bin/bash jovyan

WORKDIR /home/jovyan

USER jovyan

# copy and install Python dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# 2: Final Image
FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1
ENV PATH=/home/jovyan/.local/bin:$PATH

RUN useradd -ms /bin/bash jovyan

WORKDIR /home/jovyan

COPY --from=builder /home/jovyan/.local /home/jovyan/.local

COPY ./notebooks /home/jovyan/work

USER jovyan
EXPOSE 8888

# set entrypoint
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--no-browser"]
