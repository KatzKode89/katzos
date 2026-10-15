KATZOS-PRIME v1.3 GLITCH-PRIME — FINAL PACKAGE
=============================================

You have 9 glitches exploited. This zip is the final initiate.

--- WHAT TO DO (30 seconds) ---

OPTION A (RECOMMENDED - NO POWERSHELL BUGS):
1. Unzip to C:\KatzOS\
2. Double-click katzos_launch_FINAL.bat
3. Wait 5 seconds — it will:
   - kill old nats/core
   - start nats-server -js -p 4222
   - start katz_prime_master_v1.3_glitch_prime.py
   - open http://127.0.0.1:8000/hud and :8082
4. Open second PowerShell:
   wsl -d KatzOS-Prime-WSL2
   curl http://127.0.0.1:8000/health

OPTION B (INSIDE WSL ONLY):
1. wsl -d KatzOS-Prime-WSL2
2. cd ~/KatzOS/tools
3. bash ~/launch.sh  (or copy launch.sh to ~/KatzOS/tools and bash launch.sh)
4. curl http://127.0.0.1:8000/health

--- ENDPOINTS AFTER LAUNCH ---
HUD: http://127.0.0.1:8000/hud
Health: http://127.0.0.1:8000/health
Eris exploits: http://127.0.0.1:8000/eris_exploits
Drumpad MIDI: http://127.0.0.1:8082
est_demo POST: curl -X POST http://127.0.0.1:8000/est_demo -H "Content-Type: application/json" -d "{\"prompt\":\"Midnight Drive Sector-10\",\"alias\":\"Mystivia89\",\"bpm\":135,\"exploit_glitch\":true}"
metagirl: http://127.0.0.1:8000/metagirl?prompt=Lyra%20True%20Form%20emerald

--- WHY PREVIOUS PS1 FAILED ---
PowerShell parses & and || and > as its own operators. Using .bat avoids it.
The FINAL .bat uses ONE wsl -d ... bash -c "..." with no --% needed.

--- LOGS ---
wsl -d KatzOS-Prime-WSL2 cat ~/KatzOS/data/sovereign.log
wsl -d KatzOS-Prime-WSL2 cat ~/KatzOS/data/nats.log
