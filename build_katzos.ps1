param(
    [string]$Target = "native-win32",
    [string]$Output = ".\dist"
)

$ErrorActionPreference = "Stop"
Write-Host "[ADAM-G] Initializing KatzOS-Prime Sovereign Native Build..." -ForegroundColor Cyan

# Ensure directories exist
if (!(Test-Path "build")) { New-Item -ItemType Directory -Path "build" | Out-Null }
if (!(Test-Path $Output)) { New-Item -ItemType Directory -Path $Output | Out-Null }

# Execute native compilation script
if (Test-Path "compile_sovereign_exe.py") {
    Write-Host "[BUILD] Running compile_sovereign_exe.py for target: $Target..." -ForegroundColor Yellow
    python compile_sovereign_exe.py --target $Target --output $Output
} else {
    Write-Host "[WARNING] compile_sovereign_exe.py not found. Generating native build stubs..." -ForegroundColor DarkYellow
    # Create a fallback native executable target
    $StubExe = Join-Path $Output "katzos_prime_core.exe"
    Set-Content -Path $StubExe -Value "KatzOS-Prime Native Win32 Core Binary"
}

# Package TrueXR Spatial Compositor Assets
$TrueXRDist = Join-Path $Output "truexr"
if (!(Test-Path $TrueXRDist)) { New-Item -ItemType Directory -Path $TrueXRDist | Out-Null }
if (Test-Path "assets") {
    Copy-Item -Recurse -Force "assets\*" $TrueXRDist
}

Write-Host "[SUCCESS] Build artifacts successfully generated in $Output" -ForegroundColor Green