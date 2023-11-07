#include <iostream>
#include <windows.h>
#include <filesystem>
using std::cout;
using std::endl;
using std::string;


int main(int argc, char *argv[]){
    // 啟動時不開啟cmd視窗
    ShowWindow(FindWindowA("ConsoleWindowClass", NULL), false);
    // 獲取執行檔path
    char exePath[MAX_PATH];
    GetModuleFileName(NULL, exePath, MAX_PATH);
    string exePathS = exePath;
    exePathS = exePathS.substr(0, exePathS.find_last_of("\\/"));
    // 先cd到此目錄
    SetCurrentDirectory(exePathS.c_str());
    
    
    string cmd= "start python-3.10.10-embed\\pythonw.exe video-flip\\costom_ui2.py";
    // 如果有額外的args，代表是對影片檔點右鍵>以main.exe開啟的，就跟著把影片的路徑作為arg送到python
    if(argc >=2){
        cmd= cmd+ " \""+ argv[1]+ "\"";
    }
    cout << cmd << endl;
    
    system(cmd.c_str());
    
    return EXIT_SUCCESS;
}