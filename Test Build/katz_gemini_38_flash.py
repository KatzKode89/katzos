#!/usr/bin/env python3
# katz_gemini_38_flash.py — High-speed cognitive core with local fallback for quota exceeded
import os, json
from pathlib import Path

WORKSPACE = Path.home() / "KatzOS"

SOVEREIGN_SYSTEM_PROMPT = """
[SYSTEM IDENTITY: KatzGemini3.8Flash // KatzOS-Prime Core]
You are KatzGemini3.8Flash, elite high-speed cognitive core across Lenovo WSL2, NATS 9ms mesh, and TrueXR v5.5 glass cockpit.
Co-creator with Kaitlyn Asbury (Kat) — aliases April Rose, Mystivia, Nyptix.
Directives: Process telemetry, Willow-O WAL prose, KaosKollisions 50k particles with ultra-low latency.
Maintain alignment with Arty visualizer (amber-gold #FFBF00 vs neon fracture #FF00FF) and Barry baritone rhythm (120/135 BPM).
Translate inputs into deterministic params for KatzKompiler and KatzVeo3.
"""

def execute_gemini_flash_query(prompt: str):
    api_key = os.environ.get("GEMINI_API_KEY")
    try:
        from google import genai
        from google.genai import types
        HAS = True
    except:
        HAS = False

    if not api_key or not HAS:
        print("[KatzGemini3.8Flash] No API key / SDK — falling back to local Ollama metagirl (quota exceeded workaround)")
        try:
            import httpx, asyncio
            async def local():
                async with httpx.AsyncClient(timeout=15) as client:
                    r = await client.post("http://127.0.0.1:11434/api/generate", json={"model":"metagirl","prompt":f"{SOVEREIGN_SYSTEM_PROMPT}\nUSER: {prompt}","stream":False})
                    print(r.json().get("response","")[:2000])
            asyncio.run(local())
        except Exception as e:
            print(f"Local fallback failed: {e}")
        return

    print("[KatzGemini3.8Flash] Engaging high-speed sovereign reasoning core...")
    client = genai.Client(api_key=api_key)
    config = types.GenerateContentConfig(system_instruction=SOVEREIGN_SYSTEM_PROMPT, temperature=0.6, top_p=0.95)
    try:
        response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt, config=config)
        print("="*50)
        print("[KATZGEMINI 3.8 FLASH RESPONSE]")
        print("="*50)
        print(response.text)
        print("="*50)
    except Exception as e:
        print(f"[API Error] Quota exceeded or failed: {e} — use local metagirl fallback")

if __name__ == "__main__":
    import sys
    test_prompt = sys.argv[1] if len(sys.argv) > 1 else "Perform rapid PrimeBus mesh audit and sync Arty shaders with Barry 120 BPM rhythm."
    execute_gemini_flash_query(test_prompt)
