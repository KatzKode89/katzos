import time
import os
import shutil

SOURCE = "C:\\KatzOS\\CrystalSeekers_Narrative_Engine_V1"
TARGET = "C:\\KatzOS\\CrystalSeekers\\Assets\\KatzOS\\Core\\Architecture"

print(f"[PRIMEBUS WATCHER] Monitoring {SOURCE} for CrystalSeekers narrative updates...")
while True:
    if os.path.exists(SOURCE):
        os.makedirs(TARGET, exist_ok=True)
        for item in os.listdir(SOURCE):
            s = os.path.join(SOURCE, item)
            d = os.path.join(TARGET, item)
            if os.path.isfile(s) and not os.path.exists(d):
                shutil.copy2(s, d)
                print(f"[SYNCED] Transferred {item} to Unity/Godot asset pipeline.")
    time.sleep(5)
