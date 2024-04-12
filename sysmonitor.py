import psutil
import datetime
import math

import email_service

# Function to collect system metrics
def collect_metrics():
    cpu_percent = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()
    mem_percent = mem.percent
    disk = psutil.disk_usage('/')
    disk_percent = disk.percent
    net = psutil.net_io_counters()
    network_traffic = [net.bytes_sent, net.bytes_recv]
    return cpu_percent, mem_percent, disk_percent, network_traffic

# Function to generate report
def generate_report(cpu_percent, mem_percent, disk_percent, network_traffic):
    timestamp = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    network_traffic_sent = f"{math.ceil(network_traffic[0] / 1024):,}"
    network_traffic_received = f"{math.ceil(network_traffic[1] / 1024):,}"
    report = f"Performance Report - {timestamp}\n"
    report += f"CPU Usage: {cpu_percent}%\n"
    report += f"Memory Usage: {mem_percent}%\n"
    report += f"Disk Usage: {disk_percent}%\n"
    report += f"Network Traffic Sent: {network_traffic_sent}KB\n"
    report += f"Network Traffic Received: {network_traffic_received}KB\n"
    return report

def main():
    cpu_percent, mem_percent, disk_percent, network_traffic = collect_metrics()
    report = generate_report(cpu_percent, mem_percent, disk_percent, network_traffic)
    print(report)
    email_service.send_email("System report", report)

    if cpu_percent > 90:
        email_service.send_email("High CPU Usage Alert", f"CPU usage is {cpu_percent}%")
    if mem_percent > 90:
        email_service.send_email("High Memory Usage Alert", f"Memory usage is {mem_percent}%")
    if disk_percent > 90:
        email_service.send_email("High Disk Usage Alert", f"Disk usage is {disk_percent}%")

if __name__ == "__main__":
    main()
