#!/usr/bin/env python3
import base64, pathlib
A=pathlib.Path("/sessions/peaceful-eager-allen/mnt/outputs/designer_assets")
def b64(p): return base64.b64encode((A/p).read_bytes()).decode()
fontcss="".join(
 f"@font-face{{font-family:Inter;font-weight:{w};src:url(data:font/woff2;base64,{b64(f'inter-latin-{w}-normal.woff2')}) format('woff2')}}"
 for w in [400,500,600,700,800])
LOGOW="data:image/png;base64,"+b64("logo-white.png")

HTML=r'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>CVBS Digital Hub</title>
<style>
__FONTCSS__
:root{--teal:#3BC9D9;--teal-deep:#28A8B6;--navy:#0A2C52;--navy2:#061E3B;--stone:#EEF6F7}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Inter,system-ui,sans-serif;min-height:100vh;color:#eaf1f4;
 background:radial-gradient(70% 60% at 18% 12%,rgba(59,201,217,.16),transparent 60%),radial-gradient(60% 60% at 85% 90%,rgba(3,102,198,.20),transparent 60%),var(--navy);
 display:flex;flex-direction:column;align-items:center;justify-content:center;padding:40px 22px}
.wrap{width:100%;max-width:1080px}
.top{display:flex;align-items:center;gap:16px;margin-bottom:6px}
.top img{height:44px}
.ey{font-size:13px;letter-spacing:.24em;text-transform:uppercase;font-weight:700;color:var(--teal);margin-bottom:10px}
h1{font-size:clamp(34px,6vw,54px);font-weight:800;letter-spacing:-.03em;line-height:1.04}
h1 b{color:var(--teal);font-weight:800}
.sub{font-size:clamp(15px,2.4vw,19px);color:rgba(234,241,244,.72);margin-top:14px;max-width:52ch;line-height:1.5}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:40px}
@media(max-width:860px){.grid{grid-template-columns:1fr}}
.card{display:block;text-decoration:none;color:inherit;background:linear-gradient(160deg,rgba(255,255,255,.09),rgba(255,255,255,.04));
 border:1.5px solid rgba(255,255,255,.16);border-radius:22px;padding:30px 28px;transition:transform .25s,border-color .25s,background .25s}
.card:hover{transform:translateY(-4px);border-color:var(--teal);background:linear-gradient(160deg,rgba(59,201,217,.14),rgba(255,255,255,.05))}
.ic{width:56px;height:56px;border-radius:15px;display:grid;place-items:center;background:rgba(59,201,217,.16);border:1.5px solid rgba(59,201,217,.4);margin-bottom:20px}
.ic svg{width:28px;height:28px;color:var(--teal)}
.card h2{font-size:24px;font-weight:700;letter-spacing:-.02em}
.card p{font-size:14.5px;color:rgba(234,241,244,.66);margin-top:8px;line-height:1.5}
.go{display:inline-flex;align-items:center;gap:8px;margin-top:20px;font-size:14px;font-weight:700;color:var(--teal)}
.go svg{width:17px;height:17px}
.foot{margin-top:38px;font-size:12.5px;color:rgba(234,241,244,.45)}
</style></head>
<body><div class="wrap">
  <div class="top"><img src="__LOGOW__" alt="CVBS"></div>
  <div class="ey">Conference Venues &amp; Booking Services</div>
  <h1>CVBS <b>Digital Hub</b></h1>
  <div class="sub">Your in-house design tools. Build on-brand social carousels and email campaigns in minutes, no design software required.</div>
  <div class="grid">
    <a class="card" href="../Post-Designer/CVBS-Post-Designer.html">
      <div class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="3"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="M21 15l-5-5L5 21"/></svg></div>
      <h2>Social Post Designer</h2>
      <p>Instagram &amp; LinkedIn carousels. Pick a template, add your words and photos, export the whole set.</p>
      <span class="go">Open designer <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg></span>
    </a>
    <a class="card" href="../EDM-Designer/CVBS-EDM-Designer.html">
      <div class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg></div>
      <h2>EDM Designer</h2>
      <p>Venue offer &amp; monthly roundup emails. Fill in the details, copy the HTML, paste into Mailchimp.</p>
      <span class="go">Open designer <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg></span>
    </a>
    <a class="card" href="../Quote-Generator/CVBS-Quote-Generator.html">
      <div class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="3" width="14" height="18" rx="2"/><path d="M9 8h6M9 12h6M9 16h4"/></svg></div>
      <h2>Quote Generator</h2>
      <p>Itemised event quotes and venue comparison proposals. Fill in, then print or save as PDF.</p>
      <span class="go">Open generator <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg></span>
    </a>
  </div>
  <div class="foot">Internal tools · conferencevenues.com</div>
</div></body></html>'''
HTML=HTML.replace("__FONTCSS__",fontcss).replace("__LOGOW__",LOGOW)
pathlib.Path("/sessions/peaceful-eager-allen/mnt/outputs/hub-index.html").write_text(HTML)
print("hub bytes:",len(HTML))
