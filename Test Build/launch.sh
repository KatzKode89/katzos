#!/bin/bash
# launch.sh — RUN THIS INSIDE WSL: wsl -d KatzOS-Prime-WSL2 then bash launch.sh
set -x
pkill -f nats-server; pkill -f katz_prime; sleep 1
mkdir -p ~/KatzOS/data
nats-server -js -p 4222 > ~/KatzOS/data/nats.log 2>&1 &
sleep 1
cd ~/KatzOS/tools
ls -lh katz_prime_master*.py
CORE=katz_prime_master_v1.3_glitch_prime.py
if [ ! -f $CORE ]; then CORE=$(ls katz_prime_master*.py | head -1); fi
echo "Using core: $CORE"
nohup ~/KatzOS/venv/bin/python $CORE > ~/KatzOS/data/sovereign.log 2>&1 &
sleep 4
cat ~/KatzOS/data/sovereign.log | tail -30
echo "--- HEALTH ---"
curl -s http://127.0.0.1:8000/health || echo "core starting, check log"
echo ""
echo "--- NATS LOG ---"
cat ~/KatzOS/data/nats.log | tail -10
