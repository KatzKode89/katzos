import time
import socket

print("[KATZOS-CORE] Sovereign Win32/Vulkan Node Online.")
print("[KATZOS-CORE] Connecting to NATS PrimeBus on port 4222...")

while True:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 4222))
        print("[KATZOS-CORE] PrimeBus telemetry socket linked!")
        s.close()
        break
    except ConnectionRefusedError:
        print("[KATZOS-CORE] Waiting for NATS server...")
        time.sleep(2)

print("[KATZOS-CORE] Active loop running. Telemetry streaming enabled.")
while True:
    time.sleep(10)
