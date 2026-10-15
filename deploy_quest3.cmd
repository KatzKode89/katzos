@echo off
echo [ADAM-G] Checking Meta Quest 3 ADB connection...
adb devices

if exist .\dist\truexr-release.apk (
    echo [DEPLOY] Installing TrueXR release APK to Quest 3...
    adb install -r .\dist\truexr-release.apk
) else (
    echo [DEPLOY] Launching TrueXR native activity via PrimeBus port 4222...
    adb shell am start -n com.katzks.truexr/.MainActivity --es "prime_bus_port" "4222"
)
echo [ADAM-G] Hardware link sequence complete.
pause