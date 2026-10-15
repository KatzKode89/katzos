import asyncio, argparse, time
import nats

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bpm", type=int, default=135)
    parser.add_argument("--port", type=int, default=4222)
    parser.add_argument("--visualizer", type=str, default="waveshape")
    args = parser.parse_args()

    nc = await nats.connect(f"nats://127.0.0.1:{args.port}")
    print(f"[KATZ-OMNI] Audio pump active @ {args.bpm} BPM on NATS port {args.port} [Visualizer: {args.visualizer}]")
    
    beat_interval = 60.0 / args.bpm
    try:
        while True:
            payload = f'{{"bpm": {args.bpm}, "visualizer": "{args.visualizer}", "timestamp": {time.time()}}}'.encode('utf-8')
            await nc.publish("KATZOS_SOVEREIGN_AUDIO_V1.pump", payload)
            await asyncio.sleep(beat_interval)
    except asyncio.CancelledError:
        pass
    finally:
        await nc.drain()

if __name__ == "__main__":
    asyncio.run(main())
