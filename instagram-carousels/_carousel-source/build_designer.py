#!/usr/bin/env python3
import base64, pathlib
A=pathlib.Path("/sessions/peaceful-eager-allen/mnt/outputs/designer_assets")
def b64(p): return base64.b64encode((A/p).read_bytes()).decode()
def datauri(p,mime): return f"data:{mime};base64,{b64(p)}"

fontcss="".join(
 f"@font-face{{font-family:Inter;font-weight:{w};font-style:normal;font-display:block;src:url(data:font/woff2;base64,{b64(f'inter-latin-{w}-normal.woff2')}) format('woff2')}}"
 for w in [400,500,600,700,800])
LOGOW=datauri("logo-white.png","image/png")
LOGOD=datauri("logo.png","image/png")
PHOTOS={k:datauri(f"photo_{k}.jpg","image/jpeg") for k in ["group","kimpton","hyatt","crown","sydney"]}
photos_js="{"+",".join(f'"{k}":"{v}"' for k,v in PHOTOS.items())+"}"
HTI=(A/"html-to-image.js").read_text()

HTML=r'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>CVBS Post Designer</title>
<style>
__FONTCSS__
:root{--teal:#3BC9D9;--teal-deep:#28A8B6;--navy:#0D2233;--navy2:#071520;--stone:#F4F1EA;--ink:#0D1F2D;--line:#E3DED2;--muted:#6E747B}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Inter,system-ui,sans-serif;background:#0b1622;color:#eef3f6;display:flex;height:100vh;overflow:hidden}
/* ---- controls panel ---- */
.panel{width:380px;flex:none;height:100vh;overflow-y:auto;background:#0e1b28;border-right:1px solid rgba(255,255,255,.08);padding:22px 22px 60px}
.panel h1{font-size:19px;font-weight:700;letter-spacing:-.01em;margin-bottom:4px}
.panel h1 b{color:var(--teal)}
.panel .tag{font-size:12.5px;color:#8aa0b0;margin-bottom:20px}
.grp{margin-bottom:20px}
.grp>label{display:block;font-size:11px;text-transform:uppercase;letter-spacing:.12em;color:#8aa0b0;font-weight:700;margin-bottom:8px}
.seg{display:flex;flex-wrap:wrap;gap:6px}
.seg button{flex:1;min-width:0;padding:9px 6px;font:inherit;font-size:12.5px;font-weight:600;color:#cfe0ea;background:#132535;border:1px solid rgba(255,255,255,.1);border-radius:9px;cursor:pointer;white-space:nowrap}
.seg button.on{background:var(--teal);color:#05222a;border-color:var(--teal)}
.tmpls{display:grid;grid-template-columns:1fr 1fr;gap:7px}
.tmpls button{padding:11px 8px;font:inherit;font-size:12.5px;font-weight:600;color:#cfe0ea;background:#132535;border:1px solid rgba(255,255,255,.1);border-radius:9px;cursor:pointer;text-align:left}
.tmpls button.on{background:#1d3a52;border-color:var(--teal);color:#fff}
.field{margin-bottom:12px}
.field label{display:block;font-size:12px;color:#a9bccb;margin-bottom:5px;font-weight:500}
.field input,.field textarea{width:100%;font:inherit;font-size:13.5px;color:#eef3f6;background:#0b1622;border:1px solid rgba(255,255,255,.14);border-radius:8px;padding:9px 11px;resize:vertical}
.field textarea{min-height:60px;line-height:1.35}
.field input:focus,.field textarea:focus{outline:none;border-color:var(--teal)}
.row2{display:flex;gap:8px}.row2>.field{flex:1}
.slider{display:flex;align-items:center;gap:10px}
.slider input[type=range]{flex:1}
.photos{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:8px}
.photos .th{width:52px;height:52px;border-radius:8px;background-size:cover;background-position:center;cursor:pointer;border:2px solid transparent}
.photos .th.on{border-color:var(--teal)}
.up{display:inline-block;font-size:12.5px;font-weight:600;color:#05222a;background:var(--teal);padding:9px 14px;border-radius:8px;cursor:pointer}
.chk{display:flex;align-items:center;gap:8px;font-size:13px;color:#cfe0ea;cursor:pointer}
.dl{position:sticky;bottom:0;margin-top:10px}
.dl button{width:100%;padding:14px;font:inherit;font-size:15px;font-weight:700;color:#05222a;background:var(--teal);border:none;border-radius:11px;cursor:pointer}
.dl button:active{transform:translateY(1px)}
.hint{font-size:11.5px;color:#8aa0b0;margin-top:7px;line-height:1.4}
/* ---- stage ---- */
.stagewrap{flex:1;height:100vh;display:flex;align-items:center;justify-content:center;background:radial-gradient(60% 60% at 50% 30%,#12263a,#0a121c);padding:24px;overflow:hidden}
.stage{transform-origin:center center;box-shadow:0 40px 90px -30px rgba(0,0,0,.7);border-radius:2px}
/* ---- CARD (export target) ---- */
.card{position:relative;overflow:hidden;font-family:Inter;color:#fff;background:var(--navy)}
.fmt-ig{width:1080px;height:1350px}
.fmt-square{width:1080px;height:1080px}
.fmt-wide{width:1200px;height:628px}
.card .bg{position:absolute;inset:0;background-size:cover;transform:scale(1.05)}
.card .scrim{position:absolute;inset:0}
.card.bg-stone{background:var(--stone);color:var(--ink)}
.card .content{position:absolute;inset:0;z-index:3;display:flex;flex-direction:column;padding:80px 74px 72px}
.fmt-wide .content{padding:54px 60px}
.fill{flex:1}
.accent{color:var(--teal)}
.bg-stone .accent{color:var(--teal-deep)}
.hl{font-weight:700;line-height:1.03;letter-spacing:-.035em;text-shadow:0 4px 30px rgba(0,0,0,.35)}
.bg-stone .hl{text-shadow:none}
.h-xl{font-size:88px}.h-lg{font-size:64px}.h-md{font-size:56px}
.fmt-wide .h-xl{font-size:58px}.fmt-wide .h-lg{font-size:50px}.fmt-wide .h-md{font-size:46px}
.fmt-square .h-xl{font-size:80px}
.sub{font-size:32px;line-height:1.45;font-weight:400;color:rgba(255,255,255,.9);margin-top:18px}
.bg-stone .sub{color:#37444f}
.fmt-wide .sub{font-size:26px}
.lead-narrow{max-width:30ch}
.eyebrow{display:inline-flex;align-items:center;gap:16px;font-size:23px;letter-spacing:.24em;text-transform:uppercase;font-weight:600;color:var(--teal);align-self:flex-start}
.bg-stone .eyebrow{color:var(--teal-deep)}
.eyebrow::before{content:"";width:40px;height:3px;border-radius:2px;background:var(--teal)}
/* glass (export-safe: translucent, no backdrop-filter) */
.glass{background:linear-gradient(135deg,rgba(255,255,255,.17),rgba(255,255,255,.09));border:1.5px solid rgba(255,255,255,.30);border-radius:34px;box-shadow:0 40px 70px -30px rgba(0,0,0,.55),inset 0 2px 0 rgba(255,255,255,.38);padding:52px 54px}
.chip{align-self:flex-start;display:inline-flex;align-items:center;gap:16px;padding:17px 27px;border-radius:999px;font-size:22px;font-weight:600;letter-spacing:.2em;text-transform:uppercase;color:#fff;background:rgba(255,255,255,.15);border:1.5px solid rgba(255,255,255,.32);box-shadow:inset 0 1.5px 0 rgba(255,255,255,.4)}
.chip::before{content:"";width:34px;height:3px;border-radius:2px;background:var(--teal)}
.evbadge{align-self:flex-start;display:inline-flex;align-items:center;gap:14px;padding:15px 25px;border-radius:999px;font-size:22px;font-weight:600;letter-spacing:.18em;text-transform:uppercase;color:#fff;background:rgba(255,255,255,.15);border:1.5px solid rgba(255,255,255,.32)}
.evbadge .dot{width:8px;height:8px;border-radius:50%;background:var(--teal)}
.filebadge{align-self:flex-start;display:inline-flex;align-items:center;border:1.5px solid rgba(255,255,255,.45);border-radius:12px;overflow:hidden;font-weight:700;letter-spacing:.18em;text-transform:uppercase;font-size:21px;background:rgba(255,255,255,.12)}
.filebadge .a{padding:14px 18px;color:#fff}.filebadge .b{padding:14px 16px;background:var(--teal);color:#06262b;display:flex;align-items:center}
.loc2{align-self:flex-start;display:inline-flex;align-items:center;gap:12px;margin-top:16px;padding:12px 22px;border-radius:999px;font-size:22px;font-weight:600;color:#fff;background:rgba(7,21,32,.5);border:1.5px solid rgba(255,255,255,.28)}
.loc2 svg{width:23px;height:23px;color:var(--teal)}
.pricebox{align-self:flex-start;padding:26px 38px;border-radius:22px;margin-top:26px}
.price{display:flex;align-items:baseline;gap:16px}
.price .pre{font-size:27px;font-weight:500;color:rgba(255,255,255,.85)}
.price .big{font-size:70px;font-weight:800;letter-spacing:-.03em;color:var(--teal)}
.specbar{align-self:stretch;display:flex;border-radius:18px;overflow:hidden;margin-top:26px;background:linear-gradient(135deg,rgba(255,255,255,.16),rgba(255,255,255,.09));border:1.5px solid rgba(255,255,255,.26)}
.specbar .s{flex:1;padding:26px 8px;text-align:center}
.specbar .s+.s{border-left:1.5px solid rgba(255,255,255,.22)}
.specbar .n{font-size:38px;font-weight:800;color:var(--teal);line-height:1}
.specbar .l{font-size:18px;color:rgba(255,255,255,.85);letter-spacing:.1em;text-transform:uppercase;margin-top:8px}
.bignum{font-size:300px;font-weight:800;color:var(--teal);line-height:.74;letter-spacing:-.05em}
.tag2{align-self:flex-start;position:relative;background:var(--teal);color:#06262b;font-weight:700;padding:20px 32px 20px 58px;border-radius:16px;font-size:26px;letter-spacing:.06em;text-transform:uppercase;transform:rotate(-2.5deg)}
.tag2::before{content:"";position:absolute;left:24px;top:50%;transform:translateY(-50%);width:18px;height:18px;border-radius:50%;background:#06262b}
.statbig{font-size:96px;font-weight:800;line-height:1.0;letter-spacing:-.04em}
.foot{display:flex;align-items:center;justify-content:space-between;padding-top:28px;margin-top:8px;border-top:1px solid rgba(255,255,255,.22)}
.bg-stone .foot{border-top:1px solid var(--line)}
.foot img{height:48px}
.foot .url{font-size:24px;font-weight:600;color:rgba(255,255,255,.86)}
.bg-stone .foot .url{color:var(--muted)}
.foot .swipe{display:inline-flex;align-items:center;gap:12px;font-size:24px;font-weight:600;color:var(--teal)}
.foot .swipe svg{width:28px;height:28px}
.foot.lfoot{justify-content:flex-start;gap:18px}
.foot.lfoot .nm{font-size:23px;font-weight:700;color:#fff;line-height:1.12}
.foot.lfoot .nm span{display:block;font-size:18px;font-weight:500;color:rgba(255,255,255,.72)}
</style></head>
<body>
<div class="panel">
  <h1>CVBS <b>Post Designer</b></h1>
  <div class="tag">Pick a template, add your words and photo, download.</div>

  <div class="grp"><label>Template</label><div class="tmpls" id="tmpls"></div></div>
  <div class="grp"><label>Format</label><div class="seg" id="formats"></div></div>

  <div class="grp" id="photogrp"><label>Photo</label>
    <div class="photos" id="photos"></div>
    <label class="up">Upload photo<input type="file" id="upload" accept="image/*" hidden></label>
    <div class="slider" style="margin-top:12px"><span style="font-size:11px;color:#8aa0b0">POS</span><input type="range" id="posY" min="0" max="100" value="40"></div>
    <div class="slider"><span style="font-size:11px;color:#8aa0b0">DIM</span><input type="range" id="scrim" min="20" max="95" value="72"></div>
  </div>

  <div class="grp"><label>Content</label><div id="fields"></div></div>

  <div class="grp"><label class="chk"><input type="checkbox" id="li"> LinkedIn footer (company name)</label></div>

  <div class="dl"><button id="download">Download PNG</button>
   <div class="hint">Tip: wrap a word in *asterisks* to colour it teal. Use line breaks in the headline to control wrapping.</div>
  </div>
</div>

<div class="stagewrap" id="stagewrap">
  <div class="stage" id="stage">
    <div class="card fmt-ig" id="card">
      <div class="bg" id="bg"></div><div class="scrim" id="scrim"></div>
      <div class="content" id="content"></div>
    </div>
  </div>
</div>

<script>__HTI__</script>
<script>
const PHOTOS=__PHOTOS__, LOGOW="__LOGOW__", LOGOD="__LOGOD__";
const ARROW='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>';
const PIN='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s7-5.5 7-11a7 7 0 0 0-14 0c0 5.5 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/></svg>';
const esc=s=>(s||"").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
const rich=s=>esc(s).replace(/\*(.+?)\*/g,'<span class="accent">$1</span>').replace(/\n/g,"<br>");

// ---- component builders
const chip=t=>`<div class="chip">${esc(t)}</div>`;
const evbadge=t=>`<div class="evbadge">${esc(t).replace(/\s\|\s/,' <span class="dot"></span> ')}</div>`;
const filebadge=(a,b)=>`<div class="filebadge"><span class="a">${esc(a)}</span><span class="b">${esc(b)}</span></div>`;
const loc=t=>`<div class="loc2">${PIN} ${esc(t)}</div>`;
const tag2=t=>`<div class="tag2">${esc(t)}</div>`;
const pricePill=(p,b)=>`<div class="glass pricebox"><div class="price"><span class="pre">${esc(p)}</span><span class="big">${esc(b)}</span></div></div>`;
const specbar=a=>`<div class="specbar">${a.map(x=>`<div class="s"><div class="n">${esc(x[0])}</div><div class="l">${esc(x[1])}</div></div>`).join("")}</div>`;
function foot(){const li=document.getElementById('li').checked;const light=T[state.template].bg==='stone';
  if(li) return `<div class="foot lfoot"><img src="${light?LOGOD:LOGOW}"><div class="nm">CVBS<span>Conference Venues &amp; Booking Services</span></div></div>`;
  return `<div class="foot"><img src="${light?LOGOD:LOGOW}"><span class="url">conferencevenues.com</span><span class="swipe">Swipe ${ARROW}</span></div>`;}
const F=(k)=>state.fields[k]||"";

// ---- templates
const T={
 offer:{name:"Offer / EDM",bg:"photo",render:()=>`${chip(F('badge'))}<div class="fill"></div><div class="hl h-xl">${rich(F('headline'))}</div>${pricePill(F('pricePre'),F('priceBig'))}<div style="height:28px"></div>${foot()}`,
   def:{badge:"Venue offer · Sydney",headline:"Winter at\n*Kimpton Margot*.",pricePre:"Day delegate from",priceBig:"$110pp"},photo:"kimpton"},
 venue:{name:"Site visit · Venue Files",bg:"photo",render:()=>`${filebadge('Venue Files',F('seriesNo'))}${loc(F('location'))}<div class="fill"></div><div class="hl h-md">${rich(F('headline'))}</div>${specbar([[F('s1n'),F('s1l')],[F('s2n'),F('s2l')],[F('s3n'),F('s3l')]])}<div style="height:28px"></div>${foot()}`,
   def:{seriesNo:"No. 12",location:"Essendon Fields, VIC",headline:"Hyatt Place,\n*Essendon Fields*.",s1n:"1,700",s1l:"sqm",s2n:"1,500",s2l:"guests",s3n:"6",s3l:"rooms"},photo:"hyatt"},
 event:{name:"Industry event · Out & About",bg:"photo",render:()=>`${evbadge(F('badge'))}<div class="fill"></div><div class="glass"><div class="hl h-lg">${rich(F('headline'))}</div><div class="sub">${rich(F('sub'))}</div></div><div style="height:28px"></div>${foot()}`,
   def:{badge:"Out & About | June 2026",headline:"An afternoon\nwith *IHG*.",sub:"A great afternoon connecting with the industry."},photo:"group"},
 educational:{name:"Educational",bg:"photo",render:()=>`<div class="fill"></div>${chip(F('badge'))}<div style="height:16px"></div><div class="bignum">${esc(F('number'))}</div><div class="hl h-lg" style="margin-top:6px">${rich(F('headline'))}</div><div style="height:28px"></div>${foot()}`,
   def:{badge:"Conference planning",number:"5",headline:"mistakes that inflate\nyour event *budget*"},photo:"crown"},
 positioning:{name:"Positioning",bg:"navy",render:()=>`<div class="eyebrow">${esc(F('eyebrow'))}</div><div class="fill"></div><div class="hl h-lg">${rich(F('headline'))}</div><div class="sub lead-narrow">${rich(F('sub'))}</div><div class="fill"></div>${foot()}`,
   def:{eyebrow:"How we work",headline:"The right venue\nisn't searched.\nIt's *sourced*.",sub:"There's a difference between finding a room and being handed the right one."}},
 destination:{name:"Destination",bg:"photo",render:()=>`${tag2(F('tag'))}<div class="fill"></div><div class="hl h-xl">${rich(F('headline'))}</div><div class="sub">${rich(F('sub'))}</div><div style="height:28px"></div>${foot()}`,
   def:{tag:"Sydney, NSW",headline:"Conferences,\nsorted in *Sydney*.",sub:"From the harbour to the CBD, the right room at the right rate."},photo:"sydney"},
 roundup:{name:"Offers roundup (light)",bg:"stone",render:()=>`<div class="eyebrow">${esc(F('eyebrow'))}</div><div class="fill"></div><div class="hl h-lg">${rich(F('headline'))}</div><div class="sub">${rich(F('sub'))}</div><div class="fill"></div>${foot()}`,
   def:{eyebrow:"Offers roundup · June",headline:"This month's\nvenue *offers*.",sub:"Five rates worth booking, negotiated for CVBS clients."}},
 result:{name:"Client result",bg:"photo",render:()=>`${chip(F('badge'))}<div class="fill"></div><div class="hl statbig">${rich(F('headline'))}</div><div class="sub">${rich(F('sub'))}</div><div style="height:28px"></div>${foot()}`,
   def:{badge:"Client result",headline:"140 delegates.\n48 hours.\n*One* call.",sub:"A last-minute national conference, handled."},photo:"crown"},
};
const FIELD_LABELS={badge:"Eyebrow / badge",headline:"Headline",sub:"Sub-line",pricePre:"Price label",priceBig:"Price",seriesNo:"File number",location:"Location",eyebrow:"Eyebrow",number:"Big number",tag:"Tag text",
 s1n:"Stat 1",s1l:"Label 1",s2n:"Stat 2",s2l:"Label 2",s3n:"Stat 3",s3l:"Label 3"};
const AREA=new Set(["headline","sub"]);
const PAIRS=[["s1n","s1l"],["s2n","s2l"],["s3n","s3l"]];

let state={template:"offer",format:"ig",photo:PHOTOS.kimpton,posY:40,scrim:72,fields:{}};

function loadDefaults(){const t=T[state.template];state.fields=Object.assign({},t.def);if(t.photo)state.photo=PHOTOS[t.photo];}

function buildTemplateButtons(){const c=document.getElementById('tmpls');c.innerHTML="";
 Object.keys(T).forEach(k=>{const b=document.createElement('button');b.textContent=T[k].name;b.className=k===state.template?"on":"";
  b.onclick=()=>{state.template=k;loadDefaults();syncFormatForTemplate();buildTemplateButtons();buildFields();togglePhoto();render();};c.appendChild(b);});}

const FORMATS=[["ig","Instagram 4:5"],["square","Square"],["wide","LinkedIn wide"]];
function buildFormatButtons(){const c=document.getElementById('formats');c.innerHTML="";
 FORMATS.forEach(([k,n])=>{const b=document.createElement('button');b.textContent=n;b.className=k===state.format?"on":"";
  b.onclick=()=>{state.format=k;buildFormatButtons();render();};c.appendChild(b);});}
function syncFormatForTemplate(){/* keep current format */}

function buildFields(){const c=document.getElementById('fields');c.innerHTML="";const t=T[state.template];
 const keys=Object.keys(t.def);
 // group spec pairs on one row
 const done=new Set();
 keys.forEach(k=>{ if(done.has(k))return;
  const pair=PAIRS.find(p=>p[0]===k);
  if(pair){const wrap=document.createElement('div');wrap.className="row2";
    pair.forEach(pk=>{wrap.appendChild(makeField(pk));done.add(pk);});c.appendChild(wrap);return;}
  c.appendChild(makeField(k));done.add(k);
 });}
function makeField(k){const d=document.createElement('div');d.className="field";
 const lab=document.createElement('label');lab.textContent=FIELD_LABELS[k]||k;d.appendChild(lab);
 const el=document.createElement(AREA.has(k)?'textarea':'input');el.value=state.fields[k]||"";
 el.oninput=()=>{state.fields[k]=el.value;render();};d.appendChild(el);return d;}

function buildPhotoThumbs(){const c=document.getElementById('photos');c.innerHTML="";
 Object.keys(PHOTOS).forEach(k=>{const d=document.createElement('div');d.className="th"+(state.photo===PHOTOS[k]?" on":"");
  d.style.backgroundImage=`url(${PHOTOS[k]})`;d.onclick=()=>{state.photo=PHOTOS[k];buildPhotoThumbs();render();};c.appendChild(d);});}
document.getElementById('upload').onchange=e=>{const f=e.target.files[0];if(!f)return;const r=new FileReader();
 r.onload=()=>{state.photo=r.result;buildPhotoThumbs();render();};r.readAsDataURL(f);};
document.getElementById('posY').oninput=e=>{state.posY=+e.target.value;render();};
document.getElementById('scrim').oninput=e=>{state.scrim=+e.target.value;render();};
document.getElementById('li').onchange=render;

function togglePhoto(){document.getElementById('photogrp').style.display=T[state.template].bg==='photo'?'block':'none';}

function render(){const t=T[state.template];const card=document.getElementById('card');
 card.className="card fmt-"+state.format+(t.bg==='stone'?" bg-stone":"");
 const bg=document.getElementById('bg'),scr=document.getElementById('scrim');
 if(t.bg==='photo'){bg.style.display=scr.style.display="block";bg.style.backgroundImage=`url(${state.photo})`;
   bg.style.backgroundPosition=`center ${state.posY}%`;
   const a=state.scrim/100;
   scr.style.background=`linear-gradient(180deg,rgba(7,21,32,${a*0.42}) 0%,rgba(7,21,32,${a*0.22}) 42%,rgba(7,21,32,${a}) 100%)`;
 } else {bg.style.display=scr.style.display="none";}
 document.getElementById('content').innerHTML=t.render();
 fit();}

function fit(){const card=document.getElementById('card'),wrap=document.getElementById('stagewrap'),stage=document.getElementById('stage');
 const cw=card.offsetWidth,ch=card.offsetHeight;const pad=48;
 const s=Math.min((wrap.clientWidth-pad)/cw,(wrap.clientHeight-pad)/ch);
 stage.style.transform=`scale(${s})`;stage.style.width=cw+"px";stage.style.height=ch+"px";}
window.addEventListener('resize',fit);

document.getElementById('download').onclick=async()=>{const btn=document.getElementById('download');const old=btn.textContent;btn.textContent="Rendering…";
 const card=document.getElementById('card');
 try{await document.fonts.ready;
  const url=await htmlToImage.toPng(card,{pixelRatio:2,cacheBust:true,width:card.offsetWidth,height:card.offsetHeight});
  const a=document.createElement('a');a.download=`cvbs-${state.template}-${state.format}.png`;a.href=url;a.click();
 }catch(err){alert("Export error: "+err);}
 btn.textContent=old;};

// init
buildTemplateButtons();buildFormatButtons();loadDefaults();buildFields();buildPhotoThumbs();togglePhoto();render();
setTimeout(fit,60);
</script></body></html>'''

HTML=(HTML.replace("__FONTCSS__",fontcss).replace("__HTI__",HTI)
      .replace("__PHOTOS__",photos_js).replace("__LOGOW__",LOGOW).replace("__LOGOD__",LOGOD))
out=pathlib.Path("/sessions/peaceful-eager-allen/mnt/outputs/CVBS-Post-Designer.html")
out.write_text(HTML)
print("designer bytes:",len(HTML))
