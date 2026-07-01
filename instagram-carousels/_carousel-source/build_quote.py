#!/usr/bin/env python3
import base64, pathlib
A=pathlib.Path("/sessions/peaceful-eager-allen/mnt/outputs/designer_assets")
def b64(p): return base64.b64encode((A/p).read_bytes()).decode()
fontcss="".join(
 f"@font-face{{font-family:Inter;font-weight:{w};font-style:normal;font-display:block;src:url(data:font/woff2;base64,{b64(f'inter-latin-{w}-normal.woff2')}) format('woff2')}}"
 for w in [400,500,600,700,800])
LOGOW="data:image/png;base64,"+b64("logo-white.png")

HTML=r'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>CVBS Quote Generator</title>
<style>
__FONTCSS__
:root{--teal:#3BC9D9;--teal-deep:#28A8B6;--navy:#0A2C52;--navy2:#061E3B;--brand:#0366C6;--stone:#EEF6F7;--ink:#0D1F2D;--line:#D6E7E9;--muted:#6E747B}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Inter,system-ui,sans-serif;background:#0b1622;color:#eef3f6;display:flex;height:100vh;overflow:hidden}
.panel{width:400px;flex:none;height:100vh;overflow-y:auto;background:#0e1b28;border-right:1px solid rgba(255,255,255,.08);padding:20px 20px 40px}
.panel h1{font-size:19px;font-weight:700;margin-bottom:3px}.panel h1 b{color:var(--teal)}
.panel .tag{font-size:12.5px;color:#8aa0b0;margin-bottom:16px}
.grp{margin-bottom:15px}
.grp>label{display:block;font-size:11px;text-transform:uppercase;letter-spacing:.12em;color:#8aa0b0;font-weight:700;margin-bottom:7px}
.seg{display:flex;gap:6px}
.seg button{flex:1;padding:10px 6px;font:inherit;font-size:12.5px;font-weight:600;color:#cfe0ea;background:#132535;border:1px solid rgba(255,255,255,.1);border-radius:9px;cursor:pointer}
.seg button.on{background:var(--teal);color:#05222a;border-color:var(--teal)}
.field{margin-bottom:10px}
.field label{display:block;font-size:12px;color:#a9bccb;margin-bottom:4px;font-weight:500}
.field input,.field textarea{width:100%;font:inherit;font-size:13px;color:#eef3f6;background:#0b1622;border:1px solid rgba(255,255,255,.14);border-radius:8px;padding:8px 10px}
.field textarea{min-height:52px;line-height:1.4;resize:vertical}
.field input:focus,.field textarea:focus{outline:none;border-color:var(--teal)}
.row2{display:flex;gap:8px}.row2>.field{flex:1}
.item{display:flex;gap:6px;align-items:flex-end;margin-bottom:7px}
.item .field{margin:0}.item .desc{flex:3}.item .qty{flex:1}.item .unit{flex:1.3}
.item .rm{flex:none;width:30px;height:34px;border:1px solid rgba(255,255,255,.14);background:#132535;color:#e77;border-radius:8px;cursor:pointer;font-size:16px}
.addbtn{width:100%;padding:9px;font:inherit;font-size:12.5px;font-weight:600;color:#cfe0ea;background:#132535;border:1px dashed rgba(255,255,255,.28);border-radius:9px;cursor:pointer;margin-top:2px}
.vbox{border:1px solid rgba(255,255,255,.1);border-radius:10px;padding:11px;margin-bottom:10px;background:#0c1a27}
.vbox .vt{font-size:11px;font-weight:700;color:var(--teal);text-transform:uppercase;letter-spacing:.1em;margin-bottom:8px}
.dl{position:sticky;bottom:0;background:#0e1b28;padding-top:12px;margin-top:6px}
.dl button{width:100%;padding:13px;font:inherit;font-size:14.5px;font-weight:700;color:#05222a;background:var(--teal);border:none;border-radius:11px;cursor:pointer}
.dl button.secondary{background:#173049;color:#cfe0ea;margin-top:8px;font-size:13px;padding:10px}
.hint{font-size:11.5px;color:#8aa0b0;margin-top:8px;line-height:1.4}
.stage{flex:1;height:100vh;overflow:auto;background:#c9d4dc;display:flex;justify-content:center;padding:26px}
/* ---- DOCUMENT ---- */
.doc{width:800px;flex:none;background:#fff;color:var(--ink);box-shadow:0 30px 70px -30px rgba(0,0,0,.5);align-self:flex-start;overflow:hidden}
.ey{display:inline-flex;align-items:center;gap:12px;font-size:12px;letter-spacing:.18em;text-transform:uppercase;color:var(--brand);font-weight:700}
.ey::before{content:"";width:26px;height:2px;border-radius:2px;background:var(--teal)}
.dh{background:var(--navy);color:#fff;padding:28px 44px;display:flex;justify-content:space-between;align-items:center}
.dh .lg img{height:38px;display:block}
.dh .lg .tl{font-size:11px;letter-spacing:.08em;color:rgba(255,255,255,.6);margin-top:9px;font-weight:500}
.dh .rt{text-align:right}
.dh .rt .k{display:inline-flex;align-items:center;gap:10px;font-size:12px;letter-spacing:.2em;text-transform:uppercase;color:var(--teal);font-weight:700}
.dh .rt .k::before{content:"";width:22px;height:2px;background:var(--teal);border-radius:2px}
.dh .rt .n{font-size:13px;color:rgba(255,255,255,.8);margin-top:9px;line-height:1.6}
.hero{background:var(--stone);padding:30px 44px;border-bottom:1px solid var(--line)}
.hero h1{font-size:34px;font-weight:800;letter-spacing:-.03em;line-height:1.08;color:var(--navy);margin:11px 0 0}
.facts{display:flex;flex-wrap:wrap;gap:8px;margin-top:16px}
.facts .f{display:inline-flex;align-items:center;gap:8px;font-size:13px;font-weight:600;color:var(--navy);background:#fff;border:1px solid var(--line);border-radius:999px;padding:7px 14px}
.facts .f .d{width:6px;height:6px;border-radius:50%;background:var(--teal)}
.dbody{padding:30px 44px}
.prep{font-size:13.5px;color:#37444f;padding-bottom:18px;border-bottom:1px solid var(--line)}
.prep b{color:var(--ink)}
table{width:100%;border-collapse:collapse;margin-top:22px}
th{font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);font-weight:700;text-align:left;padding:0 10px 12px;border-bottom:2px solid var(--navy)}
th.r,td.r{text-align:right}
tbody tr:nth-child(even){background:#f6fafb}
td{font-size:14px;padding:13px 10px;border-bottom:1px solid var(--line);color:var(--ink);vertical-align:top}
td.amt{font-weight:700;color:var(--navy)}
.totals{margin-top:18px;margin-left:auto;width:340px}
.totals .tr{display:flex;justify-content:space-between;padding:9px 10px;font-size:14px;color:#37444f}
.totals .tr.grand{background:var(--navy);color:#fff;border-radius:12px;padding:17px 20px;font-size:15px;font-weight:600;margin-top:8px;align-items:center;box-shadow:0 16px 30px -18px rgba(10,44,82,.6)}
.totals .tr.grand .big{font-size:27px;font-weight:800;color:var(--teal);letter-spacing:-.02em}
.totals .tr.grand small{font-weight:400;opacity:.7;font-size:11px}
.notebox{margin-top:26px;background:var(--stone);border:1px solid var(--line);border-radius:14px;padding:22px 24px}
.notebox .lbl{margin-bottom:10px}
.notebox p{font-size:13.5px;line-height:1.65;color:#37444f;white-space:pre-wrap}
.trust{display:flex;flex-wrap:wrap;gap:9px;margin-top:24px}
.tb{display:inline-flex;align-items:center;gap:8px;font-size:12px;font-weight:700;color:var(--navy);background:var(--stone);border:1px solid var(--line);border-radius:999px;padding:8px 14px}
.tb svg{width:15px;height:15px;color:var(--teal-deep)}
.vgrid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px;margin-top:24px}
.vcard{border:1px solid var(--line);border-radius:16px;overflow:hidden;position:relative;display:flex;flex-direction:column}
.vcard.pick{border-color:var(--teal);box-shadow:0 0 0 1.5px var(--teal)}
.vcard .tag{position:absolute;top:12px;right:12px;background:var(--teal);color:#06262b;font-size:10px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;padding:4px 9px;border-radius:6px}
.vcard .vch{background:var(--navy);padding:18px}
.vcard .vn{font-size:17px;font-weight:800;color:#fff;line-height:1.15}
.vcard .vl{font-size:12px;color:var(--teal);margin-top:4px;font-weight:600}
.vcard .vb{padding:18px;display:flex;flex-direction:column;flex:1}
.vcard .vspec{font-size:12.5px;color:#37444f;line-height:1.6;min-height:56px}
.vcard .vrate{font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:.08em;margin-top:14px;font-weight:600}
.vcard .vprice{font-size:28px;font-weight:800;color:var(--teal-deep);letter-spacing:-.02em}
.vcard .vnote{font-size:12px;color:#37444f;line-height:1.5;margin-top:12px;padding-top:12px;border-top:1px solid var(--line)}
.terms{margin-top:26px;padding-top:18px;border-top:1px solid var(--line);font-size:11.5px;line-height:1.6;color:var(--muted)}
.df{background:var(--navy2);color:rgba(255,255,255,.8);padding:22px 44px;font-size:12px;line-height:1.7}
.df b{color:#fff}.df .teal{color:var(--teal)}
.df .row{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px}
@media print{
 body{display:block;height:auto;background:#fff}
 .panel{display:none!important}
 .stage{padding:0;background:#fff;display:block;overflow:visible;height:auto}
 .doc{width:100%;box-shadow:none}
 @page{size:A4;margin:11mm}
}
</style></head>
<body>
<div class="panel">
  <h1>CVBS <b>Quote Generator</b></h1>
  <div class="tag">Fill it in, then Print / Save as PDF.</div>
  <div class="grp"><label>Quote type</label><div class="seg" id="modes"></div></div>
  <div id="fields"></div>
  <div class="dl">
    <button id="print">Print / Save as PDF</button>
    <button id="download" class="secondary">Download HTML</button>
    <div class="hint">Print → destination "Save as PDF" gives you a clean A4 document to email.</div>
  </div>
</div>
<div class="stage"><div class="doc" id="doc"></div></div>
<script>
const LOGOW="__LOGOW__";
const esc=s=>(s||"").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
const money=n=>"$"+(Number(String(n).replace(/[^0-9.]/g,''))||0).toLocaleString('en-AU',{minimumFractionDigits:2,maximumFractionDigits:2});
const num=n=>Number(String(n).replace(/[^0-9.]/g,''))||0;
const M=k=>state.meta[k]||"";
const TICK='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7"/></svg>';
const TRUST=`<div class="trust"><span class="tb">${TICK}Free to you</span><span class="tb">${TICK}Independent since 1989</span><span class="tb">${TICK}Shortlist in 48 hours</span></div>`;

function head(kind){return `<div class="dh"><div class="lg"><img src="${LOGOW}" alt="CVBS"><div class="tl">Conference Venues &amp; Booking Services</div></div>
 <div class="rt"><div class="k">${kind}</div><div class="n">${esc(M('quoteNo'))}<br>${esc(M('date'))}${M('validUntil')?`<br>Valid until ${esc(M('validUntil'))}`:""}</div></div></div>`;}
const fact=t=>`<span class="f"><span class="d"></span>${esc(t)}</span>`;
function hero(ey){return `<div class="hero"><div class="ey">${ey}</div><h1>${esc(M('event'))||"&nbsp;"}</h1>
 <div class="facts">${M('destination')?fact(M('destination')):""}${M('dates')?fact(M('dates')):""}${M('delegates')?fact(M('delegates')+' delegates'):""}</div></div>`;}
const prep=()=>`<div class="prep">Prepared for <b>${esc(M('client'))}</b>${M('company')?', '+esc(M('company')):""}.</div>`;
function foot(){return `<div class="df"><div class="row">
 <div><b>CVBS · Conference Venues &amp; Booking Services</b><br>${esc(M('contactName'))}${M('contactPhone')?` · ${esc(M('contactPhone'))}`:""}${M('contactEmail')?` · <span class="teal">${esc(M('contactEmail'))}</span>`:""}</div>
 <div style="text-align:right"><b>Free to you.</b><br>We're paid by the venue, never by you.</div></div></div>`;}

function buildItemised(){let sub=0;
 const rows=state.items.map(it=>{const amt=num(it.qty)*num(it.unit);sub+=amt;
  return `<tr><td>${esc(it.desc)||"&nbsp;"}</td><td class="r">${esc(it.qty)}</td><td class="r">${it.unit?money(it.unit):""}</td><td class="r amt">${money(amt)}</td></tr>`;}).join("");
 const gst=sub*0.1, total=sub+gst;
 return `${head("Estimate")}${hero("Event estimate")}<div class="dbody">${prep()}
  <table><thead><tr><th>Description</th><th class="r">Qty</th><th class="r">Unit</th><th class="r">Amount</th></tr></thead><tbody>${rows}</tbody></table>
  <div class="totals">
   <div class="tr"><span>Subtotal</span><span>${money(sub)}</span></div>
   <div class="tr"><span>GST (10%)</span><span>${money(gst)}</span></div>
   <div class="tr grand"><span>Estimated total <small>incl. GST</small></span><span class="big">${money(total)}</span></div>
  </div>
  ${M('notes')?`<div class="notebox"><div class="ey lbl">Notes</div><p>${esc(M('notes'))}</p></div>`:""}
  ${TRUST}
  <div class="terms">This is an estimate based on the details supplied and current venue rates; final pricing is confirmed on booking. Figures are indicative and subject to availability and change. CVBS is an independent venue finding service, free to the client.</div>
  </div>${foot()}`;}

function buildProposal(){
 const cards=state.venues.filter(v=>v.name||v.price).map((v,i)=>`<div class="vcard${i===0?' pick':''}">${i===0?'<span class="tag">Our pick</span>':''}<div class="vch"><div class="vn">${esc(v.name)||"&nbsp;"}</div><div class="vl">${esc(v.location)}</div></div>
  <div class="vb"><div class="vspec">${esc(v.spec).split("\n").join("<br>")}</div>
  <div class="vrate">${esc(v.rate)}</div><div class="vprice">${v.price?money(v.price):""}</div>
  ${v.note?`<div class="vnote">${esc(v.note)}</div>`:""}</div></div>`).join("");
 return `${head("Proposal")}${hero("Venue proposal")}<div class="dbody">${prep()}
  <div class="vgrid">${cards}</div>
  ${M('recommendation')?`<div class="notebox"><div class="ey lbl">Our recommendation</div><p>${esc(M('recommendation'))}</p></div>`:""}
  ${TRUST}
  <div class="terms">Estimated totals are indicative, based on the brief and current venue rates, and confirmed on booking. Subject to availability. CVBS is an independent venue finding service, free to the client.</div>
  </div>${foot()}`;}

const DEF_META={quoteNo:"Q-2026-014",date:"1 July 2026",validUntil:"31 July 2026",client:"Jane Smith",company:"Acme Corporation",
 event:"National Sales Conference",destination:"Sydney, NSW",dates:"14–15 October 2026",delegates:"140",
 contactName:"Chantelle",contactPhone:"0414 784 999",contactEmail:"hello@conferencevenues.com",
 notes:"Includes full-day delegate package, plenary and three breakout rooms. Accommodation held on a rooming list; final numbers due 30 days out.",
 recommendation:"Kimpton Margot is our pick for character and CBD access at the winter rate; Hyatt Place offers the best value and airport convenience if budget leads."};
const DEF_ITEMS=[{desc:"Day delegate package",qty:"140",unit:"110"},{desc:"Accommodation (twin share, per night)",qty:"70",unit:"260"},{desc:"Plenary room hire (2 days)",qty:"2",unit:"1200"},{desc:"AV package",qty:"1",unit:"3500"}];
const DEF_VENUES=[
 {name:"Kimpton Margot",location:"Sydney CBD",spec:"Up to 120 delegates\nHeritage hotel, CBD\nLuke Mangan catering",rate:"Day delegate from",price:"110",note:"Winter rate, April–June. Most character."},
 {name:"Hyatt Place",location:"Essendon Fields, VIC",spec:"Up to 1,500 guests\n1,700 sqm pillarless\n10 min from airport",rate:"Day delegate from",price:"95",note:"Best value and access."},
 {name:"Crown Sydney",location:"Barangaroo, NSW",spec:"Premium harbour venue\nLarge ballroom\nHarbour views",rate:"Day delegate from",price:"165",note:"Flagship option."}];

let state={mode:"itemised",meta:Object.assign({},DEF_META),items:JSON.parse(JSON.stringify(DEF_ITEMS)),venues:JSON.parse(JSON.stringify(DEF_VENUES))};
const LABEL={quoteNo:"Quote number",date:"Date",validUntil:"Valid until",client:"Client name",company:"Company",event:"Event",destination:"Destination",dates:"Dates",delegates:"Delegates",contactName:"Your name",contactPhone:"Phone",contactEmail:"Email",notes:"Notes",recommendation:"Recommendation"};

function buildModes(){const c=document.getElementById('modes');c.innerHTML="";
 [["itemised","Itemised quote"],["proposal","Venue comparison"]].forEach(([k,n])=>{const b=document.createElement('button');b.textContent=n;b.className=k===state.mode?"on":"";
  b.onclick=()=>{state.mode=k;buildModes();buildFields();render();};c.appendChild(b);});}
function fld(k){const d=document.createElement('div');d.className="field";const l=document.createElement('label');l.textContent=LABEL[k]||k;d.appendChild(l);
 const area=(k==='notes'||k==='recommendation');const el=document.createElement(area?'textarea':'input');el.value=state.meta[k]||"";
 el.oninput=()=>{state.meta[k]=el.value;render();};d.appendChild(el);return d;}
function twoCol(a,b){const w=document.createElement('div');w.className="row2";w.appendChild(fld(a));w.appendChild(fld(b));return w;}
function fldObj(lbl,obj,key,area){const d=document.createElement('div');d.className="field";const l=document.createElement('label');l.textContent=lbl;d.appendChild(l);
 const el=document.createElement(area?'textarea':'input');el.value=obj[key]||"";el.oninput=()=>{obj[key]=el.value;render();};d.appendChild(el);return d;}
function fld2(lbl,obj,key,cls){const d=document.createElement('div');d.className="field "+cls;const l=document.createElement('label');l.textContent=lbl;d.appendChild(l);
 const el=document.createElement('input');el.value=obj[key]||"";el.oninput=()=>{obj[key]=el.value;render();};d.appendChild(el);return d;}

function buildFields(){const c=document.getElementById('fields');c.innerHTML="";
 c.appendChild(twoCol('quoteNo','date'));c.appendChild(fld('validUntil'));
 c.appendChild(twoCol('client','company'));c.appendChild(fld('event'));
 c.appendChild(twoCol('destination','dates'));c.appendChild(fld('delegates'));
 if(state.mode==='itemised'){
   const g=document.createElement('div');g.className="grp";g.innerHTML='<label>Line items</label>';const list=document.createElement('div');
   state.items.forEach((it,i)=>{const row=document.createElement('div');row.className="item";
     row.append(fld2("Description",it,'desc','desc'),fld2("Qty",it,'qty','qty'),fld2("Unit $",it,'unit','unit'));
     const rm=document.createElement('button');rm.className="rm";rm.textContent="×";rm.onclick=()=>{state.items.splice(i,1);buildFields();render();};
     row.appendChild(rm);list.appendChild(row);});
   g.appendChild(list);
   const add=document.createElement('button');add.className="addbtn";add.textContent="+ Add line";add.onclick=()=>{state.items.push({desc:"",qty:"1",unit:"0"});buildFields();render();};
   g.appendChild(add);c.appendChild(g);c.appendChild(fld('notes'));
 } else {
   state.venues.forEach((v,i)=>{const box=document.createElement('div');box.className="vbox";box.innerHTML=`<div class="vt">Venue ${i+1}${i===0?' · our pick':''}</div>`;
     box.appendChild(fldObj("Venue name",v,'name'));box.appendChild(fldObj("Location",v,'location'));
     box.appendChild(fldObj("Key specs (one per line)",v,'spec',true));
     box.appendChild(fldObj("Rate label",v,'rate'));box.appendChild(fldObj("Price $",v,'price'));box.appendChild(fldObj("Note",v,'note'));
     c.appendChild(box);});
   c.appendChild(fld('recommendation'));
 }
 const g2=document.createElement('div');g2.className="grp";g2.innerHTML='<label>Your contact details</label>';
 g2.appendChild(fld('contactName'));g2.appendChild(twoCol('contactPhone','contactEmail'));c.appendChild(g2);
}
function render(){document.getElementById('doc').innerHTML=state.mode==='itemised'?buildItemised():buildProposal();}
document.getElementById('print').onclick=()=>window.print();
document.getElementById('download').onclick=()=>{const html="<!doctype html><html><head><meta charset='utf-8'><style>"+document.querySelector('style').innerHTML+"</style></head><body><div class='stage' style='background:#fff;padding:0'>"+document.getElementById('doc').outerHTML+"</div></body></html>";
 const blob=new Blob([html],{type:"text/html"});const a=document.createElement('a');a.download=`cvbs-${state.mode}-quote.html`;a.href=URL.createObjectURL(blob);a.click();};
buildModes();buildFields();render();
</script></body></html>'''
HTML=HTML.replace("__FONTCSS__",fontcss).replace("__LOGOW__",LOGOW)
pathlib.Path("/sessions/peaceful-eager-allen/mnt/outputs/CVBS-Quote-Generator.html").write_text(HTML)
print("quote bytes:",len(HTML))
