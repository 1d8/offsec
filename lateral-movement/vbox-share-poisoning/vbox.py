import virtualbox


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


    print(f"[+] {sharedFolder} | writable: {writable}")
    return writable, sharedFolder

"""
Currently will only enumerate shared folders

Todo
- [ ] Test if it'll enumerate multiple shared folders
- [ ] Add in functionality that'll add malware to the shared folder
- [ ] Add in functionality that if there's no shared folder, it'll create one
- [ ] Maybe auto-mount the shared folder if it's not already mounted?
- [ ] Turn shared folder finder into a separate function
- Docs/available functions: https://github.com/sethmlarson/virtualbox-python/blob/master/virtualbox/library.py
"""

if __name__ == '__main__':
    machines = findVMs()
    vbox = virtualbox.VirtualBox()

    for machine in machines:
        vm = vbox.find_machine(machine)
        session = vm.create_session()

        sharedFolders = session.machine.shared_folders
        if len(sharedFolders) != 0:
            tmpDict = {}
            sharedFolderList = []
            for item in sharedFolders:
                tmpDict["VM Name"] = machine
                tmpDict["Shared Folder Name"] = item.name
                tmpDict["Shared Folder Host Path"] = item.host_path
                tmpDict["Writable"] = item.writable
            
            sharedFolderList.append(tmpDict)


        session.unlock_machine()

    
    #print(f"[+] Discovered shared folders: {sharedFolderList}")

    # Loop through discovered shared folders & check if writable
    for entry in sharedFolderList:
        checkCanWrite(entry)
