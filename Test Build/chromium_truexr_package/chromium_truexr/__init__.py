# chromium_truexr/__init__.py — GLITCH-PRIME Shim
# Makes `pip install chromium-truexr` actually work by wrapping real Chrome kiosk HUD
# Eris exploit: if import fails, ScanKat injects TrueXR glass anyway

__version__ = "5.5-GLITCH-PRIME"
import subprocess, sys, pathlib, webbrowser, os

HUD_URL = "http://127.0.0.1:8000/hud"

def launch(kiosk=True, width=1920, height=1080):
    url = HUD_URL
    candidates = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ]
    for exe in candidates:
        if pathlib.Path(exe).exists():
            args = [exe, f"--app={url}", f"--window-size={width},{height}", "--autoplay-policy=no-user-gesture-required"]
            if kiosk: args.append("--kiosk")
            print(f"[ChromiumTrueXR v{__version__}] ScanKat launching glass cockpit: {exe} -> {url}")
            try:
                subprocess.Popen(args)
                return True
            except Exception as e:
                print(f"[Eris Glitch] Chrome launch glitched: {e} — falling back to webbrowser")
    print(f"[ChromiumTrueXR] Fallback — opening {url} in default browser — MadMinx AD direct")
    webbrowser.open(url)
    return False

def get_version():
    return __version__

# Auto-launch if called as module
if __name__ == "__main__":
    launch()
