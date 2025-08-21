import subprocess
from datetime import datetime
import urllib.request
import requests

outputFile = "report.txt"
URL = "http://YOUR_PC_IP:8000/upload"  # Use LAN IP or public if port-forwarded

def writeLog(message):
    with open(outputFile, "a") as f:
        f.write(f"{message}\n")

def log():
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    writeLog(f"Date/Time Stamp: {stamp}")

def pubIP():
    try:
        pub = urllib.request.urlopen("https://api.ipify.org").read().decode("utf8")
        writeLog(f"Public IPv4 Address is: {pub}")
    except Exception as e:
        writeLog(f"Error Getting Public IPv4: {e}")

def config():
    try:
        result = subprocess.run(["ipconfig"], capture_output=True, text=True, shell=False)
        writeLog(result.stdout)
    except Exception as e:
        writeLog(f"Error: {e}")

def ping():
    try:
        result = subprocess.run(["ping", "-n", "4", "8.8.8.8"], capture_output=True, text=True, shell=False)
        writeLog(result.stdout if result.returncode == 0 else "Ping Failed.")
    except Exception as e:
        writeLog(f"Error During Ping: {e}")

def sendFile():
    try:
        with open(outputFile, "rb") as f:
            files = {'file': (outputFile, f)}
            requests.post(URL, files=files)
        writeLog("Data sent successfully.")
    except Exception as e:
        writeLog(f"Failed to send file: {e}")

def main():
    log()
    pubIP()
    config()
    ping()
    sendFile()

if __name__ == "__main__":
    main()   