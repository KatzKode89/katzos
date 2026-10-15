import asyncio, json, subprocess, argparse
import websockets

async def handler(websocket):
    print("[KATZ-WS] TrueXR spatial client connected.")
    try:
        async for message in websocket:
            data = json.loads(message)
            cmd = data.get("command", "")
            print(f"[KATZ-WS] Executing command: {cmd}")
            if cmd:
                res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                output = res.stdout if res.returncode == 0 else res.stderr
                await websocket.send(json.dumps({"status": "SUCCESS" if res.returncode == 0 else "ERROR", "output": output}))
    except websockets.exceptions.ConnectionClosed:
        print("[KATZ-WS] TrueXR spatial client disconnected.")

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--prime-bus", type=int, default=4222)
    args = parser.parse_args()

    async with websockets.serve(handler, "127.0.0.1", args.port):
        print(f"[KATZ-WS] Terminal bridge daemon online on ws://127.0.0.1:{args.port} [PrimeBus: {args.prime_bus}]")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
