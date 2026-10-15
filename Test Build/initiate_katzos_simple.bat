@echo off
REM initiate_katzos_simple.bat — BULLETPROOF .bat — no PowerShell parsing issues
echo === KATZOS-PRIME v1.3 GLITCH-PRIME INITIATE BAT ===
echo [1] WSL list
wsl --list --verbose

echo [2] Kill old
wsl -d KatzOS-Prime-WSL2 bash -c "pkill -f nats-server; pkill -f katz_prime; sleep 1"

echo [3] Start NATS
wsl -d KatzOS-Prime-WSL2 bash -c "mkdir -p ~/KatzOS/data; nats-server -js -p 4222 > ~/KatzOS/data/nats.log 2>&1 & echo started"

echo [4] Start Core
wsl -d KatzOS-Prime-WSL2 bash -c "cd ~/KatzOS/tools; CORE=katz_prime_master_v1.3_glitch_prime.py; if [ ! -f $CORE ]; then CORE=katz_prime_master.py; fi; nohup ~/KatzOS/venv/bin/python $CORE > ~/KatzOS/data/sovereign.log 2>&1 & sleep 3; cat ~/KatzOS/data/sovereign.log | tail -20"

echo [5] Start Drumpad
wsl -d KatzOS-Prime-WSL2 bash -c "python3 -m http.server 8082 --directory ~/KatzOS/KatzDrumpadHolo > ~/KatzOS/data/drumpad.log 2>&1 & echo drumpad 8082"

echo [6] Health
wsl -d KatzOS-Prime-WSL2 bash -c "sleep 2; curl -s http://127.0.0.1:8000/health"

echo [7] Opening HUDs
start http://127.0.0.1:8000/hud
start http://127.0.0.1:8000/health
start http://127.0.0.1:8000/eris_exploits
start http://127.0.0.1:8082

echo === DONE — wsl -d KatzOS-Prime-WSL2 then curl http://127.0.0.1:8000/health ===
pause
