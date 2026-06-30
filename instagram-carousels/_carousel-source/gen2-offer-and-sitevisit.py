#!/usr/bin/env python3
# CVBS glass carousels: Offer/EDM (Kimpton) + Site Visit (Hyatt Place)
CSS = """
@font-face{font-family:Inter;font-weight:400;src:url('../fonts/Inter-400.ttf')}
@font-face{font-family:Inter;font-weight:500;src:url('../fonts/Inter-500.ttf')}
@font-face{font-family:Inter;font-weight:600;src:url('../fonts/Inter-600.ttf')}
@font-face{font-family:Inter;font-weight:700;src:url('../fonts/Inter-700.ttf')}
@font-face{font-family:Inter;font-weight:800;src:url('../fonts/Inter-800.ttf')}
:root{--teal:#3BC9D9;--teal-deep:#28A8B6;--navy:#0D2233;--navy2:#071520;--stone:#F4F1EA}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Inter,sans-serif;-webkit-font-smoothing:antialiased}
.slide{width:1080px;height:1350px;position:relative;overflow:hidden;
 display:flex;flex-direction:column;padding:80px 74px 72px;color:#fff}
.slide>*{position:relative;z-index:2}
.bg{position:absolute;inset:0;z-index:0;background-size:cover;background-position:center;transform:scale(1.06)}
.scrim{position:absolute;inset:0;z-index:1;
 background:linear-gradient(180deg,rgba(7,21,32,.46) 0%,rgba(7,21,32,.20) 30%,rgba(7,21,32,.40) 62%,rgba(7,21,32,.86) 100%)}
.scrim-soft{background:linear-gradient(180deg,rgba(7,21,32,.34) 0%,rgba(7,21,32,.16) 45%,rgba(7,21,32,.74) 100%)}
.scrim-deep{background:linear-gradient(180deg,rgba(7,21,32,.62) 0%,rgba(7,21,32,.55) 50%,rgba(7,21,32,.82) 100%)}
.fill{flex:1}
.s8{height:18px}.s16{height:30px}.s24{height:44px}.s32{height:60px}
/* glass */
.glass{background:rgba(255,255,255,.13);
 backdrop-filter:blur(34px) saturate(155%);-webkit-backdrop-filter:blur(34px) saturate(155%);
 border:1.5px solid rgba(255,255,255,.30);border-radius:34px;
 box-shadow:0 44px 80px -34px rgba(0,0,0,.70), inset 0 2px 0 rgba(255,255,255,.42), inset 0 -1px 0 rgba(255,255,255,.07)}
.glass-tint{background:rgba(11,28,42,.42);
 backdrop-filter:blur(30px) saturate(150%);-webkit-backdrop-filter:blur(30px) saturate(150%);
 border:1.5px solid rgba(255,255,255,.20);border-radius:34px;
 box-shadow:0 44px 80px -34px rgba(0,0,0,.7), inset 0 2px 0 rgba(255,255,255,.28)}
.pad{padding:56px 56px}
.chip{display:inline-flex;align-items:center;gap:16px;align-self:flex-start;
 padding:18px 28px;border-radius:999px;font-size:23px;font-weight:600;
 letter-spacing:.2em;text-transform:uppercase;color:#fff;
 background:rgba(255,255,255,.14);backdrop-filter:blur(24px) saturate(150%);
 -webkit-backdrop-filter:blur(24px) saturate(150%);
 border:1.5px solid rgba(255,255,255,.32);box-shadow:inset 0 1.5px 0 rgba(255,255,255,.45)}
.chip::before{content:"";width:34px;height:3px;border-radius:2px;background:var(--teal)}
.chip.plain::before{display:none}
/* type */
.h1{font-size:90px;font-weight:700;line-height:1.02;letter-spacing:-.035em;
 text-shadow:0 4px 30px rgba(0,0,0,.4)}
.h2{font-size:62px;font-weight:700;line-height:1.06;letter-spacing:-.03em}
.h3{font-size:44px;font-weight:700;line-height:1.12;letter-spacing:-.02em}
.accent{color:var(--teal)}
.lead{font-size:33px;line-height:1.5;font-weight:400;color:rgba(255,255,255,.9)}
.sub{font-size:31px;line-height:1.45;font-weight:400;color:rgba(255,255,255,.86)}
.kick{font-size:24px;font-weight:600;letter-spacing:.22em;text-transform:uppercase;color:var(--teal)}
.kick.bar{display:inline-flex;align-items:center;gap:16px}
.kick.bar::before{content:"";width:40px;height:3px;border-radius:2px;background:var(--teal)}
/* price pill */
.price{display:flex;align-items:baseline;gap:18px}
.price .pre{font-size:28px;font-weight:500;color:rgba(255,255,255,.82);letter-spacing:.02em}
.price .big{font-size:74px;font-weight:800;letter-spacing:-.03em;color:var(--teal)}
/* list */
.li{display:flex;gap:24px;align-items:flex-start}
.li+.li{margin-top:34px}
.li .ic{flex:none;width:52px;height:52px;border-radius:50%;display:grid;place-items:center;
 background:rgba(59,201,217,.22);color:var(--teal);border:1.5px solid rgba(59,201,217,.45)}
.li .ic svg{width:28px;height:28px}
.li .tx{font-size:34px;font-weight:600;line-height:1.3;padding-top:6px}
/* stat grid */
.stats{display:grid;grid-template-columns:1fr 1fr;gap:0}
.stat{padding:40px 36px}
.stat .n{font-size:72px;font-weight:800;letter-spacing:-.04em;color:var(--teal);line-height:.95}
.stat .l{font-size:27px;font-weight:500;color:rgba(255,255,255,.86);margin-top:14px;line-height:1.3}
.stat.br{border-right:1.5px solid rgba(255,255,255,.18)}
.stat.bt{border-top:1.5px solid rgba(255,255,255,.18)}
/* cta pill */
.pill{display:inline-flex;align-items:center;gap:18px;align-self:flex-start;
 background:var(--teal-deep);color:#fff;font-size:33px;font-weight:600;
 padding:30px 46px;border-radius:18px;box-shadow:0 24px 50px -18px rgba(0,0,0,.6)}
.pill svg{width:30px;height:30px}
.trust{display:flex;gap:26px;flex-wrap:wrap;font-size:25px;color:rgba(255,255,255,.9);font-weight:500}
.trust .t{display:inline-flex;align-items:center;gap:12px}
.trust svg{width:25px;height:25px;color:var(--teal)}
/* footer */
.foot{display:flex;align-items:center;justify-content:space-between;
 padding-top:30px;border-top:1px solid rgba(255,255,255,.22)}
.foot img{height:48px}
.foot .url{font-size:24px;font-weight:600;color:rgba(255,255,255,.88)}
.swipe{display:inline-flex;align-items:center;gap:14px;font-size:25px;font-weight:600;color:var(--teal)}
.swipe svg{width:30px;height:30px}
.dots{display:flex;gap:11px;align-items:center}
.dot{width:11px;height:11px;border-radius:50%;background:rgba(255,255,255,.32)}
.dot.on{background:var(--teal);width:30px;border-radius:6px}
"""
ARROW='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
CHK='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7"/></svg>'
TICK='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M8.5 12.5l2.5 2.5 4.5-5"/></svg>'
PIN='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s7-5.5 7-11a7 7 0 0 0-14 0c0 5.5 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/></svg>'

