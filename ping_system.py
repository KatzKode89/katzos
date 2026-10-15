import urllib.request, json, time

def ping_metagirl():
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "metagirl",
        "prompt": "Run diagnostic check: Report system status, RTX 5060 VRAM load, and PrimeBus telemetry.",
        "stream": False
    }
    req = urllib.request.Request(
        url, 
        data=json.dumps(payload).encode('utf-8'), 
        headers={'Content-Type': 'application/json'}
    )
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            print(f"[METAGIRL TELEMETRY]:\n{result.get('response')}\n")
    except Exception as e:
        print(f"[ERROR] PrimeBus telemetry connection failed: {e}")

if __name__ == "__main__":
    ping_metagirl()
