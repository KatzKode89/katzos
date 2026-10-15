import psutil

print("[KATZOS-PROC] Scanning active sovereign processes...")
count = 0
for proc in psutil.process_iter(['pid', 'name']):
    try:
        name = proc.info['name']
        if name and ('python' in name.lower() or 'katzos' in name.lower()):
            print(f"  [PID: {proc.info['pid']}] {name}")
            count += 1
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass
print(f"[KATZOS-PROC] Total active sovereign nodes detected: {count}")
