; KatzOS-Prime v1.3 GLITCH-PRIME — Inno Setup Installer
; Build with: iscc.exe katzos_prime_inno.iss

#define MyAppName "KatzOS-Prime v1.3 GLITCH-PRIME"
#define MyAppVersion "1.3.1"
#define MyAppPublisher "KatzOS / Mystivia89"

[Setup]
AppId={{KATZOS-PRIME-GLITCH-1.3}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\KatzOS-Prime
DefaultGroupName=KatzOS-Prime
OutputDir=.
OutputBaseFilename=KatzOS-Prime-v1.3-GLITCH-PRIME-Setup
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
UninstallDisplayIcon={app}\katzos_launch_FINAL.bat

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "launchHUD"; Description: "Launch KatzOS HUD after install"; GroupDescription: "Launch:"; Flags: checkedonce

[Files]
Source: "katzos_launch_FINAL.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "launch.sh"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.txt"; DestDir: "{app}"; Flags: ignoreversion isreadme

[Icons]
Name: "{autoprograms}\{#MyAppName}\KatzOS Launch"; Filename: "{app}\katzos_launch_FINAL.bat"; WorkingDir: "{app}"
Name: "{autodesktop}\KatzOS-Prime HUD"; Filename: "{app}\katzos_launch_FINAL.bat"; Tasks: desktopicon; WorkingDir: "{app}"

[Run]
Filename: "wsl.exe"; Parameters: "--list --verbose"; Flags: postinstall shellexec waituntilterminated
Filename: "{app}\katzos_launch_FINAL.bat"; Description: "Launch KatzOS-Prime Core + HUD"; Flags: postinstall nowait shellexec skipifsilent; Tasks: launchHUD
Filename: "http://127.0.0.1:8000/hud"; Description: "Open HUD"; Flags: postinstall shellexec nowait skipifsilent; Tasks: launchHUD

[Code]
procedure CurStepChanged(CurStep: TSetupStep);
var
  ResultCode: Integer;
begin
  if CurStep = ssPostInstall then
  begin
    Exec('wsl.exe', '-d KatzOS-Prime-WSL2 bash -c "pkill -f nats-server; pkill -f katz_prime; sleep 1"', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
    Exec('wsl.exe', '-d KatzOS-Prime-WSL2 bash -c "mkdir -p ~/KatzOS/data; nats-server -js -p 4222 > ~/KatzOS/data/nats.log 2>&1 & sleep 1; cd ~/KatzOS/tools; CORE=katz_prime_master_v1.3_glitch_prime.py; if [ ! -f $CORE ]; then CORE=katz_prime_master.py; fi; nohup ~/KatzOS/venv/bin/python $CORE > ~/KatzOS/data/sovereign.log 2>&1 &"', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
  end;
end;
