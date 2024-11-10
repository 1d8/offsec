import inotify.adapters
import psutil
import argparse


def main():
    # Preparing arguments
    parser = argparse.ArgumentParser(description="Utility to monitor & report on filesystem changes within specified directory")
    parser.add_argument("-d", "--directory", help="Directory to watch")
    args = parser.parse_args()
    if args.directory is None:
        print("[!] Must pass directory to monitor to the -d/--directory flag")
        return

    i = inotify.adapters.Inotify()
    
    print(f"[+] Monitoring {args.directory}")
    i.add_watch(args.directory)

    for event in i.event_gen(yield_nones=False):
        (_, type_names, path, filename) = event
        if "IN_CREATE" in type_names:
            # If file is open in vim for example, it errors out 
            fullPath = path + "/" + filename 
            # Testing to see if its a swp file that was created
            if fullPath.split("/")[-1].startswith(".") and fullPath.split("/")[-1].endswith(".swp"):
                #print(f"[!] Swap file detected: {fullPath}")   
                newPath = path + "/" + fullPath.split("/")[-1][1:].replace(".swp", "")

            elif fullPath.split("/")[-1].startswith(".") and fullPath.split("/")[-1].endswith(".swx"):
                #print(f"[!] Swap file detected: {fullPath}")
                newPath = path + "/" + fullPath.split("/")[-1][1:].replace(".swx", "")

            #print(f"[+] New file created: {fullPath}")
            while isOpen(fullPath) == True:
                #print(f"[!] {fullPath} is already opened!")
                pass
            
            f = open(newPath, 'r')
            data = f.readlines()
            print(f"[+] Contents of {newPath}: {data}")


def isOpen(path):
    for proc in psutil.process_iter():
        try:
            for item in proc.open_files():
                if path == item.path:
                    return True
        except Exception:
            pass
    return False

main()
