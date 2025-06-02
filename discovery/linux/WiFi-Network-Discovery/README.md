# WiFi Network Discovery

Tool meant to enumerate all connection files located within `/etc/NetworkManager/system-connections/<SSID>.nmconnection`, gathering SSID, network passkey, as well as additional location details gathered from Wigle

Requires API key from Wigle

# Usage

`pip3 install -r requirements.txt`

`python3 main.py -apikey <Wigle-api-key-here>`

All results will then be saved within a `results.json` file.
