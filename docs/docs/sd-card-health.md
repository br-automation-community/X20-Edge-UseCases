---
sidebar_position: 4
---

# ❤️ SD Card Health

## Overview
SD cards in industrial and embedded systems endure significant wear due to continuous read/write operations. Monitoring their health can help predict failures and extend their lifespan. This guide provides a **Dockerized** approach using `mmc-utils`, and explores native Linux tools like `iostat` and `/proc/diskstats` for tracking SD card wear and performance.

## 1️⃣ Setting Up `mmc-utils` in Docker

### **Dockerfile for `mmc-utils`**
This Dockerfile:
1. **Clones** the official `mmc-utils` repository.
2. **Clones** the transcend repository including patches to source files that make it possible to fetch SMART information from transcend SD Cards.
2. **Overwrites** the files in the official `mmc-utils` repository with the ones coming from Transcend.
3. **Builds** the modified `mmc-utils`.
4. **Allows running the tool on host devices**.

```dockerfile
# Stage 1: Build the binary
FROM debian:bookworm-slim AS build

RUN apt-get update && apt-get install -y \
    git build-essential sparse \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN git clone https://kernel.googlesource.com/pub/scm/utils/mmc/mmc-utils
RUN git clone https://github.com/transcend-information/RaspberryPi_NVIDIAJetson-SDcard-SMARTQuery.git transcend-patches

RUN cp transcend-patches/mmc-utils/lsmmc.c mmc-utils/ && \
    cp transcend-patches/mmc-utils/mmc.c mmc-utils/ && \
    cp transcend-patches/mmc-utils/mmc.h mmc-utils/ && \
    cp transcend-patches/mmc-utils/mmc_cmds.c mmc-utils/ && \
    cp transcend-patches/mmc-utils/mmc_cmds.h mmc-utils/

WORKDIR /app/mmc-utils
RUN make

# Runtime stage: copy only the binary into a minimal environment
FROM debian:bookworm-slim

# Create directory for binary
WORKDIR /app

# Copy compiled binary from previous stage
COPY --from=0 /app/mmc-utils/mmc .

ENTRYPOINT ["./mmc"]
```

### **Building & Running the Container**

#### **1️⃣ Build the Docker Image**
```bash
docker build -t mmc-utils .
```

#### **2️⃣ Run the Container with Access to the SD Card**
```bash
docker run --rm --privileged -v /dev:/dev mmc-utils smart /dev/mmcblk1
```
(*Replace `/dev/mmcblk1` with your actual SD card device path.*)

### **Monitoring SD Card Health with `mmc-utils`**

#### **Check SMART Info**
```bash
docker run --rm --privileged -v /dev:/dev mmc-utils smart /dev/mmcblk1
```

#### **Check SD Card Health**
```bash
docker run --rm --privileged -v /dev:/dev mmc-utils health /dev/mmcblk1
```

## 2️⃣ Monitoring SD Card Write Activity with `iostat`

`iostat` provides real-time disk usage and I/O statistics.

### **Installing `iostat` (if not installed)**
```bash
sudo apt-get install sysstat
```

### **Basic Usage**
```bash
iostat -d -k 1 1
```
- `-d`: Show **disk statistics**.
- `-k`: Display values in **KB (kilobytes)**.
- `1 1`: Take **one measurement**, wait **one second**, and print the result.

**Example Output:**
```
Device       tps    kB_read/s    kB_wrtn/s    kB_read    kB_wrtn
mmcblk1      12.0         0.0       1536.0         0       1536
```
📌 **Key Metrics:**
- `tps` = Transfers per second.
- `kB_wrtn/s` = KB written per second.
- `kB_wrtn` = Total KB written since system boot.

### **Continuous Monitoring**
```bash
iostat -d -k 10
```
📌 **This updates every 10 seconds.**

---

## 3️⃣ Deep Dive: Visualizing Disk Statistics (`/proc/diskstats`)

Linux provides detailed disk write statistics through the `/proc/diskstats` file. Here's a clearer and more interactive approach:

### 🔍 **Check Disk Write Stats**

Quickly view statistics for your disk (e.g., `mmcblk1`):
```bash
cat /proc/diskstats | grep mmcblk1
```

**Example Output:**
```
179       0 mmcblk1 33890 8762 2892906 110522 22176313 8542353 249743440 47112865 0 49371376 47569059 6702 9 104127704 345671 0 0
```

---

### 📋 **Important Metrics**

| Metric                 | Field # | Example Value | Description                        |
|------------------------|---------|---------------|------------------------------------|
| 📝 **Sectors Written** | **10**  | `249743440`   | Total sectors written since boot.  |
| ⏱️ **Write Time (ms)** | **11**  | `47112865`    | Total milliseconds spent writing.  |

---

### 🧮 **Calculate Data Written (One-liner)**

Each **sector is 512 bytes**. Here's a simple one-liner to display sectors written directly in MB:

```bash
echo "$(( $(awk '$3=="mmcblk1"{print $10}' /proc/diskstats) * 512 / 1024 / 1024 )) MB written"
```

📌 **This outputs data written directly in MB.**

---

## 🚀 **Conclusion & Recommendations**
- ✅ **Use `mmc-utils` in Docker** to assess SD card health (SMART & erase cycles).
- ✅ **Monitor real-time write activity** with tools like `iostat`.
- ✅ **Analyze historical data precisely** using `/proc/diskstats`.

