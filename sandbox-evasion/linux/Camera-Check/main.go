package main

import (
	"fmt"
	"io/fs"
	"os"
	"strings"
	"io/ioutil"
)

func main() {
	root := "/sys/class/video4linux/"
	fileSys := os.DirFS(root)
	var camNames []string


	fs.WalkDir(fileSys, ".", func(path string, d fs.DirEntry, err error) error {
		if err != nil {
			fmt.Println(err)
		}
		
		if strings.HasPrefix(path, ".") != true {
			vidPath := root + path
			files, err := ioutil.ReadDir(vidPath)
			if err != nil {
				fmt.Println(err)
			}

			for _, file := range files {
				fPath := vidPath + "/" + file.Name()	
				if file.Name() == "name" {
					// Read camera name from file
					content, err := ioutil.ReadFile(fPath)
					if err != nil {
						fmt.Println(err)
					}
					camNames = append(camNames, string(content))
				}
			}
		}


		return nil
	})




	if len(camNames) == 0 {
		fmt.Println("[!] No cameras found to be associated within /sys/class/video4linux/! Possible sandbox/VM!")
	} else {
		fmt.Printf("[+] %d cameras found! Possibly not a sandbox/VM!\n", len(camNames))
	}
}
