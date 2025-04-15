from prometheus_client import start_http_server, Gauge
import subprocess
import time
import json
import re

# MMC
sd_health = Gauge('sd_card_health_percent', 'Remaining SD card health (%)')
sd_bad_blocks = Gauge('sd_card_bad_blocks', 'New bad block count')
sd_spare_blocks = Gauge('sd_card_spare_blocks', 'Remaining spare blocks')
sd_erase_count_min = Gauge('sd_card_min_erase_count', 'Minimum erase count')
sd_erase_count_max = Gauge('sd_card_max_erase_count', 'Maximum erase count')
sd_erase_count_total = Gauge('sd_card_total_erase_count', 'Total erase operations')
sd_erase_count_avg = Gauge('sd_card_avg_erase_count', 'Average erase count')
sd_pe_cycles = Gauge('sd_card_pe_cycles', 'Program/Erase cycles (max)')
sd_power_cycles = Gauge('sd_card_power_cycles', 'Power on/off count')
sd_crc_errors = Gauge('sd_card_write_crc_errors', 'Total Write CRC Count')
sd_iostat_util = Gauge('iostat_util_percent', 'Disk utilization (%) from iostat')

#IOSTAT
iostat_tps = Gauge('iostat_tps', 'Transfers per second')
iostat_kb_read_s = Gauge('iostat_kb_read_s', 'Kilobytes read per second')
iostat_kb_wrtn_s = Gauge('iostat_kb_wrtn_s', 'Kilobytes written per second')
iostat_kb_read = Gauge('iostat_kb_read', 'Total kilobytes read')
iostat_kb_wrtn = Gauge('iostat_kb_wrtn', 'Total kilobytes written')

def extract_int(line):
    """Extract the last integer from a line."""
    match = re.search(r'(\d+)\s*%?$', line)
    return int(match.group(1)) if match else None

def read_metrics():
    try:
        out = subprocess.check_output(["/usr/local/bin/mmc", "smart", "/dev/mmcblk1"]).decode()
        for line in out.splitlines():
            if "Card Life" in line:
                sd_health.set(extract_int(line))
            elif "New Bad block Count" in line:
                sd_bad_blocks.set(extract_int(line))
            elif "Spare Block" in line:
                sd_spare_blocks.set(extract_int(line))
            elif "Min Erase Count" in line:
                sd_erase_count_min.set(extract_int(line))
            elif "Max Erase Count" in line:
                sd_erase_count_max.set(extract_int(line))
            elif "Total Erase Count" in line:
                sd_erase_count_total.set(extract_int(line))
            elif "Avg. Erase Count" in line:
                sd_erase_count_avg.set(extract_int(line))
            elif "NAND P/E Cycle" in line:
                sd_pe_cycles.set(extract_int(line))
            elif "Power On/Off Count" in line:
                sd_power_cycles.set(extract_int(line))
            elif "Total Write CRC Count" in line:
                sd_crc_errors.set(extract_int(line))
    except Exception as e:
        print(f"Error getting mmc smart info: {e}")

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
