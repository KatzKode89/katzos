import asyncio, json, os
import nats

async def tavus_bridge():
    nc = await nats.connect("nats://127.0.0.1:4222")
    print("[KATZ-TAVUS-BRIDGE] Initialized spatial crew video/audio telemetry stream on port 4222.")

    async def handler(msg):
        data = json.loads(msg.data.decode())
        print(f"[KATZ-TAVUS] Received crew frame update: {data.get('status', 'SYNC')}")

    await nc.subscribe("KATZOS_SOVEREIGN_AUDIO_V1.tavus", cb=handler)

    try:
        while True:
            payload = json.dumps({"status": "ACTIVE", "bridge": "tavus.io/pal-maker", "bpm": 135}).encode()
            await nc.publish("KATZOS_SOVEREIGN_AUDIO_V1.tavus", payload)
            await asyncio.sleep(5)
    except asyncio.CancelledError:
        pass
    finally:
        await nc.drain()

if __name__ == "__main__":
    asyncio.run(tavus_bridge())
