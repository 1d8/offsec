import pyudev, time, os
from pathlib import Path

"""
This script will monitor a Linux system for the insertion of an external media (EX: USB Device) & search for files with extensions of interest.
It can be modified to perform any event after it's triggered by the insertion of a USB device, such as downloading an additional payload & storing it on the USB device for example.
"""


interestingExts = ('.xlsx')

def getMountPath(devPath):
    #print(f'[+] Grabbing mount path for {devPath}')
    
    time.sleep(20) # We sleep for a bit to give the /proc/mounts file time to refresh & contain mount path for devpath
    
    try:
        with open("/proc/mounts", "r") as mFile:
            #print('[+] Reading /proc/mounts')
            for line in mFile:
                parts = line.split()
                if devPath.strip() in parts:
                        #print(f'[+] Mount path found for {devPath}: {parts[1]}') #parts[1] -> full file path
                        return parts[1]
    except:
        print("[!] Cannot open /proc/mounts!")

def getInterestingFiles(fPath, interestingExt):
    print(f'[+] Interesting file ext list: {interestingExt}')
    for path in Path(fPath).rglob('*'):
        if len(path.suffix) != 0 and path.suffix in interestingExt:
            print(f'[+] Found interesting file: {path}')
        #if path.suffix in interestingExts:
        #    print(f'[+] Interesting file discovered: {path}')


def getDevPath():
    context = pyudev.Context()

    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by('block')

    monitor.start()




    for device in iter(monitor.poll, None):
        if device.device_type in ('disk', 'partition'):
            device_node = device.device_node
            if device.action == 'add':
                print(f'[+] Device connected: {device_node}!')
                

                mntPath = getMountPath(device_node)
                print(f'[+] Mount path for {device_node}: {mntPath}')
                if mntPath is not None:
                    getInterestingFiles(mntPath, interestingExts)

getDevPath()
