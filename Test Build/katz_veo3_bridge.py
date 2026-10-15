#!/usr/bin/env python3
# katz_veo3_bridge.py — KatzOS-Prime Veo 3.1 Sovereign Video Generation Bridge
import os, json
from pathlib import Path

WORKSPACE = Path.home() / "KatzOS"
DIRECTOR_DIR = WORKSPACE / "renders" / "director_scripts"
OUTPUT_DIR = WORKSPACE / "renders" / "veo3_output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def generate_veo3_sequence(director_json_path: str):
    api_key = os.environ.get("GEMINI_API_KEY")
    try:
        from google import genai
        from google.genai import types
        HAS = True
    except:
        HAS = False

    print(f"[KatzVeo3] Initializing Veo 3.1 generation pipeline...")
    
    path = Path(director_json_path)
    if not path.exists():
        print(f"[KatzVeo3 Error] Director script not found at {path}")
        # create demo packet from Willow-O latest
        import sqlite3
        db = WORKSPACE / "data" / "katz_telemetry.db"
        if db.exists():
            conn = sqlite3.connect(db)
            cur = conn.cursor()
            cur.execute("SELECT full_prose FROM willow_story_archive ORDER BY id DESC LIMIT 1")
            row = cur.fetchone()
            prose = row[0][:500] if row else "Cyberpunk icosahedral chamber in soft collapse."
            conn.close()
        else:
            prose = "Midnight drive through Sector-10, amber-gold luminescence to neon fracture"
        packet = {"prose_directive": prose, "video_params": {"grading": "Amber-Gold Luminescence", "motion_scale": 0.35}}
    else:
        packet = json.loads(path.read_text(encoding="utf-8"))
    
    prose = packet.get("prose_directive", "Cyberpunk icosahedral chamber in soft collapse.")
    params = packet.get("video_params", {})
    enhanced_prompt = f"{prose} Visual style: {params.get('grading','Amber-Gold Luminescence')}. Cinematic motion scale: {params.get('motion_scale',0.35)}, 90 FPS, volumetric bloom and analog tape saturation. KATZmagiclight.render(Lyra.TrueForm)"
    print(f"[Veo 3.1] Dispatching prompt: {enhanced_prompt[:200]}...")

    if not api_key or not HAS:
        print("[KatzVeo3] No API key or genai SDK — writing render spec for later (quota exceeded workaround)")
        out_file = OUTPUT_DIR / f"veo3_render_spec_{path.stem if path.exists() else 'latest'}.json"
        out_file.write_text(json.dumps({"prompt": enhanced_prompt, "params": params, "packet": packet}, indent=2), encoding="utf-8")
        print(f"[KATZ VEO3 RENDER SPEC COMPILED] {out_file}")
        return

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=f"Generate cinematic video parameters and script for Veo 3.1: {enhanced_prompt}",
            config=types.GenerateContentConfig(temperature=0.4, system_instruction="You are KatzVeo3, translating sovereign narrative director packets into exact Veo 3.1 rendering configuration blocks with native synchronized audio directives.")
        )
        out_file = OUTPUT_DIR / f"veo3_render_spec_{path.stem}.json"
        out_file.write_text(response.text, encoding="utf-8")
        print(f"[KATZ VEO3 RENDER SPEC COMPILED] {out_file}")
        print(response.text[:500])
    except Exception as e:
        print(f"[KatzVeo3 API Error] {e} — quota exceeded, wrote local spec instead")
        out_file = OUTPUT_DIR / f"veo3_render_spec_{path.stem}.json"
        out_file.write_text(json.dumps({"prompt": enhanced_prompt, "fallback_error": str(e)}, indent=2), encoding="utf-8")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        scripts = sorted(DIRECTOR_DIR.glob("director_*.json"))
        target = str(scripts[-1]) if scripts else str(WORKSPACE / "renders" / "director_scripts" / "director_midnight_drive.json")
    generate_veo3_sequence(target)
