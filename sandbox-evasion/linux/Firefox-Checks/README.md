# Firefox Extension Check - Sandbox Evasion

This script will search through the `addons.json` & `formhistory.sqlite` file in a Mozilla profile in an effort to find any extensions are installed & to find any typed data within the searchbar. If no extensions are installed & no typed data is found, this may hint that it's running inside of a sandbox. 

## References

* https://1d8.github.io/publications/evasion_1/
