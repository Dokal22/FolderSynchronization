# 폴더 동기화 Folder Synchronization

## Installation

:warning: 파이썬이 설치되어있어야 합니다!! (버전은 몰루. 난 3.12)
:warning: Python must be installed!!

```powershell
pip install watchdog
```

watchdog 라이브러리가 필요합니다.

```powershell
git clone https://github.com/Dokal22/FolderSynchronization.git
```

원하는 경로에서 입력하세용
Download it

```json
{
  "pathA": "D:\\원하는\\경로\\~~",
  "pathB": "C:\\원하는\\경로\\~~"
}
```

`define.json.example`을 `define.json`로 바꾸고 작업하는 경로와 복사될 경로를 세팅하구요
Replace `define.json.example` with `define.json`. And set the path to work and the path to be copied

## Usage

거냥 `execute.bat` 실행시키믄 댑니다
You just have to run `execute.bat`

끄려면 ctrl + C 하고 Y 누르면 돼요

파이썬 설치? 그런거 모른다
https://github.com/BornToBeRoot/PowerShell_SyncFolder