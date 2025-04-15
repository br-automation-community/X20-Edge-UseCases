# Lightweight Monitoring Stack with Prometheus and cAdvisor

This stack provides a lightweight monitoring setup using **Prometheus**, **Node Exporter**, and **cAdvisor**, with optional support for SD card health monitoring via a custom **sdcard-exporter**.

> **Note**: Grafana is not part of this stack. It is assumed to run in a separate environment and connect to Prometheus remotely.

## Stack Overview

- **Prometheus**: Time-series database and monitoring system that scrapes metrics from exporters.
- **Node Exporter**: Collects system-level metrics from the host (CPU, memory, disk, etc.).
- **cAdvisor**: Exposes container-level metrics (CPU, memory, I/O, etc.).
- **sdcard-exporter**: (optional) Custom exporter to monitor SD card health and wear. See [`sdcard-exporter.md`](sdcard-exporter.md) for details.

## Architecture
```
                             +-----------------------+
                             |     Grafana (external)|
                             |   (dashboard/visuals) |
                             +-----------+-----------+
                                         |
                                         v
                              Exposes on port 9090
                             +-----------------------+
                             |      Prometheus       |
                             |-----------------------|
                             | Scrapes metrics from: |
                             |  - node-exporter      |
                             |  - cadvisor           |
                             |  - sdcard-exporter    |
                             +-----------+-----------+
                                         |
       ----------------------------------+---------------------------------
       |                                 |                                 |
       v                                 v                                 v
+-------------------+       +-----------------------+        +------------------------+
|   node-exporter   |       |       cAdvisor        |        |     sdcard-exporter    |
|-------------------|       |-----------------------|        |------------------------|
| Host system stats |       | Docker/container stats|        |  SD card health stats  |
|   (CPU, mem, fs)  |       |   (CPU, mem, IO, etc.)|        | (wear, read errors...) |
+-------------------+       +-----------------------+        +------------------------+
```
All services run in a shared Docker `monitoring` network.



##  💡 Docker Compose Configuration

This stack uses Docker Compose with:

- A dedicated `monitoring` bridge network.
- Persistent storage for Prometheus metrics.
- Proper host mounts for exporter access.
- Minimal port exposure (only Prometheus is exposed externally).

### Services

#### Prometheus
- Web UI: [http://host-ip:9090](http://host-ip:9090)
- Scrapes metrics from all exporters in the `monitoring` network.

#### Node Exporter
- Exposes host-level metrics at port `9100` (internal only).

#### cAdvisor
- Exposes container metrics at port `8080` (internal only).

#### sdcard-exporter (Optional)
- Builds from the local `./SDcardHealth` directory.
- Requires `privileged` mode for accessing `/dev/mmcblk1`.
- Exposes metrics at port `8000` (internal only).
- See [`sdcard-exporter`](sdcard-exporter.md), [`SD Card Health`](sd-card-health.md)for detailed usage and metrics.

## 🛠️ Setup
```bash
Monitoring/
│
├── docker-compose.yml
│
├── prometheus/
│   ├── _data/                  # Volume mount for Prometheus storage
│   └── prometheus.yml          # Prometheus configuration file
│
└── SDcardHealth/
    ├── Dockerfile              # Dockerfile for building sdcard-exporter
    ├── grafana-dashboard.json # Exported Grafana dashboard (optional)
    └── app/
        ├── exporter.py         # Python script collecting SD card metrics
        └── mmc/                # Tools or scripts for MMC/SD access
```
### 🚀 How to Start the Stack
1) Make sure you're in the Monitoring/ directory:

>```bash
>cd Monitoring
>```

2) Launch the stack:

>```bash
>docker compose up -d
>```

3) Prometheus will start and automatically begin scraping:

 - Node metrics (`node-exporter`)

 - Docker/container metrics (`cAdvisor`)

 - SD card health (`sdcard-exporter`)

4) Your external Grafana instance can be configured to connect to Prometheus at:

>```cpp
>http://<your-docker-host>:9090
>```

For SD card metrics dashboard, you can import the provided grafana-dashboard.json in Grafana.

### Prometheus Configuration

```yaml
scrape_configs:
  - job_name: 'node'
    static_configs:
      - targets: ['node-exporter:9100']

  - job_name: 'cadvisor'
    static_configs:
      - targets: ['cadvisor:8080']

  - job_name: 'sdcard'
    static_configs:
      - targets: ['sdcard-exporter:8000']

```

## 🚨 Security Notes
The sdcard-exporter runs with privileged access to interact with low-level hardware.  
The Prometheus and exporter ports are internal except for Prometheus (port 9090).  
Adjust user/group permissions for sdcard-exporter if needed in production.  