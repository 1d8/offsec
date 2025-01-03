#include "head.h"
#include <stdio.h>
#include <windows.h>
#include <wbemidl.h>
#include <tchar.h>

#define k(msg, ...) printf("[+] " msg "\n", ##__VA_ARGS__)
#define w(msg, ...) printf("[-] " msg "\n", ##__VA_ARGS__)
#define i(msg, ...) printf("[i] " msg "\n", ##__VA_ARGS__)


int main(void){
	
	HRESULT hr = 0;
	int serial;

	IWbemLoator *locator = NULL;
	IWbemServices * services = NULL;
	IEnumWbemClassObject *results = NULL;

    BSTR resource = SysAllocString(L"ROOT\\CIMV2");
    BSTR language = SysAllocString(L"WQL");
		BSTR query = SysAllocString(L"SELECT * FROM Win32_SerialNumber");

		hr = CoInitalizeEx(0, COINIT_MULTITHREADED);
		hr =  CoInitalizeSecurity(NULL, -1, NULL, NULL, RPC_C_AUTHN_LEVEL_DEFAULT, RPC_C_IMP_LEVEL_IMPERSONATE, NULL, EOAC_NONE, NULL);
		
	hr CoCreateIntsance(&CLSID_WbemLocator, 0 , CLSCTX_INPROC_SERVER, &IID_IWbemLocator, (LPVOID *) &locator);
	hr locator ->lpVtbl->ConnectServer(locator, resource, NULL, NULL, NULL, 0, NULL, NULL, &services);

	hr = services->lpVtbl->ExecQuery(services, language, query, WBEM_FLAG_BIDIRECTIONAL, NULL, &results);

		if (results != NULL){
		IWbemClassObject *result = NULL;
		ULONG returnedCount =0;

		while((hr = results->lpVtbl->Next(results, WBEM_INFINITE, 1, &result, &returnedCount))==S_OK){
			VARIANT number;

			hr = result->Get(result,L"SerialNumber", 0, &number, 0,0);
			serial = number.intVal;
		result->lpVtbl->Release(result);

		}
	}

		results->lpVtbl->Release(results);
    services->lpVtbl->Release(services);
    locator->lpVtbl->Release(locator);

    // unwind everything else we've allocated
    CoUninitialize();

    SysFreeString(query);
    SysFreeString(language);
    SysFreeString(resource);
		
	if (serial == 0){
		i("virtual env detected!");
	}
	else{
		i("non virtual env detected!")
	}
}
