# Stage 1: Build patched mmc binary
FROM debian:bookworm-slim AS build

RUN apt-get update && apt-get install -y \
    git build-essential sparse \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
RUN git clone --depth 1 https://kernel.googlesource.com/pub/scm/utils/mmc/mmc-utils
RUN git clone --depth 1 https://github.com/transcend-information/RaspberryPi_NVIDIAJetson-SDcard-SMARTQuery.git transcend-patches

RUN cp transcend-patches/mmc-utils/*.c mmc-utils/ && \
    cp transcend-patches/mmc-utils/*.h mmc-utils/

WORKDIR /app/mmc-utils
RUN make

# Stage 2: Runtime container
FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    sysstat jq \
    && rm -rf /var/lib/apt/lists/*

COPY --from=build /app/mmc-utils/mmc /usr/local/bin/mmc
RUN chmod +x /usr/local/bin/mmc
RUN chmod 4755 /usr/local/bin/mmc

# Add essential groups and permissions
RUN groupadd -f -g 6 disk && \
    useradd -r -s /bin/false -G disk exporter && \
    chmod 4755 /usr/local/bin/mmc  # SUID bit for mmc utils

WORKDIR /home/exporter

RUN pip install --user prometheus_client
COPY app/exporter.py .

EXPOSE 8000
CMD ["python3", "exporter.py"]
