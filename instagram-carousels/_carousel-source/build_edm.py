#!/usr/bin/env python3
import base64, pathlib
A=pathlib.Path("/sessions/peaceful-eager-allen/mnt/outputs/designer_assets")
def b64(p): return base64.b64encode((A/p).read_bytes()).decode()
fontcss="".join(
 f"@font-face{{font-family:Inter;font-weight:{w};font-style:normal;font-display:block;src:url(data:font/woff2;base64,{b64(f'inter-latin-{w}-normal.woff2')}) format('woff2')}}"
 for w in [400,500,600,700,800])
LOGOW="data:image/png;base64,"+b64("logo-white.png")

HTML=r'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>CVBS EDM Designer</title>
<style>
__FONTCSS__
:root{--teal:#3BC9D9;--teal-deep:#28A8B6;--navy:#0A2C52;--navy2:#061E3B;--brand:#0366C6;--stone:#EEF6F7;--ink:#0D1F2D;--line:#D6E7E9;--muted:#6E747B}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Inter,system-ui,sans-serif;background:#0b1622;color:#eef3f6;display:flex;height:100vh;overflow:hidden}
.panel{width:400px;flex:none;height:100vh;overflow-y:auto;background:#0e1b28;border-right:1px solid rgba(255,255,255,.08);padding:20px 20px 40px}
.panel h1{font-size:19px;font-weight:700;margin-bottom:3px}.panel h1 b{color:var(--teal)}
.panel .tag{font-size:12.5px;color:#8aa0b0;margin-bottom:16px}
.grp{margin-bottom:16px}
.grp>label{display:block;font-size:11px;text-transform:uppercase;letter-spacing:.12em;color:#8aa0b0;font-weight:700;margin-bottom:7px}
.seg{display:flex;gap:6px}
.seg button{flex:1;padding:10px 6px;font:inherit;font-size:13px;font-weight:600;color:#cfe0ea;background:#132535;border:1px solid rgba(255,255,255,.1);border-radius:9px;cursor:pointer}
.seg button.on{background:var(--teal);color:#05222a;border-color:var(--teal)}
.field{margin-bottom:11px}
.field label{display:block;font-size:12px;color:#a9bccb;margin-bottom:5px;font-weight:500}
.field input,.field textarea{width:100%;font:inherit;font-size:13px;color:#eef3f6;background:#0b1622;border:1px solid rgba(255,255,255,.14);border-radius:8px;padding:8px 10px;resize:vertical}
.field textarea{min-height:56px;line-height:1.4}
.field input:focus,.field textarea:focus{outline:none;border-color:var(--teal)}
.row2{display:flex;gap:8px}.row2>.field{flex:1}
.card-edit{border:1px solid rgba(255,255,255,.1);border-radius:10px;padding:11px;margin-bottom:10px;background:#0c1a27}
.card-edit .ct{font-size:11px;font-weight:700;color:var(--teal);text-transform:uppercase;letter-spacing:.1em;margin-bottom:8px}
.dl{position:sticky;bottom:0;background:#0e1b28;padding-top:12px;margin-top:6px}
.dl button{width:100%;padding:13px;font:inherit;font-size:14.5px;font-weight:700;color:#05222a;background:var(--teal);border:none;border-radius:11px;cursor:pointer}
.dl button.secondary{background:#173049;color:#cfe0ea;margin-top:8px;font-size:13px;padding:10px}
.hint{font-size:11.5px;color:#8aa0b0;margin-top:8px;line-height:1.4}
.stage{flex:1;height:100vh;overflow:auto;background:#c9d4dc;display:flex;justify-content:center;padding:26px}
.previewwrap{width:600px;flex:none;background:#fff;box-shadow:0 30px 70px -30px rgba(0,0,0,.5);height:max-content}
iframe{width:600px;border:0;display:block}
.bar{position:fixed;top:14px;right:22px;background:rgba(10,44,82,.9);color:#fff;font-size:12px;font-weight:600;padding:8px 14px;border-radius:8px;backdrop-filter:blur(6px)}
</style></head>
<body>
<div class="panel">
  <h1>CVBS <b>EDM Designer</b></h1>
  <div class="tag">Fill it in, copy the HTML, paste into Mailchimp.</div>
  <div class="grp"><label>Email type</label><div class="seg" id="modes"></div></div>
  <div id="fields"></div>
  <div class="dl">
    <button id="copy">Copy HTML for Mailchimp</button>
    <button id="download" class="secondary">Download .html</button>
    <div class="hint">In Mailchimp: Create → Email → Code your own → Paste in code. The unsubscribe + address footer is already wired in.</div>
  </div>
</div>
<div class="stage"><div class="previewwrap"><iframe id="pv"></iframe></div></div>
<div class="bar" id="bar">Live preview · 600px</div>
<script>
const LOGOW="__LOGOW__";
const BASE="https://the-service-edit.github.io/cvbs-2026/";
const esc=s=>(s||"").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
const nl2br=s=>esc(s).replace(/\n/g,"<br>");
const lines=s=>(s||"").split("\n").map(x=>x.trim()).filter(Boolean);

// email-safe colors
const C={navy:"#0A2C52",navy2:"#061E3B",teal:"#28A8B6",tealb:"#3BC9D9",stone:"#EEF6F7",ink:"#0D1F2D",muted:"#6E747B",line:"#D6E7E9",amber:"#E0B341"};
const FONT="Inter,Arial,Helvetica,sans-serif";
function shell(inner,preheader){return `<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="X-UA-Compatible" content="IE=edge"></head>
<body style="margin:0;padding:0;background:${C.stone};">
<span style="display:none;font-size:1px;color:${C.stone};line-height:1px;max-height:0;max-width:0;opacity:0;overflow:hidden">${esc(preheader)}</span>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:${C.stone};"><tr><td align="center" style="padding:22px 12px;">
<table role="presentation" width="600" cellpadding="0" cellspacing="0" style="width:600px;max-width:600px;background:#ffffff;border-radius:16px;overflow:hidden;font-family:${FONT};">
${inner}
</table></td></tr></table></body></html>`;}

function header(){return `<tr><td style="background:${C.navy};padding:20px 28px;">
<img src="${BASE}assets/img/logo-white.png" alt="CVBS" width="120" style="display:block;border:0;height:auto;width:120px;">
</td></tr>`;}
function btn(text,url){return `<table role="presentation" cellpadding="0" cellspacing="0"><tr><td align="center" bgcolor="${C.teal}" style="border-radius:12px;">
<a href="${esc(url)}" style="display:inline-block;padding:16px 34px;font-family:${FONT};font-size:16px;font-weight:700;color:#ffffff;text-decoration:none;border-radius:12px;">${esc(text)} &rarr;</a>
</td></tr></table>`;}
function briefBlock(url){return `<tr><td style="padding:6px 28px 26px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:${C.stone};border:1px solid ${C.line};border-radius:14px;"><tr><td style="padding:22px 24px;">
<div style="font-family:${FONT};font-size:18px;font-weight:700;color:${C.ink};">Planning a different event?</div>
<div style="font-family:${FONT};font-size:14px;line-height:1.5;color:${C.muted};padding:6px 0 14px;">Tell us what you're planning and we'll source the right venue, compare options and negotiate the rate. Free to you, since 1989.</div>
${btn("Send us your brief",url)}
</td></tr></table></td></tr>`;}
function footer(){return `<tr><td style="background:${C.navy};padding:22px 28px;">
<div style="font-family:${FONT};font-size:12px;line-height:1.6;color:rgba(255,255,255,.72);">
CVBS · Conference Venues &amp; Booking Services<br>*|HTML:LIST_ADDRESS_HTML|*<br>
<a href="*|UNSUB|*" style="color:${C.tealb};">Unsubscribe</a> &nbsp;·&nbsp;
<a href="*|UPDATE_PROFILE|*" style="color:${C.tealb};">Update preferences</a> &nbsp;·&nbsp;
<a href="*|ARCHIVE|*" style="color:${C.tealb};">View in browser</a>
</div></td></tr>`;}

function F(k){return state.fields[k]||"";}

function buildOffer(){const specs=[[F('s1')],[F('s2')],[F('s3')]];
 const specCells=[F('s1'),F('s2'),F('s3')].map(s=>`<td width="33%" align="center" style="padding:14px 8px;font-family:${FONT};font-size:13px;font-weight:600;color:${C.navy};border-right:1px solid ${C.line};">${esc(s)}</td>`).join("").replace(/border-right:1px solid #D6E7E9;">([^<]*)<\/td>$/,'">$1</td>');
 const incl=lines(F('inclusions')).map(x=>`<tr><td valign="top" style="font-family:${FONT};font-size:15px;color:${C.teal};padding:3px 8px 3px 0;">✓</td><td style="font-family:${FONT};font-size:15px;line-height:1.5;color:${C.ink};padding:3px 0;">${esc(x)}</td></tr>`).join("");
 const deadline=F('deadline')?`<tr><td style="padding:0 28px 20px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:${C.amber};border-radius:10px;"><tr><td align="center" style="padding:12px;font-family:${FONT};font-size:14px;font-weight:700;color:#3a2a00;">${esc(F('deadline'))}</td></tr></table></td></tr>`:"";
 const inner=header()+
 `<tr><td style="background:${C.navy2};padding:14px 28px;font-family:${FONT};font-size:15px;font-weight:700;color:${C.tealb};letter-spacing:.02em;">${esc(F('dealBand'))}</td></tr>`+
 `<tr><td style="padding:0;"><img src="${esc(F('hero'))}" alt="" width="600" style="display:block;border:0;width:100%;max-width:600px;height:auto;"></td></tr>`+
 `<tr><td style="padding:26px 28px 6px;">
   <div style="font-family:${FONT};font-size:12px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:${C.brand||'#0366C6'};">${esc(F('eyebrow'))}</div>
   <div style="font-family:${FONT};font-size:30px;line-height:1.15;font-weight:800;color:${C.navy};padding:8px 0 0;">${nl2br(F('headline'))}</div>
   <div style="font-family:${FONT};font-size:15px;line-height:1.6;color:${C.muted};padding:12px 0 0;">${nl2br(F('intro'))}</div>
 </td></tr>`+
 `<tr><td style="padding:18px 28px 6px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:${C.stone};border:1px solid ${C.line};border-radius:12px;"><tr>${specCells}</tr></table></td></tr>`+
 `<tr><td style="padding:14px 28px 6px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:${C.stone};border:1px solid ${C.line};border-radius:14px;"><tr><td style="padding:22px 24px;">
   <div style="font-family:${FONT};font-size:18px;font-weight:700;color:${C.navy};padding-bottom:12px;">${esc(F('offerTitle'))}</div>
   <table role="presentation" cellpadding="0" cellspacing="0">${incl}</table>
 </td></tr></table></td></tr>`+
 deadline+
 `<tr><td align="center" style="padding:8px 28px 24px;">${btn(F('ctaText'),F('ctaUrl'))}</td></tr>`+
 briefBlock(F('briefUrl'))+
 `<tr><td style="padding:2px 28px 24px;font-family:${FONT};font-size:15px;line-height:1.6;color:${C.ink};">${nl2br(F('signoff'))}</td></tr>`+
 (F('finePrint')?`<tr><td style="padding:0 28px 22px;font-family:${FONT};font-size:11px;line-height:1.5;color:${C.muted};">${nl2br(F('finePrint'))}</td></tr>`:"")+
 footer();
 return shell(inner,F('preheader'));}

function card(im,ti,bl,ur){return `<tr><td style="padding:0 28px 16px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border:1px solid ${C.line};border-radius:14px;overflow:hidden;"><tr>
<td width="190" style="padding:0;"><img src="${esc(im)}" alt="" width="190" style="display:block;border:0;width:190px;height:150px;object-fit:cover;"></td>
<td style="padding:16px 18px;vertical-align:top;">
<div style="font-family:${FONT};font-size:17px;font-weight:700;color:${C.navy};">${esc(ti)}</div>
<div style="font-family:${FONT};font-size:13px;line-height:1.5;color:${C.muted};padding:6px 0 10px;">${esc(bl)}</div>
<a href="${esc(ur)}" style="font-family:${FONT};font-size:14px;font-weight:700;color:${C.teal};text-decoration:none;">View offer &rarr;</a>
</td></tr></table></td></tr>`;}

function buildRoundup(){
 const cards=[1,2,3].map(i=>F('c'+i+'img')||F('c'+i+'title')?card(F('c'+i+'img'),F('c'+i+'title'),F('c'+i+'blurb'),F('c'+i+'url')):"").join("");
 const inner=header()+
 `<tr><td style="padding:26px 28px 6px;">
   <div style="font-family:${FONT};font-size:12px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#0366C6;">${esc(F('eyebrow'))}</div>
   <div style="font-family:${FONT};font-size:30px;line-height:1.15;font-weight:800;color:${C.navy};padding:8px 0 0;">${nl2br(F('headline'))}</div>
   <div style="font-family:${FONT};font-size:15px;line-height:1.6;color:${C.muted};padding:12px 0 18px;">${nl2br(F('intro'))}</div>
 </td></tr>`+
 cards+
 `<tr><td style="padding:10px 28px 24px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:${C.navy};border-radius:14px;"><tr><td align="center" style="padding:26px 24px;">
   <div style="font-family:${FONT};font-size:20px;font-weight:800;color:#fff;padding-bottom:6px;">Not seeing your city?</div>
   <div style="font-family:${FONT};font-size:14px;line-height:1.5;color:rgba(255,255,255,.8);padding-bottom:16px;">Send us the brief and we'll source it. Free to you.</div>
   ${btn(F('ctaText'),F('briefUrl'))}
 </td></tr></table></td></tr>`+
 `<tr><td style="padding:2px 28px 24px;font-family:${FONT};font-size:15px;line-height:1.6;color:${C.ink};">${nl2br(F('signoff'))}</td></tr>`+
 footer();
 return shell(inner,F('preheader'));}

const DEF={
 offer:{preheader:"A limited-time rate at one of Sydney's best venues.",dealBand:"Winter day delegate from $110pp",hero:BASE+"assets/img/offers/kimpton.jpg",
  eyebrow:"Venue offer · Sydney",headline:"Winter at Kimpton Margot",intro:"A limited winter rate at one of Sydney's most characterful heritage hotels, available April to June 2026.",
  s1:"Up to 120 delegates",s2:"Sydney CBD",s3:"April–June 2026",offerTitle:"What's included",
  inclusions:"Seasonal menus by Luke Mangan\nBarista coffee and juice shots on arrival\nA plated working lunch\nFull-service day delegate, start to finish",
  deadline:"Book by 30 June 2026",ctaText:"Get this rate",ctaUrl:BASE+"submit-a-brief.html",briefUrl:BASE+"submit-a-brief.html",
  signoff:"Karen, Anthony, Chantelle & Rychelle\nCVBS",finePrint:"Subject to availability. New bookings only. Terms and conditions apply."},
 roundup:{preheader:"This month's venue offers, negotiated for CVBS clients.",eyebrow:"Offers roundup · June",headline:"This month's venue offers",
  intro:"A few rates worth booking this month. Every one negotiated for CVBS clients.",
  c1img:BASE+"assets/img/offers/kimpton.jpg",c1title:"Kimpton Margot, Sydney",c1blurb:"Winter day delegate from $110pp, April to June.",c1url:BASE+"offers.html",
  c2img:BASE+"assets/img/offers/hyatt.jpg",c2title:"Hyatt Place, Essendon Fields",c2blurb:"1,700 sqm pillarless, minutes from the airport.",c2url:BASE+"offers.html",
  c3img:BASE+"assets/img/offers/hamilton-island.jpg",c3title:"Hamilton Island",c3blurb:"Up to 700 delegates in the Whitsundays.",c3url:BASE+"offers.html",
  ctaText:"Send us your brief",briefUrl:BASE+"submit-a-brief.html",signoff:"Karen, Anthony, Chantelle & Rychelle\nCVBS"}
};
const LABEL={preheader:"Preview text",dealBand:"Deal band (top hook)",hero:"Hero image URL",eyebrow:"Eyebrow",headline:"Headline",intro:"Intro paragraph",
 s1:"Spec 1",s2:"Spec 2",s3:"Spec 3",offerTitle:"Offer panel title",inclusions:"Inclusions (one per line)",deadline:"Deadline strip (blank = hide)",
 ctaText:"Button text",ctaUrl:"Button link",briefUrl:"Brief-block link",signoff:"Sign-off",finePrint:"Fine print",
 c1img:"Card 1 image",c1title:"Card 1 title",c1blurb:"Card 1 blurb",c1url:"Card 1 link",
 c2img:"Card 2 image",c2title:"Card 2 title",c2blurb:"Card 2 blurb",c2url:"Card 2 link",
 c3img:"Card 3 image",c3title:"Card 3 title",c3blurb:"Card 3 blurb",c3url:"Card 3 link"};
const AREA=new Set(["intro","inclusions","signoff","finePrint","headline","c1blurb","c2blurb","c3blurb","preheader"]);
const ORDER={offer:["preheader","dealBand","eyebrow","headline","hero","intro","s1","s2","s3","offerTitle","inclusions","deadline","ctaText","ctaUrl","briefUrl","signoff","finePrint"],
 roundup:["preheader","eyebrow","headline","intro","c1img","c1title","c1blurb","c1url","c2img","c2title","c2blurb","c2url","c3img","c3title","c3blurb","c3url","ctaText","briefUrl","signoff"]};

let state={mode:"offer",fields:Object.assign({},DEF.offer)};
function buildModes(){const c=document.getElementById('modes');c.innerHTML="";
 [["offer","Venue offer"],["roundup","Offers roundup"]].forEach(([k,n])=>{const b=document.createElement('button');b.textContent=n;b.className=k===state.mode?"on":"";
  b.onclick=()=>{state.mode=k;state.fields=Object.assign({},DEF[k]);buildModes();buildFields();render();};c.appendChild(b);});}
function mkField(k){const d=document.createElement('div');d.className="field";
 const l=document.createElement('label');l.textContent=LABEL[k]||k;d.appendChild(l);
 const el=document.createElement(AREA.has(k)?'textarea':'input');el.value=state.fields[k]||"";
 el.oninput=()=>{state.fields[k]=el.value;render();};d.appendChild(el);return d;}
function buildFields(){const c=document.getElementById('fields');c.innerHTML="";
 if(state.mode==='roundup'){
   ["preheader","eyebrow","headline","intro"].forEach(k=>c.appendChild(mkField(k)));
   [1,2,3].forEach(i=>{const box=document.createElement('div');box.className="card-edit";
     const t=document.createElement('div');t.className="ct";t.textContent="Card "+i;box.appendChild(t);
     ["c"+i+"img","c"+i+"title","c"+i+"blurb","c"+i+"url"].forEach(k=>box.appendChild(mkField(k)));c.appendChild(box);});
   ["ctaText","briefUrl","signoff"].forEach(k=>c.appendChild(mkField(k)));
 } else { ORDER.offer.forEach(k=>{
     if(k==='ctaText'||k==='s1'){const w=document.createElement('div');w.className="row2";
       const pair=k==='s1'?["s1","s2"]:["ctaText","ctaUrl"];pair.forEach(pk=>w.appendChild(mkField(pk)));c.appendChild(w);
       if(k==='s1')c.appendChild(mkField("s3"));return;}
     if(k==='s2'||k==='ctaUrl'||k==='s3')return;
     c.appendChild(mkField(k));});}
}
function render(){const html=state.mode==='offer'?buildOffer():buildRoundup();
 document.getElementById('pv').srcdoc=html;window._html=html;
 const f=document.getElementById('pv');f.onload=()=>{try{f.style.height=(f.contentWindow.document.body.scrollHeight+20)+"px";}catch(e){}};}
document.getElementById('copy').onclick=async(e)=>{const b=e.target,o=b.textContent;
 try{await navigator.clipboard.writeText(window._html);b.textContent="Copied ✓";}catch(err){
   const ta=document.createElement('textarea');ta.value=window._html;document.body.appendChild(ta);ta.select();document.execCommand('copy');ta.remove();b.textContent="Copied ✓";}
 setTimeout(()=>b.textContent=o,1400);};
document.getElementById('download').onclick=()=>{const blob=new Blob([window._html],{type:"text/html"});
 const a=document.createElement('a');a.download=`cvbs-edm-${state.mode}.html`;a.href=URL.createObjectURL(blob);a.click();};
buildModes();buildFields();render();
</script></body></html>'''
HTML=HTML.replace("__FONTCSS__",fontcss).replace("__LOGOW__",LOGOW)
out=pathlib.Path("/sessions/peaceful-eager-allen/mnt/outputs/CVBS-EDM-Designer.html")
out.write_text(HTML)
print("edm bytes:",len(HTML))
