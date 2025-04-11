# SD Card Exporter Documentation

This exporter monitors the health and performance of an SD card using B&R X20 Edge tools and exposes the data in Prometheus-compatible format.

It builds upon the B&R use case documented at:  
[`SD Card Health`](sd-card-health.md)

---

## 📝 Overview

The `sdcard-exporter` is a containerized Python application that uses:
- `mmc` utility (from B&R) to retrieve SMART data from `/dev/mmcblk1`
- `iostat` to gather disk usage statistics
- `prometheus_client` Python module to expose metrics on port `8000`

These metrics are scraped by Prometheus and visualized in Grafana.

---

## 🐳 Container Structure

Folder structure:
```c
Monitoring/
├── docker-compose.yml
├── prometheus/
│   ├── prometheus.yml
│   └── _data/              # Prometheus data volume
└── SdcardHealth/
    ├── Dockerfile
    ├── sdcard-exporter.json    # Grafana dashboard export
    └── app/
        ├── exporter.py         # Python exporter script
        └── mmc                 # MMC binary from B&R

```
## 📊 Exported Metrics

### From `mmc smart /dev/mmcblk1`
- `sd_card_health_percent`
- `sd_card_bad_blocks`
- `sd_card_spare_blocks`
- `sd_card_min_erase_count`
- `sd_card_max_erase_count`
- `sd_card_total_erase_count`
- `sd_card_avg_erase_count`
- `sd_card_pe_cycles`
- `sd_card_power_cycles`
- `sd_card_write_crc_errors`

### From `iostat -d -o JSON`
- `iostat_util_percent`
- `iostat_tps`
- `iostat_kb_read_s`
- `iostat_kb_wrtn_s`
- `iostat_kb_read`
- `iostat_kb_wrtn`

---

## 🚀 Running the Exporter

The container is built and managed via Docker Compose. Here's a snippet from `docker-compose.yml`:

```yaml
  sdcard-exporter:
    build: ./SdcardHealth
    container_name: sdcard-exporter
    restart: unless-stopped
    privileged: true
    cap_add:
      - SYS_RAWIO
      - SYS_ADMIN
    devices:
      - "/dev/mmcblk1:/dev/mmcblk1"
    volumes:
      - "/dev:/dev"
    expose:
      - "8000"
    user: "0:0"
    tty: true
    stdin_open: true
    networks:
      - monitoring
```
## 📡 Prometheus Integration
Add this job to prometheus/prometheus.yml:
```yaml
  - job_name: 'sdcard-exporter'
    static_configs:
      - targets: ['sdcard-exporter:8000']
```
## 📊 Grafana Dashboard
Import the dashboard:

Go to Grafana → **Dashboards** → **Import**

Upload `sdcard-exporter.json` from the `SDcardHealth` folder

Set Prometheus as the data source

Alternatively, you can customize this dashboard using B&R’s original templates or your own metrics.

## ⚙️ Notes
The exporter must run with root privileges (`user: "0:0"`, `privileged: true`) to access SD card diagnostics.

Make sure `/dev/mmcblk1` matches your system's SD card device.

The Python script sleeps 15 seconds between metric reads. Adjust this if needed.

For visual examples and step-by-step dashboard import, refer to the main documentation file: monitoring-stack.md.

