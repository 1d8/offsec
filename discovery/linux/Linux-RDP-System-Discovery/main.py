import os
"""
Todo: 
    [ ] Check each previously connected RDP host to see if RDP port is still open
"""



prefPath = os.path.expanduser("~/.config/remmina/remmina.pref")
rdpHosts = []

with open(prefPath, "r") as file:
    data = file.readlines()
    for line in data:
        if line.startswith("recent_RDP"):
            csvIPs = line.split("=")[1]
            for ip in csvIPs.split(","):
                rdpHosts.append(ip)

print(f"[+] Previously connected hosts with RDP open: {rdpHosts}")
