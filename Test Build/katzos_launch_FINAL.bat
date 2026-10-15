@echo off
REM katzos_launch_FINAL.bat — DOUBLE CLICK THIS, NO POWERSHELL NEEDED
echo === KATZOS-PRIME FINAL LAUNCH .BAT ===

echo [1] Checking WSL...
wsl --list --verbose

echo [2] Entering WSL and launching everything...
wsl -d KatzOS-Prime-WSL2 bash -c "pkill -f nats-server; pkill -f katz_prime; sleep 1; mkdir -p ~/KatzOS/data; nats-server -js -p 4222 > ~/KatzOS/data/nats.log 2>&1 & sleep 1; cd ~/KatzOS/tools; ls katz_prime_master*.py; CORE=katz_prime_master_v1.3_glitch_prime.py; if [ ! -f $CORE ]; then CORE=katz_prime_master.py; fi; nohup ~/KatzOS/venv/bin/python $CORE > ~/KatzOS/data/sovereign.log 2>&1 & sleep 4; cat ~/KatzOS/data/sovereign.log | tail -20; echo ---HEALTH---; curl -s http://127.0.0.1:8000/health"

echo [3] Opening HUDs...
start http://127.0.0.1:8000/hud
start http://127.0.0.1:8000/health
start http://127.0.0.1:8000/eris_exploits
start http://127.0.0.1:8082

echo DONE
pause
