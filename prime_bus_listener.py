import asyncio
import json

async def listen_telemetry():
    reader, writer = await asyncio.open_connection('127.0.0.1', 4222)
    writer.write(b'CONNECT {"verbose":false,"pedantic":false,"user_agent":"KatzOS-Subscriber"}\r\n')
    writer.write(b'SUB katzos.telemetry.heartbeat 1\r\n')
    await writer.drain()

    print("[KATZOS-LISTENER] Listening for PrimeBus telemetry streams...")
    while True:
        line = await reader.readline()
        if not line:
            break
        decoded = line.decode().strip()
        if decoded.startswith('MSG'):
            payload_header = await reader.readline()
            print(f"[TELEMETRY RECEIVED]: {payload_header.decode().strip()}")

if __name__ == "__main__":
    asyncio.run(listen_telemetry())
