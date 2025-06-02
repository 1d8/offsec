import requests
import os
import configparser
from datetime import datetime
import urllib.parse
import json
from pythonjsonlogger import jsonlogger
import logging
import argparse

def checkRoot():
    if os.getuid() != 0:
        return False
    else:
        return True

# Given SSID, return lat & lon coords
def wigleQuery(ssid, apikey):
    # urlencode SSID for GET req
    ssidEncoded = urllib.parse.quote(ssid)
    url = f"https://api.wigle.net/api/v2/network/search?onlymine=false&freenet=false&paynet=false&ssid={ssidEncoded}"
    r = requests.get(url, headers={"Authorization": f"Basic {apikey}"})
    stats = {}
    locationInfo = []
    for i in r.json()["results"]:
        locationInfo.append(f"{i['trilat']}:{i['trilong']}:{i['city']},{i['region']}")
        

    stats[ssid] = locationInfo
    return stats

def scrapeNmFiles(filename, configHandle, logHandle, apikey):
    config.read(filename)
    try:
        ssid = config["wifi"]["ssid"]
        timestampRaw = datetime.fromtimestamp(int(config["connection"]["timestamp"]))
        timestampReadable = timestampRaw.strftime('%Y-%m-%d %H:%M:%S')
        keyMgmtMode = config["wifi-security"]["key-mgmt"]
        passKey = config["wifi-security"]["psk"]
        
        stats = wigleQuery(ssid, apikey)
    
        # Build JSON log entry
        logger.info(f"[{timestampReadable}] {filename}:{ssid}", extra={"Key Management Mode": f"{keyMgmtMode}", "Key": f"{passKey}", "Location Info": f"{stats}"})
    except KeyError:
        pass


def gatherNmFiles():
    # Default directory /etc/NetworkManager/system-connections/*.nmconnection
    files = []
    rawListing = os.listdir("/etc/NetworkManager/system-connections/")
    for entry in rawListing:
        if os.path.isfile("/etc/NetworkManager/system-connections/" + entry) == True:
            if entry.endswith(".nmconnection") == True:
                files.append(entry)

    return files

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-api", "--api", required=True)
    args = parser.parse_args()

    if checkRoot():
        print("[+] Running as root")
        files = gatherNmFiles()
        print(f"[+] Enumerated SSID count: {len(files)}")
        # Build logging util
        logger = logging.getLogger("jsonLogger")
        logger.setLevel(logging.DEBUG)
        fileHandle = logging.FileHandler("results.json")
        formatter = jsonlogger.JsonFormatter()
        fileHandle.setFormatter(formatter)
        logger.addHandler(fileHandle)
        # create parser config obj
        config = configparser.ConfigParser()
        for file in files:
            scrapeNmFiles("/etc/NetworkManager/system-connections/" + file, config, logger, args.api)
        print("[+] Results saved to results.json file!")
        
    else:
        print("[!] Re-run as root! Exiting...")
