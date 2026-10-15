# initiate_katzos_simple.ps1 — BULLETPROOF — uses --% to stop PowerShell parsing bash
Write-Host "=== KATZOS-PRIME v1.3 GLITCH-PRIME — INITIATE ===" -ForegroundColor Cyan

Write-Host "[1] WSL list" -ForegroundColor Green
wsl --list --verbose

Write-Host "[2] Kill old" -ForegroundColor Green
wsl -d KatzOS-Prime-WSL2 --% bash -c "pkill -f nats-server; pkill -f katz_prime; sleep 1"

Write-Host "[3] Start NATS" -ForegroundColor Green
wsl -d KatzOS-Prime-WSL2 --% bash -c "mkdir -p ~/KatzOS/data; nats-server -js -p 4222 > ~/KatzOS/data/nats.log 2>&1 & echo started"

Write-Host "[4] Start Sovereign Core" -ForegroundColor Green
wsl -d KatzOS-Prime-WSL2 --% bash -c "cd ~/KatzOS/tools; CORE=katz_prime_master_v1.3_glitch_prime.py; if [ ! -f $CORE ]; then CORE=katz_prime_master.py; fi; nohup ~/KatzOS/venv/bin/python $CORE > ~/KatzOS/data/sovereign.log 2>&1 & sleep 3; cat ~/KatzOS/data/sovereign.log | tail -20"

Write-Host "[5] Start Drumpad web" -ForegroundColor Green
wsl -d KatzOS-Prime-WSL2 --% bash -c "python3 -m http.server 8082 --directory ~/KatzOS/KatzDrumpadHolo > ~/KatzOS/data/drumpad.log 2>&1 & echo drumpad 8082"

Write-Host "[6] Health" -ForegroundColor Green
wsl -d KatzOS-Prime-WSL2 --% bash -c "sleep 2; curl -s http://127.0.0.1:8000/health"

Write-Host "[7] Opening HUDs" -ForegroundColor Green
Start-Process "http://127.0.0.1:8000/hud"
Start-Process "http://127.0.0.1:8000/health"
Start-Process "http://127.0.0.1:8000/eris_exploits"
Start-Process "http://127.0.0.1:8082"

Write-Host "=== DONE ===" -ForegroundColor Cyan
Write-Host "NOW: wsl -d KatzOS-Prime-WSL2" -ForegroundColor Yellow
Write-Host "THEN: curl http://127.0.0.1:8000/health" -ForegroundColor Yellow
Pause
