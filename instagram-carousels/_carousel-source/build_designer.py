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
JSZIP=(A/"jszip.min.js").read_text()

HTML=r'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>CVBS Post Designer</title>
<style>
__FONTCSS__
:root{--teal:#3BC9D9;--teal-deep:#28A8B6;--navy:#0A2C52;--navy2:#061E3B;--brand:#0366C6;--stone:#EEF6F7;--stone-deep:#DFEFF1;--ink:#0D1F2D;--line:#D6E7E9;--muted:#6E747B}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Inter,system-ui,sans-serif;background:#0b1622;color:#eef3f6;display:flex;height:100vh;overflow:hidden}
.panel{width:392px;flex:none;height:100vh;overflow-y:auto;background:#0e1b28;border-right:1px solid rgba(255,255,255,.08);padding:22px 22px 40px}
.panel h1{font-size:19px;font-weight:700;letter-spacing:-.01em;margin-bottom:4px}
.panel h1 b{color:var(--teal)}
.panel .tag{font-size:12.5px;color:#8aa0b0;margin-bottom:18px}
.grp{margin-bottom:18px}
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
/* slides strip */
.slides{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:8px}
.slidechip{display:flex;align-items:center;gap:7px;padding:8px 10px;background:#132535;border:1px solid rgba(255,255,255,.1);border-radius:9px;cursor:pointer;color:#cfe0ea;font:inherit;font-size:11.5px;font-weight:600;max-width:158px}
.slidechip.on{border-color:var(--teal);background:#1d3a52;color:#fff}
.slidechip .sn{background:var(--teal);color:#05222a;border-radius:5px;padding:1px 6px;font-weight:800;font-size:11px}
.slidechip .st{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.slideadd{padding:8px 13px;background:#132535;border:1px dashed rgba(255,255,255,.28);border-radius:9px;color:#cfe0ea;cursor:pointer;font:inherit;font-weight:700;font-size:14px}
.slideops{display:flex;gap:6px}
.slideops button{flex:1;padding:8px 4px;font:inherit;font-size:11.5px;font-weight:600;color:#cfe0ea;background:#132535;border:1px solid rgba(255,255,255,.1);border-radius:8px;cursor:pointer}
.slideops button:hover{border-color:var(--teal)}
.dl{position:sticky;bottom:0;background:#0e1b28;padding-top:12px;margin-top:6px}
.dl button{width:100%;padding:14px;font:inherit;font-size:15px;font-weight:700;color:#05222a;background:var(--teal);border:none;border-radius:11px;cursor:pointer}
.dl button.secondary{background:#173049;color:#cfe0ea;margin-top:8px;font-size:13.5px;padding:11px}
.dl button:active{transform:translateY(1px)}
.hint{font-size:11.5px;color:#8aa0b0;margin-top:7px;line-height:1.4}
/* stage */
.stagewrap{flex:1;height:100vh;display:flex;align-items:center;justify-content:center;background:radial-gradient(60% 60% at 50% 30%,#12263a,#0a121c);padding:24px;overflow:hidden}
.stage{transform-origin:center center;box-shadow:0 40px 90px -30px rgba(0,0,0,.7);border-radius:2px}
/* CARD */
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
.hl{font-weight:700;line-height:1.03;letter-spacing:-.035em;text-shadow:0 2px 22px rgba(0,0,0,.6)}
.bg-stone .hl{text-shadow:none}
.h-xl{font-size:88px}.h-lg{font-size:64px}.h-md{font-size:56px}
.fmt-wide .h-xl{font-size:58px}.fmt-wide .h-lg{font-size:50px}.fmt-wide .h-md{font-size:46px}
.fmt-square .h-xl{font-size:80px}
.sub{font-size:32px;line-height:1.45;font-weight:400;color:rgba(255,255,255,.9);margin-top:18px}
.bg-stone .sub{color:#37444f}
.fmt-wide .sub{font-size:26px}
.lead-narrow{max-width:30ch}
.eyebrow{display:inline-flex;align-items:center;font-size:23px;letter-spacing:.24em;text-transform:uppercase;font-weight:700;color:var(--teal);align-self:flex-start}
.bg-stone .eyebrow{color:var(--teal-deep)}
.glass{background:linear-gradient(135deg,rgba(6,30,59,.60),rgba(6,30,59,.44));border:1.5px solid rgba(255,255,255,.20);border-radius:22px;box-shadow:0 40px 70px -30px rgba(0,0,0,.6),inset 0 1.5px 0 rgba(255,255,255,.22);padding:52px 54px}
.chip{align-self:flex-start;display:inline-flex;align-items:center;padding:16px 26px;border-radius:11px;font-size:22px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:#08252c;background:var(--teal)}
.evbadge{align-self:flex-start;display:inline-flex;align-items:center;gap:14px;padding:15px 25px;border-radius:11px;font-size:22px;font-weight:700;letter-spacing:.18em;text-transform:uppercase;color:#08252c;background:var(--teal)}
.evbadge .dot{width:8px;height:8px;border-radius:50%;background:#08252c}
.filebadge{align-self:flex-start;display:inline-flex;align-items:center;border-radius:11px;overflow:hidden;font-weight:700;letter-spacing:.18em;text-transform:uppercase;font-size:21px;background:rgba(6,30,59,.62);border:1.5px solid rgba(255,255,255,.20)}
.filebadge .a{padding:14px 18px;color:#fff}.filebadge .b{padding:14px 16px;background:var(--teal);color:#06262b;display:flex;align-items:center}
.loc2{align-self:flex-start;display:inline-flex;align-items:center;gap:12px;margin-top:16px;padding:12px 22px;border-radius:11px;font-size:22px;font-weight:600;color:#fff;background:rgba(6,30,59,.62);border:1.5px solid rgba(255,255,255,.22)}
.loc2 svg{width:23px;height:23px;color:var(--teal)}
.pricebox{align-self:flex-start;padding:24px 36px;border-radius:14px;margin-top:26px}
.price{display:flex;align-items:baseline;gap:16px}
.price .pre{font-size:27px;font-weight:500;color:rgba(255,255,255,.9)}
.price .big{font-size:70px;font-weight:800;letter-spacing:-.03em;color:var(--teal)}
.specbar{align-self:stretch;display:flex;border-radius:14px;overflow:hidden;margin-top:26px;background:rgba(6,30,59,.58);border:1.5px solid rgba(255,255,255,.20)}
.specbar .s{flex:1;padding:26px 8px;text-align:center}
.specbar .s+.s{border-left:1.5px solid rgba(255,255,255,.22)}
.specbar .n{font-size:38px;font-weight:800;color:var(--teal);line-height:1}
.specbar .l{font-size:18px;color:rgba(255,255,255,.85);letter-spacing:.1em;text-transform:uppercase;margin-top:8px}
.bignum{font-size:300px;font-weight:800;color:var(--teal);line-height:.74;letter-spacing:-.05em}
.tag2{align-self:flex-start;position:relative;background:var(--teal);color:#06262b;font-weight:700;padding:20px 32px 20px 58px;border-radius:11px;font-size:26px;letter-spacing:.06em;text-transform:uppercase;transform:rotate(-2.5deg)}
.tag2::before{content:"";position:absolute;left:24px;top:50%;transform:translateY(-50%);width:18px;height:18px;border-radius:50%;background:#06262b}
.btn{align-self:flex-start;display:inline-flex;align-items:center;gap:12px;background:var(--teal);color:#06262b;font-weight:700;font-size:30px;padding:22px 36px;border-radius:12px;margin-top:8px}
.btn svg{width:28px;height:28px}
.content.center{align-items:center;text-align:center}
.content.center .chip,.content.center .evbadge,.content.center .eyebrow,.content.center .filebadge,.content.center .loc2,.content.center .pricebox,.content.center .tag2,.content.center .btn,.content.center .bignum{align-self:center}
.content.center .glass,.content.center .specbar,.content.center .foot{align-self:stretch}
.statbig{font-size:96px;font-weight:800;line-height:1.0;letter-spacing:-.04em}
.foot{display:flex;width:100%;align-items:center;justify-content:space-between;padding-top:28px;margin-top:8px;border-top:1px solid rgba(255,255,255,.22)}
.bg-stone .foot{border-top:1px solid var(--line)}
.foot img{height:48px}
.foot .url{font-size:24px;font-weight:600;color:rgba(255,255,255,.86)}
.bg-stone .foot .url{color:var(--muted)}
.foot .swipe{display:inline-flex;align-items:center;gap:12px;font-size:24px;font-weight:600;color:var(--teal)}
.foot .swipe svg{width:28px;height:28px}
.foot.lfoot{justify-content:flex-start;gap:18px}
.foot.lfoot .nm{font-size:23px;font-weight:700;color:#fff;line-height:1.12}
.foot.lfoot .nm span{display:block;font-size:18px;font-weight:500;color:rgba(255,255,255,.72)}
.dots{display:flex;gap:11px;align-items:center}
.dot{width:11px;height:11px;border-radius:50%;background:rgba(255,255,255,.34)}
.dot.on{background:var(--teal);width:30px;border-radius:6px}
.bg-stone .dot{background:rgba(10,44,82,.22)}.bg-stone .dot.on{background:var(--teal-deep)}
</style></head>
<body>
<div class="panel">
  <h1>CVBS <b>Post Designer</b></h1>
  <div class="tag">Build a carousel: add slides, edit each, export the set.</div>

  <div class="grp"><label>Slides in this carousel</label>
    <div class="slides" id="slides"></div>
    <div class="slideops">
      <button id="dupslide">Duplicate</button><button id="delslide">Delete</button>
      <button id="mvl">◀ Move</button><button id="mvr">Move ▶</button>
    </div>
  </div>

  <div class="grp"><label>Template (for this slide)</label><div class="tmpls" id="tmpls"></div></div>
  <div class="grp"><label>Format (whole carousel)</label><div class="seg" id="formats"></div></div>
  <div class="grp"><label>Align</label><div class="seg" id="aligns"></div></div>

  <div class="grp" id="photogrp"><label>Photo</label>
    <div class="photos" id="photos"></div>
    <label class="up">Upload photo<input type="file" id="upload" accept="image/*" hidden></label>
    <div class="slider" style="margin-top:12px"><span style="font-size:11px;color:#8aa0b0">POS</span><input type="range" id="posY" min="0" max="100" value="40"></div>
    <div class="slider"><span style="font-size:11px;color:#8aa0b0">DIM</span><input type="range" id="scrim" min="20" max="100" value="82"></div>
  </div>

  <div class="grp"><label>Content</label><div id="fields"></div></div>
  <div class="grp"><label class="chk"><input type="checkbox" id="li"> LinkedIn footer (company name)</label></div>

  <div class="dl">
    <button id="downloadAll">Download carousel (.zip)</button>
    <button id="downloadOne" class="secondary">Download this slide only</button>
    <div class="hint">Tip: *asterisks* colour a word teal. Slide 1 shows Swipe; later slides show progress dots automatically.</div>
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

<script>__JSZIP__</script>
<script>__HTI__</script>
<script>
const PHOTOS=__PHOTOS__, LOGOW="__LOGOW__", LOGOD="__LOGOD__";
const ARROW='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>';
const PIN='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s7-5.5 7-11a7 7 0 0 0-14 0c0 5.5 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/></svg>';
const esc=s=>(s||"").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
const rich=s=>esc(s).replace(/\*(.+?)\*/g,'<span class="accent">$1</span>').replace(/\n/g,"<br>");
const chip=t=>`<div class="chip">${esc(t)}</div>`;
const evbadge=t=>`<div class="evbadge">${esc(t).replace(/\s\|\s/,' <span class="dot"></span> ')}</div>`;
const filebadge=(a,b)=>`<div class="filebadge"><span class="a">${esc(a)}</span><span class="b">${esc(b)}</span></div>`;
const loc=t=>`<div class="loc2">${PIN} ${esc(t)}</div>`;
const tag2=t=>`<div class="tag2">${esc(t)}</div>`;
const pricePill=(p,b)=>`<div class="glass pricebox"><div class="price"><span class="pre">${esc(p)}</span><span class="big">${esc(b)}</span></div></div>`;
const specbar=a=>`<div class="specbar">${a.map(x=>`<div class="s"><div class="n">${esc(x[0])}</div><div class="l">${esc(x[1])}</div></div>`).join("")}</div>`;
let RCTX={i:0,n:1};
function dotsHtml(){let d="";for(let k=0;k<RCTX.n;k++)d+=`<span class="dot${k===RCTX.i?' on':''}"></span>`;return `<div class="dots">${d}</div>`;}
function foot(){const light=T[cur().template].bg==='stone';
  if(carousel.linkedin) return `<div class="foot lfoot"><img src="${light?LOGOD:LOGOW}"><div class="nm">CVBS<span>Conference Venues &amp; Booking Services</span></div></div>`;
  const right=(RCTX.n>1 && RCTX.i>0)?dotsHtml():`<span class="swipe">Swipe ${ARROW}</span>`;
  return `<div class="foot"><img src="${light?LOGOD:LOGOW}"><span class="url">conferencevenues.com</span>${right}</div>`;}
const F=(k)=>cur().fields[k]||"";

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
 content:{name:"› Content page",bg:"photo",render:()=>`<div class="eyebrow">${esc(F('eyebrow'))}</div><div class="fill"></div><div class="hl h-md">${rich(F('headline'))}</div><div class="sub">${rich(F('body'))}</div><div style="height:28px"></div>${foot()}`,
   def:{eyebrow:"The brief",headline:"A two-day conference\nfor *140 people*.",body:"Plenary plus three breakout rooms, full catering and rooms for interstate delegates."},photo:"crown"},
 point:{name:"› Numbered point",bg:"photo",render:()=>`<div class="fill"></div><div class="bignum" style="font-size:200px">${esc(F('number'))}</div><div class="hl h-md" style="margin-top:8px">${rich(F('headline'))}</div><div class="sub">${rich(F('body'))}</div><div style="height:28px"></div>${foot()}`,
   def:{number:"01",headline:"Booking the first\nvenue that says *yes*.",body:"The fastest option is rarely the best value. One comparison usually moves the price."},photo:"hyatt"},
 quote:{name:"› Quote",bg:"navy",render:()=>`<div class="eyebrow">${esc(F('eyebrow'))}</div><div class="fill"></div><div class="hl h-lg">${rich(F('quote'))}</div><div class="sub">${esc(F('attribution'))}</div><div class="fill"></div>${foot()}`,
   def:{eyebrow:"Client words",quote:"“They held the room\nbefore I'd finished\nthe *brief*.”",attribution:"Events Manager, national association"}},
 cta:{name:"› Call to action",bg:"navy",render:()=>`<div class="eyebrow">${esc(F('eyebrow'))}</div><div class="fill"></div><div class="hl h-lg">${rich(F('headline'))}</div><div class="sub">${rich(F('body'))}</div><div class="btn">${esc(F('button'))} ${ARROW}</div><div class="fill"></div>${foot()}`,
   def:{eyebrow:"Your event next",headline:"Planning something\n*like this?*",body:"Send us the brief. We'll come back with a shortlist worth your time.",button:"Start your brief"}},
};
const FIELD_LABELS={badge:"Eyebrow / badge",headline:"Headline",sub:"Sub-line",pricePre:"Price label",priceBig:"Price",seriesNo:"File number",location:"Location",eyebrow:"Eyebrow",number:"Big number",tag:"Tag text",
 body:"Body text",quote:"Quote",attribution:"Attribution",button:"Button text",
 s1n:"Stat 1",s1l:"Label 1",s2n:"Stat 2",s2l:"Label 2",s3n:"Stat 3",s3l:"Label 3"};
const AREA=new Set(["headline","sub","body","quote"]);
const PAIRS=[["s1n","s1l"],["s2n","s2l"],["s3n","s3l"]];
const CENTER_DEFAULT=new Set(["positioning","quote","cta","roundup"]);

function newSlide(tmpl){const t=T[tmpl];return{template:tmpl,align:CENTER_DEFAULT.has(tmpl)?"center":"left",photo:t.photo?PHOTOS[t.photo]:null,posY:40,scrim:82,fields:Object.assign({},t.def)};}
let carousel={format:"ig",linkedin:false,slides:[newSlide("offer")],current:0};
const cur=()=>carousel.slides[carousel.current];

function setTemplate(k){const s=cur();s.template=k;s.fields=Object.assign({},T[k].def);if(T[k].photo)s.photo=PHOTOS[T[k].photo];s.align=CENTER_DEFAULT.has(k)?"center":"left";refreshAll();}

function buildSlides(){const c=document.getElementById('slides');c.innerHTML="";
 carousel.slides.forEach((s,i)=>{const b=document.createElement('button');b.className="slidechip"+(i===carousel.current?" on":"");
  b.innerHTML=`<span class="sn">${i+1}</span><span class="st">${T[s.template].name.replace('› ','')}</span>`;
  b.onclick=()=>{carousel.current=i;refreshAll();};c.appendChild(b);});
 const add=document.createElement('button');add.className="slideadd";add.textContent="+";add.title="Add slide";add.onclick=addSlide;c.appendChild(add);}
function addSlide(){carousel.slides.splice(carousel.current+1,0,newSlide("content"));carousel.current++;refreshAll();}
function dupSlide(){const s=JSON.parse(JSON.stringify(cur()));carousel.slides.splice(carousel.current+1,0,s);carousel.current++;refreshAll();}
function delSlide(){if(carousel.slides.length<=1)return;carousel.slides.splice(carousel.current,1);carousel.current=Math.max(0,carousel.current-1);refreshAll();}
function moveSlide(d){const j=carousel.current+d;if(j<0||j>=carousel.slides.length)return;const s=carousel.slides.splice(carousel.current,1)[0];carousel.slides.splice(j,0,s);carousel.current=j;refreshAll();}
document.getElementById('dupslide').onclick=dupSlide;
document.getElementById('delslide').onclick=delSlide;
document.getElementById('mvl').onclick=()=>moveSlide(-1);
document.getElementById('mvr').onclick=()=>moveSlide(1);

function buildTemplateButtons(){const c=document.getElementById('tmpls');c.innerHTML="";
 Object.keys(T).forEach(k=>{const b=document.createElement('button');b.textContent=T[k].name;b.className=k===cur().template?"on":"";
  b.onclick=()=>setTemplate(k);c.appendChild(b);});}
const ALIGNS=[["left","Left"],["center","Centre"]];
function buildAlignButtons(){const c=document.getElementById('aligns');c.innerHTML="";
 ALIGNS.forEach(([k,n])=>{const b=document.createElement('button');b.textContent=n;b.className=k===cur().align?"on":"";
  b.onclick=()=>{cur().align=k;buildAlignButtons();render();};c.appendChild(b);});}
const FORMATS=[["ig","Instagram 4:5"],["square","Square"],["wide","LinkedIn wide"]];
function buildFormatButtons(){const c=document.getElementById('formats');c.innerHTML="";
 FORMATS.forEach(([k,n])=>{const b=document.createElement('button');b.textContent=n;b.className=k===carousel.format?"on":"";
  b.onclick=()=>{carousel.format=k;buildFormatButtons();render();};c.appendChild(b);});}

function buildFields(){const c=document.getElementById('fields');c.innerHTML="";const t=T[cur().template];
 const keys=Object.keys(t.def);const done=new Set();
 keys.forEach(k=>{if(done.has(k))return;const pair=PAIRS.find(p=>p[0]===k);
  if(pair){const wrap=document.createElement('div');wrap.className="row2";pair.forEach(pk=>{wrap.appendChild(makeField(pk));done.add(pk);});c.appendChild(wrap);return;}
  c.appendChild(makeField(k));done.add(k);});}
function makeField(k){const d=document.createElement('div');d.className="field";
 const lab=document.createElement('label');lab.textContent=FIELD_LABELS[k]||k;d.appendChild(lab);
 const el=document.createElement(AREA.has(k)?'textarea':'input');el.value=cur().fields[k]||"";
 el.oninput=()=>{cur().fields[k]=el.value;render();};d.appendChild(el);return d;}

function buildPhotoThumbs(){const c=document.getElementById('photos');c.innerHTML="";
 Object.keys(PHOTOS).forEach(k=>{const d=document.createElement('div');d.className="th"+(cur().photo===PHOTOS[k]?" on":"");
  d.style.backgroundImage=`url(${PHOTOS[k]})`;d.onclick=()=>{cur().photo=PHOTOS[k];buildPhotoThumbs();render();};c.appendChild(d);});}
document.getElementById('upload').onchange=e=>{const f=e.target.files[0];if(!f)return;const r=new FileReader();
 r.onload=()=>{cur().photo=r.result;buildPhotoThumbs();render();};r.readAsDataURL(f);};
document.getElementById('posY').oninput=e=>{cur().posY=+e.target.value;render();};
document.getElementById('scrim').oninput=e=>{cur().scrim=+e.target.value;render();};
document.getElementById('li').onchange=e=>{carousel.linkedin=e.target.checked;render();};

function togglePhoto(){document.getElementById('photogrp').style.display=T[cur().template].bg==='photo'?'block':'none';}

function render(){const s=cur(),t=T[s.template];const card=document.getElementById('card');
 RCTX={i:carousel.current,n:carousel.slides.length};
 card.className="card fmt-"+carousel.format+(t.bg==='stone'?" bg-stone":"");
 const bg=document.getElementById('bg'),scr=document.getElementById('scrim');
 if(t.bg==='photo'){bg.style.display=scr.style.display="block";bg.style.backgroundImage=`url(${s.photo})`;
   bg.style.backgroundPosition=`center ${s.posY}%`;
   const a=s.scrim/100, bot=Math.min(a+0.15,0.97);
   scr.style.background=`linear-gradient(180deg,rgba(6,30,59,${a*0.34}) 0%,rgba(6,30,59,${a*0.12}) 20%,rgba(6,30,59,${a*0.5}) 44%,rgba(6,30,59,${bot}) 73%,rgba(6,30,59,${bot}) 100%)`;
 } else {bg.style.display=scr.style.display="none";}
 const ct=document.getElementById('content');ct.className="content"+(s.align==='center'?" center":"");
 ct.innerHTML=t.render();
 fit();}

function refreshAll(){document.getElementById('posY').value=cur().posY;document.getElementById('scrim').value=cur().scrim;
 document.getElementById('li').checked=carousel.linkedin;
 buildSlides();buildTemplateButtons();buildFormatButtons();buildAlignButtons();buildFields();buildPhotoThumbs();togglePhoto();render();}

function fit(){const card=document.getElementById('card'),wrap=document.getElementById('stagewrap'),stage=document.getElementById('stage');
 const cw=card.offsetWidth,ch=card.offsetHeight,pad=48;
 const sc=Math.min((wrap.clientWidth-pad)/cw,(wrap.clientHeight-pad)/ch);
 stage.style.transform=`scale(${sc})`;stage.style.width=cw+"px";stage.style.height=ch+"px";}
window.addEventListener('resize',fit);

async function shot(){await document.fonts.ready;const c=document.getElementById('card');
 return await htmlToImage.toPng(c,{pixelRatio:2,cacheBust:true,width:c.offsetWidth,height:c.offsetHeight});}
document.getElementById('downloadOne').onclick=async(e)=>{const b=e.target,o=b.textContent;b.textContent="Rendering…";
 try{const u=await shot();const a=document.createElement('a');a.download=`cvbs-slide-${carousel.current+1}.png`;a.href=u;a.click();}catch(err){alert("Export error: "+err);}b.textContent=o;};
document.getElementById('downloadAll').onclick=async(e)=>{const b=e.target,o=b.textContent;const keep=carousel.current;const zip=new JSZip();
 try{for(let i=0;i<carousel.slides.length;i++){carousel.current=i;render();b.textContent=`Rendering ${i+1}/${carousel.slides.length}…`;
   await new Promise(r=>setTimeout(r,40));const u=await shot();zip.file(`slide-${String(i+1).padStart(2,'0')}.png`,u.split(",")[1],{base64:true});}
  const blob=await zip.generateAsync({type:"blob"});const a=document.createElement('a');a.download="cvbs-carousel.zip";a.href=URL.createObjectURL(blob);a.click();
 }catch(err){alert("Export error: "+err);} carousel.current=keep;refreshAll();b.textContent=o;};

refreshAll();setTimeout(fit,60);
</script></body></html>'''

HTML=(HTML.replace("__FONTCSS__",fontcss).replace("__JSZIP__",JSZIP).replace("__HTI__",HTI)
      .replace("__PHOTOS__",photos_js).replace("__LOGOW__",LOGOW).replace("__LOGOD__",LOGOD))
out=pathlib.Path("/sessions/peaceful-eager-allen/mnt/outputs/CVBS-Post-Designer.html")
out.write_text(HTML)
print("designer bytes:",len(HTML))
