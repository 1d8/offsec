# Vbox Shares

This particular method will enumerate any shared folders that exist within VirtualBox. Then depending on the mode it's ran in, it'll either enumerate & zip files in shared folders or poison them. 


So far:

* Enum mode will enumerate any shared folders available for virtual machines & zip up their folders for exfiltration
* Poison mode will:
	* Zip up shared folders for exfil & backup
	* Replace legitimate files within the shared folders with malicious ones. It does so by referencing a config file which has locations of the malicious files for each filetype


# Usage

This tool currently supports 2 modes:

1. Enum -> Enumeration of shared Vbox folders
2. Poison -> Replace specific filetypes with malicious ones within shared Vbox folders

## Enum Mode

`python vbox.py -m enum`

This will zip up all Vbox shared folder directories for exfiltration

![](https://i.ibb.co/KpQWyQMF/2025-02-22-19-42.png)

## Poison Mode

`python vbox.py -m poison poison.cfg`

If using poison mode, you have to specify a config file which is in the following format:

```yml
[filetype locations]
txt = payloads/evil.txt
docm = payloads/evil.docm
exe = payloads/shellcode.exe
```
The config file contains the file types you wish to poison & the malicious file locations that legitimate files will be replaced with.

In addition to poisoning, a zip file will be created with the original files for backup purposes.

![](https://i.ibb.co/fdh5qRKn/2025-02-22-19-43.png)
