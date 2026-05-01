from datetime import datetime
import requests
from dotenv import load_dotenv
import os

load_dotenv("/srv/scripts/.env")

aujourd_hui = datetime.now().strftime("%d/%b/%Y")

webhook_url = os.getenv("WEBHOOK_PORTFOLIO_MONITOR")

real_browsers = ["chrome/1", "chrome/2", "chrome/3", "firefox/", "edg/"]
bots = ["uptime-kuma", "bot", "crawler", "spider", "scan", "gptbot",
        "censys", "zgrab", "go-http-client", "curl", "mj12",
        "cms-checker", "chrome/108", "iphone os 13_2_3",
        "mozilla/5.0 applewebkit", "mozilla/5.0 (compatible"]

codeQrRef = "GET /?ref=qrcode"
linkedinRef = "GET /?ref=linkedin"
cvRef = "GET /?ref=cv"

counter = 0
qr = 0
linkedin = 0
cv = 0
autre = 0

with open("/var/log/nginx/access.log", "r") as f:

		for line in f:
			if ("GET / " in line and " 200" in line
                        and not any(b in line.lower() for b in bots)
                        and any(r in line.lower() for r in real_browsers)
			and (aujourd_hui in line)):
                                autre += 1
			if line:
                        	if (codeQrRef in line and " 200" in line and (aujourd_hui in line)):
                                	qr += 1
                        	if (linkedinRef in line and " 200" in line and (aujourd_hui in line)):
                                	linkedin += 1
                        	if (cvRef in line and " 200" in line and (aujourd_hui in line)):
                                	cv += 1

counter = qr + linkedin + cv + autre
requests.post(webhook_url, json={"content": f"""Rapport du {aujourd_hui}
Total : {counter} visiteurs
QR Code : {qr}
Linkedin : {linkedin}
CV : {cv}
URL direct : {autre}"""})
