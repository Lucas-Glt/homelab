import time
import requests
from dotenv import load_dotenv
import os

load_dotenv("/srv/scripts/.env")

webhook_url = os.getenv("WEBHOOK_PORTFOLIO_MONITOR")

real_browsers = ["chrome/1", "chrome/2", "chrome/3", "firefox/", "edg/"]
bots = ["uptime-kuma", "bot", "crawler", "spider", "scan", "gptbot", 
        "censys", "zgrab", "go-http-client", "curl", "mj12", 
        "cms-checker", "chrome/108", "iphone os 13_2_3",
        "mozilla/5.0 applewebkit", "mozilla/5.0 (compatible"]
codeQr = "GET /?ref=qrcode"
linkedin = "GET /?ref=linkedin"
cv = "GET /?ref=cv"
with open("/var/log/nginx/access.log", "r") as f:
	f.seek(0, 2)
	while True:
		line = f.readline()
		if line:
			if (codeQr in line and " 200" in line):
				requests.post(webhook_url, json={"content":f"QR-Code : quelqu'un regarde ton portfolio"})
			if (linkedin in line and " 200" in line):
				requests.post(webhook_url, json={"content":f"Linkedin : quelqu'un regarde ton portfolio"})
			if (cv in line and " 200" in line):
				requests.post(webhook_url, json={"content":f"CV : quelqu'un regarde ton portfolio"})
		else:
			time.sleep(0.5)