SL=[]
def add(name,inner): SL.append((name,f'<div class="slide" id="{name}">{inner}</div>'))
def bg(img,pos="center",scrim="scrim"):
    return f'<div class="bg" style="background-image:url(../assets/{img});background-position:{pos}"></div><div class="scrim {scrim}"></div>'
def foot(n,i,right=None):
    r=right if right is not None else '<div class="dots">'+''.join(f'<span class="dot{" on" if k==i else ""}"></span>' for k in range(n))+'</div>'
    return f'<div class="foot"><img src="../assets/logo-white.png"><span class="url">conferencevenues.com</span>{r}</div>'
def swipe(): return f'<span class="swipe">Swipe {ARROW}</span>'

# ============================== OFFER / EDM — Kimpton Margot
O="offer_kimpton"; N=6; IMG="kimpton.jpg"
add(f"{O}_1", f"""
 {bg(IMG,"center 30%","scrim")}
 <div class="chip">Venue offer &middot; Sydney CBD</div>
 <div class="fill"></div>
 <div class="h1">Winter at<br>Kimpton <span class="accent">Margot</span>.</div>
 <div class="s24"></div>
 <div class="glass" style="align-self:flex-start;padding:30px 40px;border-radius:24px">
   <div class="price"><span class="pre">Day delegate from</span><span class="big">$110pp</span></div>
 </div>
 <div class="s32"></div>
 {foot(N,0,swipe())}
""")
add(f"{O}_2", f"""
 {bg(IMG,"center 55%","scrim-deep")}
 <div class="fill"></div>
 <div class="glass pad">
   <div class="kick bar">The offer</div>
   <div class="s24"></div>
   <div class="h2">A full winter day<br>delegate package,<br><span class="accent">$110 per person</span>.</div>
   <div class="s16"></div>
   <div class="lead">Available April to June 2026. A limited winter rate at one of Sydney's most characterful heritage hotels.</div>
 </div>
 <div class="fill"></div>
 {foot(N,1)}
""")
add(f"{O}_3", f"""
 {bg(IMG,"center 40%","scrim-deep")}
 <div class="kick bar">What's included</div>
 <div class="s24"></div>
 <div class="glass pad">
   <div class="li"><span class="ic">{CHK}</span><span class="tx">Seasonal menus inspired by Luke Mangan's modern Australian cuisine</span></div>
   <div class="li"><span class="ic">{CHK}</span><span class="tx">Barista coffee and juice shots on arrival</span></div>
   <div class="li"><span class="ic">{CHK}</span><span class="tx">A plated working lunch, not a buffet scramble</span></div>
   <div class="li"><span class="ic">{CHK}</span><span class="tx">Full-service day delegate, start to finish</span></div>
 </div>
 <div class="fill"></div>
 {foot(N,2)}
""")
add(f"{O}_4", f"""
 {bg(IMG,"center 25%","scrim-deep")}
 <div class="fill"></div>
 <div class="glass-tint pad">
   <div class="kick bar">Prefer something smaller</div>
   <div class="s24"></div>
   <div class="h3">Boardroom meetings in a suite</div>
   <div class="s16"></div>
   <div class="sub">The Hammond or Budden Suite with an executive day delegate package: barista coffee, a plated lunch, a 75-inch screen, and an optional overnight stay.</div>
 </div>
 <div class="fill"></div>
 {foot(N,3)}
""")
add(f"{O}_5", f"""
 {bg(IMG,"center 60%","scrim-deep")}
 <div class="fill"></div>
 <div class="glass pad">
   <div class="kick bar">Why book through us</div>
   <div class="s24"></div>
   <div class="h2">Same rate.<br><span class="accent">Zero admin.</span></div>
   <div class="s16"></div>
   <div class="lead">We hold the date, handle the contract and tie off the run sheet. Free to you, because the venue pays us.</div>
 </div>
 <div class="fill"></div>
 {foot(N,4)}
""")
add(f"{O}_6", f"""
 {bg(IMG,"center 35%","scrim-deep")}
 <div class="fill"></div>
 <div class="chip plain" style="background:rgba(59,201,217,.18);border-color:rgba(59,201,217,.5)">Limited winter dates</div>
 <div class="s24"></div>
 <div class="h1">Want this<br><span class="accent">rate?</span></div>
 <div class="s16"></div>
 <div class="lead">Send us the dates and numbers. We'll secure it and come back within 48 hours.</div>
 <div class="s32"></div>
 <span class="pill">Start your brief {ARROW}</span>
 <div class="s24"></div>
 <div class="trust"><span class="t">{TICK} Free to you</span><span class="t">{TICK} Independent since 1989</span></div>
 <div class="fill"></div>
 {foot(N,5)}
""")

