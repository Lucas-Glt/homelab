import psutil
import docker
import time
import requests
from dotenv import load_dotenv
import os

load_dotenv("/srv/scripts/.env")
client = docker.from_env()
containers = client.containers.list(all=True)
webhook_url= os.getenv("WEBHOOK_MONITOR")

#Gestion de temps d'alerte
last_alert_swap = 0
last_alert_ram = 0
last_alert_disk = 0
last_alert_cpu = 0
last_alert_coeur = 0
last_alert_status = 0

while True:
    containers = client.containers.list(all=True)
    for container in containers:
        if container.status != "running" :
            if time.time() - last_alert_status > 1800:
                requests.post(webhook_url, json={"content": f"{container.name}: - {container.status}"})
                last_alert_status = time.time()

    ram = psutil.virtual_memory()
    if (ram.percent > 85):
        if time.time() - last_alert_ram > 1800:
            requests.post(webhook_url, json={"content": f"ALERTE RAM : SEUIL CRITIQUE {ram.percent}%"})
            last_alert_ram = time.time()

    disk = psutil.disk_usage("/")
    if (disk.percent > 80):
        if time.time() - last_alert_disk > 1800:
            requests.post(webhook_url, json={"content": f"ALERTE DISQUE : SEUIL CRITIQUE {disk.percent}%"})
            last_alert_disk = time.time()

    cpuPercent = psutil.cpu_percent(2)
    if (cpuPercent > 90):
        if time.time() - last_alert_cpu > 1800:
            requests.post(webhook_url, json={"content": f"ALERTE CPU : SEUIL CRITIQUE {cpuPercent}%"})
            last_alert_cpu = time.time()

    coeur = psutil.getloadavg()
    if (coeur[2] > 4):
        if time.time() - last_alert_coeur > 1800:
            requests.post(webhook_url, json={"content": f"ALERTE CPU-COEUR : Processus en attente {coeur[2]}"})
            last_alert_coeur = time.time()

    swap = psutil.swap_memory()
    if (swap.percent > 50):
        if time.time() - last_alert_swap > 1800:
            requests.post(webhook_url, json={"content": f"ALERTE SWAP : RAM SECOURS A {swap.percent}%"})
            last_alert_swap = time.time()

    time.sleep(600)
