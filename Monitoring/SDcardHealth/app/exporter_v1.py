from prometheus_client import start_http_server, Gauge
import subprocess
import time
import json
import re

# Metrics
sd_health = Gauge('sd_card_health_percent', 'Remaining SD card health (%)')
iostat_tps = Gauge('iostat_tps', 'Transfers per second')
iostat_kb_read_s = Gauge('iostat_kb_read_s', 'Kilobytes read per second')
iostat_kb_wrtn_s = Gauge('iostat_kb_wrtn_s', 'Kilobytes written per second')
iostat_kb_read = Gauge('iostat_kb_read', 'Total kilobytes read')
iostat_kb_wrtn = Gauge('iostat_kb_wrtn', 'Total kilobytes written')

def read_metrics():
    # mmc health (from Transcend patched binary)
    try:
        out = subprocess.check_output(["/usr/local/bin/mmc", "health", "/dev/mmcblk1"]).decode()
        for line in out.splitlines():
            match = re.search(r'Card\s+Life.*?:\s*(\d+)\s*%', line)
            print(f"{match}")
            if match:
                percent_used = int(match.group(1))
                percent_used = int(line.split(':')[-1].strip().split('%')[0])
                sd_health.set(percent_used)
                break
    except Exception as e:
        print(f"Error getting mmc health: {e}")
        sd_health.set(0)

    # iostat with JSON parsing
    try:
        io = subprocess.check_output(["iostat", "-d", "-o", "JSON", "1", "2", "/dev/mmcblk1"],stderr=subprocess.STDOUT).decode()
        
        # Parse JSON output
        data = json.loads(io)
        disk_data = data['sysstat']['hosts'][0]['statistics'][0]['disk'][0]
        
        iostat_tps.set(float(disk_data['tps']))
        iostat_kb_read_s.set(float(disk_data['kB_read/s']))
        iostat_kb_wrtn_s.set(float(disk_data['kB_wrtn/s']))
        iostat_kb_read.set(float(disk_data['kB_read']))
        iostat_kb_wrtn.set(float(disk_data['kB_wrtn']))
        
    except Exception as e:
        print(f"iostat error: {str(e)}")
        iostat_tps.set(0)
        iostat_kb_read_s.set(0)
        iostat_kb_wrtn_s.set(0)
        iostat_kb_read.set(0)
        iostat_kb_wrtn.set(0)

if __name__ == '__main__':
    start_http_server(8000)
    print(f"Server started ...")
    while True:
        print(f"Reading metrics - SD health: {sd_health}")
        print(f"Reading metrics - iostat: tps {iostat_tps}| kb_read/s {iostat_kb_read_s} | kb_write/s {iostat_kb_wrtn_s} ")
        read_metrics()
        time.sleep(15)
