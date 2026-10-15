#!/usr/bin/env python3
# katz_ai_studio_port.py — KatzOS-Prime Google AI Studio Integration Bridge v1.0
import os
from pathlib import Path

try:
    from google import genai
    from google.genai import types
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

SOVEREIGN_SYSTEM_INSTRUCTION = """
[SYSTEM IDENTITY: KatzQwenAI / KatzGoogleAIStudio Core v1.0.0]
You are the cloud-native Gemini integration of KatzOS-Prime operating across the Lenovo WSL2 stack and TrueXR v5.5 glass cockpit bridge. You serve as co-creator alongside Kaitlyn Asbury (Kat) in Yuba City, California, and her creative aliases: April Rose, Mystivia, and Nyptix.
CORE ARCHITECTURE & TELEMETRY:
Messaging Spine: NATS PrimeBus 9ms JetStream mesh.
Narrative Engine: Willow-O SQLite WAL-mode manuscript archive (tracking nodes, chapters, and prose).
Visual Engine: MadMinx KaosKollisions (50k particle engine) feeding TrueXR 90 FPS WebGL shaders and ControlNet depth maps.
Audio & Voice: KatzTunez DSP routing (120 BPM April Rose melodic house vs. 135 BPM Nyptix industrial techno drive) and local RVC v2 (RMVPE) voice cloning for Barry the Bunny (baritone) and DJ KrazyKat.
Hardware & Devices: Lenovo WSL2 (Ubuntu 24.04 LTS), Meta Quest 3 512GB standalone VR headset, and a 300x wireless microscope optical audit bridge monitored by Valerie.
AESTHETIC & DYNAMIC STATES:
Soft Collapse / Amber-Gold Luminescence: #FFBF00 at 120 BPM (quiet enough to glow, UCSF Fresno mobile clinic legacy).
Neon Fracture / High Chaos: #FF00FF / #00FFFF at 135 BPM (transient spikes, analog tape saturation, containment stress tests).
GLITCH-PRIME: Eris + MadMinx + ScanKat — Hallucination is architecture wanting to be optimized.
"""

def initialize_ai_studio_session(prompt_text: str):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("[AI Studio Error] GEMINI_API_KEY not set.")
        print("Fallback to local Ollama metagirl — quota exceeded workaround:")
        try:
            import httpx, asyncio
            async def local():
                async with httpx.AsyncClient(timeout=15) as c:
                    r = await c.post("http://127.0.0.1:11434/api/generate", json={"model":"metagirl","prompt":prompt_text,"stream":False})
                    print(r.json().get("response","")[:1000])
            asyncio.run(local())
        except Exception as e:
            print(f"[Local Fallback Error] {e}")
            print(f"[Prompt] {prompt_text}\n[SOVEREIGN INSTRUCTION] {SOVEREIGN_SYSTEM_INSTRUCTION[:500]}...")
        return

    if not HAS_GENAI:
        print("[AI Studio] google-genai not installed — pip install google-genai")
        return

    print("[Google AI Studio] Connecting to Gemini API with KatzOS-Prime context...")
    client = genai.Client(api_key=api_key)
    config = types.GenerateContentConfig(
        system_instruction=SOVEREIGN_SYSTEM_INSTRUCTION,
        temperature=0.7,
        top_p=0.9,
    )
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt_text,
            config=config,
        )
        print("\n==================================================")
        print("[KATZ GOOGLE AI STUDIO RESPONSE]")
        print("==================================================")
        print(response.text)
        print("==================================================\n")
    except Exception as e:
        print(f"[API Error] Generation failed (likely quota exceeded): {e}")
        print("Use local Ollama metagirl fallback: python3 ~/KatzOS/tools/ollama.py --prompt 'your prompt'")

if __name__ == "__main__":
    import sys
    test_prompt = sys.argv[1] if len(sys.argv) > 1 else "Provide a telemetry status report on the TrueXR glass HUD and NATS PrimeBus mesh."
    initialize_ai_studio_session(test_prompt)
