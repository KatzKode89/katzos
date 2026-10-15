; katzos_minimal.iss — MINIMAL INSTALLER
[Setup]
AppName=KatzOS-Prime v1.3 GLITCH-PRIME
AppVersion=1.3.1
DefaultDirName={pf}\KatzOS-Prime
OutputDir=.
OutputBaseFilename=KatzOS-Prime-Setup
Compression=lzma
SolidCompression=yes
PrivilegesRequired=admin
WizardStyle=modern

[Files]
Source: "katzos_launch_FINAL.bat"; DestDir: "{app}"
Source: "launch.sh"; DestDir: "{app}"
Source: "README.txt"; DestDir: "{app}"

[Icons]
Name: "{group}\Launch KatzOS"; Filename: "{app}\katzos_launch_FINAL.bat"
Name: "{commondesktop}\KatzOS-Prime"; Filename: "{app}\katzos_launch_FINAL.bat"

[Run]
Filename: "{app}\katzos_launch_FINAL.bat"; Flags: postinstall nowait shellexec; Description: "Launch KatzOS-Prime NOW"