# ============================== SITE VISIT — Hyatt Place Essendon Fields
V="sitevisit_hyatt"; NV=6; VIMG="hyatt.jpg"
add(f"{V}_1", f"""
 {bg(VIMG,"center 35%","scrim")}
 <div class="chip"><span style="display:inline-flex;align-items:center;gap:10px">Site visit &middot; Melbourne</span></div>
 <div class="fill"></div>
 <div class="h1">We checked out<br>Hyatt Place,<br><span class="accent">Essendon Fields</span>.</div>
 <div class="s16"></div>
 <div class="lead">Notes from the floor, for your next conference.</div>
 <div class="s32"></div>
 {foot(NV,0,swipe())}
""")
add(f"{V}_2", f"""
 {bg(VIMG,"center 55%","scrim-deep")}
 <div class="fill"></div>
 <div class="glass pad">
   <div class="kick bar">First impression</div>
   <div class="s24"></div>
   <div class="h2">Easy in,<br><span class="accent">easy out</span>.</div>
   <div class="s16"></div>
   <div class="lead">Ten minutes from Melbourne Airport, twenty from the CBD, with a complimentary shuttle. Painless for interstate delegates.</div>
 </div>
 <div class="fill"></div>
 {foot(NV,1)}
""")
add(f"{V}_3", f"""
 {bg(VIMG,"center 30%","scrim-deep")}
 <div class="kick bar">The numbers</div>
 <div class="s24"></div>
 <div class="glass" style="padding:14px 18px">
   <div class="stats">
     <div class="stat br"><div class="n">1,700<span style="font-size:38px">+</span></div><div class="l">sqm of pillarless space</div></div>
     <div class="stat"><div class="n">1,500</div><div class="l">guests at capacity</div></div>
     <div class="stat br bt"><div class="n">6</div><div class="l">flexible event rooms</div></div>
     <div class="stat bt"><div class="n">166</div><div class="l">contemporary guestrooms</div></div>
   </div>
 </div>
 <div class="fill"></div>
 {foot(NV,2)}
""")
add(f"{V}_4", f"""
 {bg(VIMG,"center 45%","scrim-deep")}
 <div class="kick bar">What stood out</div>
 <div class="s24"></div>
 <div class="glass pad">
   <div class="li"><span class="ic">{CHK}</span><span class="tx">Light-filled, genuinely modern rooms</span></div>
   <div class="li"><span class="ic">{CHK}</span><span class="tx">Current AV with in-house support on site</span></div>
   <div class="li"><span class="ic">{CHK}</span><span class="tx">Premium catering, not function-room standard</span></div>
   <div class="li"><span class="ic">{CHK}</span><span class="tx">One team running the whole event</span></div>
 </div>
 <div class="fill"></div>
 {foot(NV,3)}
""")
add(f"{V}_5", f"""
 {bg(VIMG,"center 60%","scrim-deep")}
 <div class="fill"></div>
 <div class="glass-tint pad">
   <div class="kick bar">Right for</div>
   <div class="s24"></div>
   <div class="h3">Airport-close conferences that still want polish</div>
   <div class="s16"></div>
   <div class="sub">Conferences, showcases and multi-day offsites that need the convenience of the airport without paying CBD rates.</div>
 </div>
 <div class="fill"></div>
 {foot(NV,4)}
""")
add(f"{V}_6", f"""
 {bg(VIMG,"center 35%","scrim-deep")}
 <div class="fill"></div>
 <div class="chip plain" style="background:rgba(59,201,217,.18);border-color:rgba(59,201,217,.5)">We'll arrange it</div>
 <div class="s24"></div>
 <div class="h1">Want to see<br>it <span class="accent">yourself?</span></div>
 <div class="s16"></div>
 <div class="lead">We'll set up the site visit and a like-for-like comparison against two more venues.</div>
 <div class="s32"></div>
 <span class="pill">Start your brief {ARROW}</span>
 <div class="s24"></div>
 <div class="trust"><span class="t">{TICK} Free to you</span><span class="t">{TICK} Independent since 1989</span></div>
 <div class="fill"></div>
 {foot(NV,5)}
""")

doc=f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>"+"".join(s for _,s in SL)+"</body></html>"
open("index2.html","w").write(doc)
open("slides2.txt","w").write("\n".join(n for n,_ in SL))
print("slides:",len(SL))
