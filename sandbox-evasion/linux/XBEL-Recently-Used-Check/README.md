# XBEL Recently Used Check

This particular script will parse the `~/.local/share/recently-used.xbel` on a Linux system in order to get a list of recently accessed files in the format of `application:file path` in order to determine whether or not a system is a sandbox or VM. If a system has minimal or no recently accessed files, this may be an indication of a sandbox/VM. 

Within the script, you can modify the `threshold` variable in order to set a baseline to differentiate between a sandbox/VM & a real user. For example, if you set a threshold of 10, then if the script finds less than 10 recently accessed files, it'll assume the machine is a sandbox/VM.

*NOTE: This file is typically available on certain distributions of Linux. Not all Linux distros will contain this file and it may also be disabled by the end-user*
