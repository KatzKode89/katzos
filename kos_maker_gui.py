import sys
import os
import json
import threading
import http.server
import socketserver
import webbrowser

PORT = 8090
DIRECTORY = "C:\\KatzOS"

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <title>KOS-Maker // Sovereign Project Scaffolder</title>
    <style>
        body { background: #0b0f19; color: #00ffcc; font-family: monospace; margin: 0; padding: 30px; }
        h1 { letter-spacing: 2px; text-shadow: 0 0 15px rgba(0,255,204,0.5); text-align: center; }
        .container { max-width: 800px; margin: 0 auto; background: #161b22; border: 2px solid #30363d; border-radius: 10px; padding: 25px; box-shadow: 0 0 20px rgba(0,0,0,0.8); }
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 8px; color: #8b949e; font-weight: bold; }
        input, select, textarea { width: 100%; padding: 10px; background: #0b0f19; border: 1px solid #30363d; color: #00ffcc; font-family: monospace; border-radius: 6px; box-sizing: border-box; }
        button { background: #238636; color: white; border: none; padding: 12px 20px; font-size: 16px; border-radius: 6px; cursor: pointer; font-family: monospace; font-weight: bold; width: 100%; box-shadow: 0 0 10px rgba(35,134,54,0.4); }
        button:hover { background: #2ea043; }
        #log { background: #0b0f19; border: 1px solid #30363d; padding: 15px; height: 200px; overflow-y: auto; color: #8b949e; font-size: 13px; margin-top: 20px; border-radius: 6px; white-space: pre-wrap; }
    </style>
</head>
<body>
    <h1>KOS-MAKER // SOVEREIGN GENERATOR</h1>
    <div class='container'>
        <div class='form-group'>
            <label>Project Name:</label>
            <input type='text' id='projName' value='CrystalSeekers_Module_01'>
        </div>
        <div class='form-group'>
            <label>Architecture Target:</label>
            <select id='projType'>
                <option value='katzos_app'>KatzOS Sovereign App Module</option>
                <option value='crystalseekers_game'>CrystalSeekers Unity/Godot Asset Package</option>
                <option value='katztunez_synth'>KatzTunez 135 BPM Audio Plugin</option>
                <option value='truexr_hud'>TrueXR 90 FPS Spatial HUD Overlay</option>
            </select>
        </div>
        <div class='form-group'>
            <label>PrimeBus Telemetry Hook:</label>
            <input type='text' id='primeBus' value='KATZOS_SOVEREIGN_AUDIO_V1.>'>
        </div>
        <button onclick='scaffoldProject()'>INITIALIZE SCAFFOLD SEQUENCE</button>

        <div class='form-group' style='margin-top: 25px;'>
            <label>PrimeBus Execution Log:</label>
            <div id='log'>[SYSTEM READY] Awaiting scaffold command...</div>
        </div>
    </div>

    <script>
        function scaffoldProject() {
            const name = document.getElementById('projName').value;
            const type = document.getElementById('projType').value;
            const bus = document.getElementById('primeBus').value;
            const log = document.getElementById('log');

            log.innerText += \n[INFO] Initializing generation for  [Type: ]...;

            fetch('/api/scaffold', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name: name, type: type, bus: bus })
            })
            .then(res => res.json())
            .then(data => {
                log.innerText += \n[SUCCESS] \n[PATH] ;
                log.scrollTop = log.scrollHeight;
            })
            .catch(err => {
                log.innerText += \n[ERROR] Scaffolding failed: ;
                log.scrollTop = log.scrollHeight;
            });
        }
    </script>
</body>
</html>
"""

class KOSHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(HTML_TEMPLATE.encode('utf-8'))
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/api/scaffold':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            proj_name = data.get('name', 'NewProject')
            proj_type = data.get('type', 'katzos_app')

            target_dir = os.path.join("C:\\KatzOS", proj_name)
            os.makedirs(target_dir, exist_ok=True)

            manifest = {
                "project": proj_name,
                "type": proj_type,
                "prime_bus": data.get('bus'),
                "vram_lock": True,
                "author": "Kaitlyn Asbury (KatzKode89)"
            }

            with open(os.path.join(target_dir, "kos_manifest.json"), "w") as f:
                json.dump(manifest, f, indent=4)

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = {
                "status": "compiled",
                "message": f"Successfully generated {proj_name} framework.",
                "path": target_dir
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))

def run_server():
    os.chdir(DIRECTORY)
    with socketserver.TCPServer(("", PORT), KOSHandler) as httpd:
        print(f"[KOS-MAKER GUI] Active at http://localhost:{PORT}")
        httpd.serve_forever()

if __name__ == '__main__':
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    webbrowser.open(f"http://localhost:{PORT}")
    server_thread.join()
