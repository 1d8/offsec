#include <stdio.h>
#include <string.h>
#include <windows.h>
#include <stdlib.h>
i

/* Todo
 * - Cleanup the code & rename variables to be more descriptive
 *
 */

char baseRegKey[] = "SOFTWARE\\Microsoft\\Terminal Server Client\\Servers";
char baseRegKeyName[MAX_PATH];
DWORD index = 0;
DWORD baseRegKeySz;

int main() {
	HKEY hKey;
	LSTATUS result = RegOpenKeyEx(HKEY_CURRENT_USER, baseRegKey, 0, KEY_ALL_ACCESS, &hKey);
	if (result != ERROR_SUCCESS) {
		printf("[!] Error opening registry key!\n");
	}
	while (1) {
		baseRegKeySz = sizeof(baseRegKeyName);
		// Grabbing all subkeys which would be past RDP connections
		LONG result = RegEnumKeyEx(hKey, index, baseRegKeyName, &baseRegKeySz, NULL, NULL, NULL, NULL);

		// Loop through all subkeys
		if (result == ERROR_NO_MORE_ITEMS) {
			break;
		} else if (result == ERROR_SUCCESS) {
			// Here query the value for that specific baseRegKeyName to grab the username hint
			HKEY tmpKey;
			char data[1024];
			DWORD dataSize = sizeof(data);
			DWORD valueType;
			
			// Combining IP address to the base registry key
			char *regKey = malloc(strlen(baseRegKey) + strlen(baseRegKeyName) + 1);
			if (regKey == NULL) {
				printf("[!] Memory allocation failed!\n");
			}

			strcpy(regKey, baseRegKey);
			strcat(regKey, "\\");
			strcat(regKey, baseRegKeyName);


			LSTATUS result2 = RegOpenKeyEx(HKEY_CURRENT_USER, regKey, 0, KEY_ALL_ACCESS, &tmpKey);
			if (result2 != ERROR_SUCCESS) {
				printf("[!] Error opening subkey for enumeration of %s\n", regKey);
			}


			LSTATUS result3 = RegQueryValueEx(tmpKey, "UsernameHint", NULL, &valueType, (LPBYTE)data, &dataSize);
			if (result3 == ERROR_SUCCESS) {
				printf("[+] Previous RDP connection details: %s@%s\n", data, baseRegKeyName);

			}

			free(regKey);
			RegCloseKey(tmpKey);
			index++;
		} else {
			printf("Failed to enum subkeys\n");
			break;
		}
	}
	RegCloseKey(hKey);
	
	
	return 0;
}
