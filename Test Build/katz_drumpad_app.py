#!/usr/bin/env python3
# katz_drumpad_app.py — KatzDrumpadHolo Multi-Touch + Web MIDI + Holo-Reactive Visualizer — v2 MIDI
import pathlib
WORKSPACE = pathlib.Path.home() / "KatzOS"
APP_DIR = WORKSPACE / "KatzDrumpadHolo"
APP_DIR.mkdir(parents=True, exist_ok=True)

def generate_drumpad_app():
    print("[KatzDrumpadHolo] Scaffolding v2 — Multi-Touch + Web MIDI + Holo-Reactive Visualizer...")
    app_html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
<title>KatzDrumpadHolo v2 // Web MIDI + Holo</title>
<style>
* { box-sizing: border-box; user-select: none; }
body { margin:0; background:#050508; color:#00ffff; font-family:'Courier New', monospace; height:100vh; overflow:hidden; display:flex; flex-direction:column; }
header { background: rgba(0,20,30,0.95); border-bottom:1px solid #00ffff; padding:10px 14px; display:flex; justify-content:space-between; align-items:center; z-index:10; flex-wrap:wrap; gap:8px; }
h1 { margin:0; font-size:14px; color:#ffbf00; letter-spacing:1px; }
.badge { font-size:10px; padding:4px 8px; border:1px solid #ffbf00; border-radius:4px; color:#ffbf00; }
.controls { display:flex; gap:8px; align-items:center; font-size:10px; }
select, button { background:#000; border:1px solid #00ffff; color:#fff; padding:6px 8px; border-radius:4px; font-family:monospace; font-size:10px; cursor:pointer; }
button { background:#00ffff; color:#000; font-weight:bold; }
#canvas-container { position:absolute; top:0; left:0; width:100%; height:100%; z-index:1; pointer-events:none; }
.main-stage { flex:1; position:relative; z-index:5; display:grid; grid-template-columns:repeat(4,1fr); grid-template-rows:repeat(4,1fr); gap:10px; padding:14px; max-width:650px; margin:auto; width:100%; max-height:650px; }
.pad { background: rgba(0,255,255,0.05); border:2px solid rgba(0,255,255,0.4); border-radius:12px; display:flex; flex-direction:column; justify-content:center; align-items:center; cursor:pointer; transition: transform 0.05s, background 0.05s, border-color 0.05s; box-shadow: inset 0 0 15px rgba(0,255,255,0.1); position:relative; }
.pad span { font-size:10px; color: rgba(255,255,255,0.6); margin-top:4px; text-align:center; }
.pad strong { font-size:12px; }
.pad.active { background: rgba(255,191,0,0.35); border-color:#ffbf00; transform:scale(0.94); box-shadow:0 0 25px #ffbf00; }
.pad.midi-learn { border-color:#FF00FF; box-shadow:0 0 20px #FF00FF; animation: pulse 0.8s infinite; }
@keyframes pulse { 0%{opacity:1} 50%{opacity:0.5} 100%{opacity:1} }
.pad .midi-tag { position:absolute; top:4px; right:6px; font-size:8px; background:#FF00FF; color:#fff; padding:1px 4px; border-radius:3px; display:none; }
.pad.has-midi .midi-tag { display:block; }
footer { background: rgba(0,20,30,0.95); border-top:1px solid #00ffff; padding:8px 14px; display:flex; justify-content:space-between; align-items:center; z-index:10; font-size:10px; flex-wrap:wrap; gap:6px; }
#log { max-height:60px; overflow-y:auto; font-size:9px; color:#00ffcc; }
</style>
</head>
<body>
<header>
<h1>KATZDRUMPADHOLO v2 // MIDI + HOLO-REACTIVE</h1>
<div class="controls">
<label>MIDI In:</label>
<select id="midiInSelect"><option>— no MIDI —</option></select>
<button id="learnBtn">MIDI LEARN</button>
<span id="modeBadge" class="badge">120 BPM // AMBER-GOLD</span>
</div>
</header>
<div id="canvas-container"><canvas id="holoCanvas"></canvas></div>
<div class="main-stage" id="padGrid"></div>
<footer>
<div><span>Engine: KatzTunez-HybridAISynth | </span><span id="midiStatus">MIDI: checking...</span></div>
<div id="log"></div>
<div><span style="color:#ffbf00;">PrimeBus 9ms Linked | Velocity: <span id="vel">—</span></span></div>
</footer>
<script>
const AudioContext = window.AudioContext || window.webkitAudioContext;
const audioCtx = new AudioContext();
const canvas = document.getElementById('holoCanvas');
const ctx = canvas.getContext('2d');
let width, height;
let particles = [];
let currentTheme = { color:'#ffbf00', bpm:120 };
let midiAccess = null;
let learnMode = false;
let learnTargetIndex = null;
let midiMap = JSON.parse(localStorage.getItem('katz_midi_map')||'{}'); // noteNumber -> padIndex
let reverseMap = {}; // padIndex -> noteNumber label
Object.keys(midiMap).forEach(n => reverseMap[midiMap[n]] = n);

function resize(){ width=canvas.width=window.innerWidth; height=canvas.height=window.innerHeight; }
window.addEventListener('resize', resize); resize();

class Particle {
  constructor(x,y,color,vel){ this.x=x; this.y=y; this.vx=(Math.random()-0.5)*8*vel; this.vy=(Math.random()-0.5)*8*vel; this.size=Math.random()*6+2+vel*2; this.color=color; this.life=1.0; }
  update(){ this.x+=this.vx; this.y+=this.vy; this.life-=0.018; }
  draw(){ ctx.save(); ctx.globalAlpha=Math.max(0,this.life); ctx.fillStyle=this.color; ctx.beginPath(); ctx.arc(this.x,this.y,this.size,0,Math.PI*2); ctx.fill(); ctx.restore(); }
}

function logMsg(m){
  const l=document.getElementById('log');
  l.innerHTML = `[${new Date().toLocaleTimeString()}] ${m}<br>` + l.innerHTML;
}

function triggerHoloBurst(x,y,isChaos,vel=1){
  const color = isChaos ? '#ff00ff' : '#ffbf00';
  currentTheme = isChaos ? {color:'#ff00ff', bpm:135} : {color:'#ffbf00', bpm:120};
  document.getElementById('modeBadge').innerText = `${currentTheme.bpm} BPM // ${isChaos?'NEON FRACTURE':'AMBER-GOLD'} | vel ${vel.toFixed(2)}`;
  document.getElementById('vel').innerText = vel.toFixed(2);
  const count = 15 + Math.floor(vel*25);
  for(let i=0;i<count;i++) particles.push(new Particle(x,y,color,vel));
}

function animate(){
  ctx.clearRect(0,0,width,height);
  ctx.strokeStyle='rgba(0,255,255,0.04)'; ctx.lineWidth=1;
  for(let x=0;x<width;x+=40){ ctx.beginPath(); ctx.moveTo(x,0); ctx.lineTo(x,height); ctx.stroke(); }
  for(let y=0;y<height;y+=40){ ctx.beginPath(); ctx.moveTo(0,y); ctx.lineTo(width,y); ctx.stroke(); }
  particles.forEach((p,i)=>{ p.update(); p.draw(); if(p.life<=0) particles.splice(i,1); });
  requestAnimationFrame(animate);
}
animate();

function playPadSound(index, velocity=1){
  if(audioCtx.state==='suspended') audioCtx.resume();
  const osc = audioCtx.createOscillator();
  const gain = audioCtx.createGain();
  const filter = audioCtx.createBiquadFilter();
  const frequencies = [110,123.47,130.81,146.83,164.81,174.61,196,220,246.94,261.63,293.66,329.63,349.23,392,440,523.25];
  osc.type = index>7 ? 'sawtooth' : 'sine';
  osc.frequency.setValueAtTime(frequencies[index]||220, audioCtx.currentTime);
  filter.type='lowpass'; filter.frequency.setValueAtTime(1200+velocity*3000, audioCtx.currentTime);
  const vol = 0.15 + velocity*0.35;
  gain.gain.setValueAtTime(vol, audioCtx.currentTime);
  gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime+0.5+velocity*0.4);
  osc.connect(filter); filter.connect(gain); gain.connect(audioCtx.destination);
  osc.start(); osc.stop(audioCtx.currentTime+0.6+velocity*0.4);
}

function triggerPad(index, velocity=1, x=null, y=null){
  const padEl = document.querySelectorAll('.pad')[index];
  if(!padEl) return;
  padEl.classList.add('active');
  playPadSound(index, velocity);
  const rect = padEl.getBoundingClientRect();
  const cx = x!==null?x:rect.left+rect.width/2;
  const cy = y!==null?y:rect.top+rect.height/2;
  triggerHoloBurst(cx,cy,index>=12,velocity);
  setTimeout(()=>padEl.classList.remove('active'), 120+velocity*80);
}

const padNames = ["BARRY_SUB","APRIL_PAD","NYPTIX_LEAD","REVERB_TAIL","KICK_808","SNARE_TR","HIHAT_CLS","HIHAT_OPT","VOICE_K","VOICE_B","CHORD_M1","CHORD_M2","FX_SWEEP","FX_GLITCH","CHAOS_UP","PRIME_SYNC"];
const grid=document.getElementById('padGrid');
padNames.forEach((name,i)=>{
  const pad=document.createElement('div');
  pad.className='pad';
  if(reverseMap[i]) pad.classList.add('has-midi');
  pad.innerHTML=`<div class='midi-tag'>MIDI ${reverseMap[i]||''}</div><strong>PAD ${i+1}</strong><span>${name}</span>`;
  const action=(e)=>{
    e.preventDefault();
    if(learnMode){
      learnTargetIndex=i;
      logMsg(`MIDI LEARN: Tap a key/pad on your hardware to bind to PAD ${i+1} ${name}...`);
      pad.classList.add('midi-learn');
      return;
    }
    triggerPad(i, 1);
  };
  pad.addEventListener('touchstart', action, {passive:false});
  pad.addEventListener('mousedown', action);
  grid.appendChild(pad);
});

document.getElementById('learnBtn').addEventListener('click', ()=>{
  learnMode=!learnMode;
  document.getElementById('learnBtn').innerText = learnMode?'EXIT LEARN':'MIDI LEARN';
  document.getElementById('learnBtn').style.background = learnMode?'#FF00FF':'#00ffff';
  if(!learnMode){
    document.querySelectorAll('.pad').forEach(p=>p.classList.remove('midi-learn'));
    learnTargetIndex=null;
    logMsg('Exited MIDI learn mode');
  } else {
    logMsg('MIDI LEARN active — click a pad then press hardware controller');
  }
});

// Web MIDI API
async function initMIDI(){
  if(!navigator.requestMIDIAccess){
    document.getElementById('midiStatus').innerText='MIDI: Web MIDI not supported — use Chrome/Edge';
    logMsg('Web MIDI API not supported in this browser. Use Chrome, Edge, or Opera.');
    return;
  }
  try{
    midiAccess = await navigator.requestMIDIAccess();
    document.getElementById('midiStatus').innerText='MIDI: ready — '+midiAccess.inputs.size+' input(s)';
    const select=document.getElementById('midiInSelect');
    select.innerHTML='';
    midiAccess.inputs.forEach(input=>{
      const opt=document.createElement('option');
      opt.value=input.id; opt.text=input.name;
      select.appendChild(opt);
      input.onmidimessage = onMIDIMessage;
      logMsg(`MIDI IN connected: ${input.name}`);
    });
    if(midiAccess.inputs.size===0){
      document.getElementById('midiStatus').innerText='MIDI: no inputs found — connect hardware then reload';
    }
    midiAccess.onstatechange = (e)=>{
      logMsg(`MIDI state change: ${e.port.name} ${e.port.state}`);
      initMIDI();
    };
  }catch(err){
    document.getElementById('midiStatus').innerText='MIDI: access denied — '+err.message;
    logMsg('MIDI access denied: '+err);
  }
}

function onMIDIMessage(msg){
  const [status, data1, data2] = msg.data;
  const isNoteOn = (status & 0xF0) === 0x90 && data2>0;
  const isNoteOff = (status & 0xF0) === 0x80 || ((status & 0xF0)===0x90 && data2===0);
  const isCC = (status & 0xF0) === 0xB0;
  const velocity = data2/127;

  if(learnMode && learnTargetIndex!==null && (isNoteOn || isCC)){
    const key = isCC?`CC${data1}`:`N${data1}`;
    midiMap[data1] = learnTargetIndex;
    reverseMap[learnTargetIndex]=data1;
    localStorage.setItem('katz_midi_map', JSON.stringify(midiMap));
    logMsg(`Bound ${key} (val ${data1}) → PAD ${learnTargetIndex+1} ${padNames[learnTargetIndex]}`);
    document.querySelectorAll('.pad').forEach((p,idx)=>{
      if(idx===learnTargetIndex){ p.classList.add('has-midi'); p.querySelector('.midi-tag').innerText=`MIDI ${data1}`; p.classList.remove('midi-learn'); }
    });
    learnTargetIndex=null;
    // keep learnMode active for next binding
    return;
  }

  if(isNoteOn){
    const padIndex = midiMap[data1];
    if(padIndex!==undefined){
      triggerPad(padIndex, velocity);
      logMsg(`MIDI Note ${data1} vel ${velocity.toFixed(2)} → PAD ${padIndex+1}`);
    } else if(!learnMode){
      // unmapped — auto-trigger by modulo
      const autoIdx = data1 % 16;
      triggerPad(autoIdx, velocity);
    }
  }
  if(isCC){
    // CC maps to bloom / filter — use CC1 modwheel to control holo intensity
    if(data1===1){
      // modwheel
      document.body.style.filter = `brightness(${1+velocity*0.3})`;
    }
  }
}

initMIDI();
</script>
</body>
</html>
"""
    (APP_DIR / "index.html").write_text(app_html, encoding="utf-8")
    print(f"[SUCCESS] KatzDrumpadHolo v2 with Web MIDI generated at {APP_DIR}/index.html")

if __name__ == "__main__":
    generate_drumpad_app()
