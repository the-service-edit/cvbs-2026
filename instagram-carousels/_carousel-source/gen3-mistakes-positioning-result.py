#!/usr/bin/env python3
# Rebuild of 01 Budget mistakes, 02 Searched vs Sourced, 03 Client result in liquid glass.
CSS = """
@font-face{font-family:Inter;font-weight:400;src:url('../fonts/Inter-400.ttf')}
@font-face{font-family:Inter;font-weight:500;src:url('../fonts/Inter-500.ttf')}
@font-face{font-family:Inter;font-weight:600;src:url('../fonts/Inter-600.ttf')}
@font-face{font-family:Inter;font-weight:700;src:url('../fonts/Inter-700.ttf')}
@font-face{font-family:Inter;font-weight:800;src:url('../fonts/Inter-800.ttf')}
:root{--teal:#3BC9D9;--teal-deep:#28A8B6;--navy:#0D2233;--navy2:#071520;--stone:#F4F1EA}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Inter,sans-serif;-webkit-font-smoothing:antialiased}
.slide{width:1080px;height:1350px;position:relative;overflow:hidden;display:flex;flex-direction:column;padding:80px 74px 72px;color:#fff}
.slide>*{position:relative;z-index:2}
.bg{position:absolute;inset:0;z-index:0;background-size:cover;background-position:center;transform:scale(1.06)}
.scrim{position:absolute;inset:0;z-index:1;background:linear-gradient(180deg,rgba(7,21,32,.50) 0%,rgba(7,21,32,.24) 32%,rgba(7,21,32,.46) 64%,rgba(7,21,32,.88) 100%)}
.scrim-deep{background:linear-gradient(180deg,rgba(7,21,32,.64) 0%,rgba(7,21,32,.56) 50%,rgba(7,21,32,.84) 100%)}
.fill{flex:1}
.s8{height:18px}.s16{height:30px}.s24{height:44px}.s32{height:60px}
.glass{background:rgba(255,255,255,.13);backdrop-filter:blur(34px) saturate(155%);-webkit-backdrop-filter:blur(34px) saturate(155%);border:1.5px solid rgba(255,255,255,.30);border-radius:34px;box-shadow:0 44px 80px -34px rgba(0,0,0,.70), inset 0 2px 0 rgba(255,255,255,.42), inset 0 -1px 0 rgba(255,255,255,.07)}
.glass-tint{background:rgba(11,28,42,.46);backdrop-filter:blur(30px) saturate(150%);-webkit-backdrop-filter:blur(30px) saturate(150%);border:1.5px solid rgba(255,255,255,.18);border-radius:34px;box-shadow:0 44px 80px -34px rgba(0,0,0,.7), inset 0 2px 0 rgba(255,255,255,.24)}
.pad{padding:56px 56px}
.chip{display:inline-flex;align-items:center;gap:16px;align-self:flex-start;padding:18px 28px;border-radius:999px;font-size:23px;font-weight:600;letter-spacing:.2em;text-transform:uppercase;color:#fff;background:rgba(255,255,255,.14);backdrop-filter:blur(24px) saturate(150%);-webkit-backdrop-filter:blur(24px) saturate(150%);border:1.5px solid rgba(255,255,255,.32);box-shadow:inset 0 1.5px 0 rgba(255,255,255,.45)}
.chip::before{content:"";width:34px;height:3px;border-radius:2px;background:var(--teal)}
.chip.plain::before{display:none}
.h1{font-size:88px;font-weight:700;line-height:1.02;letter-spacing:-.035em;text-shadow:0 4px 30px rgba(0,0,0,.4)}
.h2{font-size:60px;font-weight:700;line-height:1.06;letter-spacing:-.03em}
.h3{font-size:44px;font-weight:700;line-height:1.12;letter-spacing:-.02em}
.accent{color:var(--teal)}
.lead{font-size:33px;line-height:1.5;font-weight:400;color:rgba(255,255,255,.9)}
.sub{font-size:31px;line-height:1.45;font-weight:400;color:rgba(255,255,255,.86)}
.kick{font-size:24px;font-weight:600;letter-spacing:.22em;text-transform:uppercase;color:var(--teal)}
.kick.bar{display:inline-flex;align-items:center;gap:16px}
.kick.bar::before{content:"";width:40px;height:3px;border-radius:2px;background:var(--teal)}
.mnum{font-size:120px;font-weight:800;letter-spacing:-.04em;color:var(--teal);line-height:.8}
/* contrast */
.cpanel{padding:42px 48px;border-radius:30px}
.clbl{display:flex;align-items:center;gap:16px;font-size:24px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;margin-bottom:18px}
.cic{width:46px;height:46px;border-radius:50%;display:grid;place-items:center;flex:none}
.cic svg{width:25px;height:25px}
.ctxt{font-size:37px;line-height:1.26;font-weight:600;letter-spacing:-.01em}
.c-dim .clbl{color:rgba(255,255,255,.7)}.c-dim .cic{background:rgba(255,255,255,.16);color:rgba(255,255,255,.8)}.c-dim .ctxt{color:rgba(255,255,255,.86)}
.c-win .clbl{color:var(--teal)}.c-win .cic{background:rgba(59,201,217,.24);color:var(--teal);border:1.5px solid rgba(59,201,217,.5)}.c-win .ctxt{color:#fff}
.vs{align-self:center;font-size:25px;font-weight:700;letter-spacing:.22em;color:rgba(255,255,255,.7);margin:16px 0;text-transform:uppercase}
.idx{font-size:28px;font-weight:700;color:var(--teal);letter-spacing:.16em}
/* steps */
.step{display:flex;gap:26px;align-items:flex-start}.step+.step{margin-top:34px}
.step .n{flex:none;width:62px;height:62px;border-radius:50%;display:grid;place-items:center;font-size:32px;font-weight:800;color:var(--teal);background:rgba(59,201,217,.20);border:1.5px solid rgba(59,201,217,.45)}
.step .st-t{font-size:34px;font-weight:700;letter-spacing:-.01em}
.step .st-b{font-size:27px;line-height:1.4;color:rgba(255,255,255,.82);margin-top:6px}
/* stat rows */
.srow{display:flex;align-items:baseline;gap:24px}.srow+.srow{margin-top:30px;padding-top:30px;border-top:1.5px solid rgba(255,255,255,.18)}
.srow .n{font-size:78px;font-weight:800;letter-spacing:-.04em;color:var(--teal);line-height:.9;min-width:230px}
.srow .l{font-size:30px;font-weight:500;color:rgba(255,255,255,.88);line-height:1.3}
/* quote */
.qm{font-size:150px;font-weight:800;line-height:.5;color:var(--teal);height:80px}
.quote{font-size:46px;font-weight:600;line-height:1.32;letter-spacing:-.02em}
.attr{font-size:28px;font-weight:600;margin-top:6px}.attr span{display:block;color:rgba(255,255,255,.72);font-weight:400;margin-top:6px}
/* cta */
.pill{display:inline-flex;align-items:center;gap:18px;align-self:flex-start;background:var(--teal-deep);color:#fff;font-size:33px;font-weight:600;padding:30px 46px;border-radius:18px;box-shadow:0 24px 50px -18px rgba(0,0,0,.6)}
.pill svg{width:30px;height:30px}
.trust{display:flex;gap:26px;flex-wrap:wrap;font-size:25px;color:rgba(255,255,255,.9);font-weight:500}
.trust .t{display:inline-flex;align-items:center;gap:12px}.trust svg{width:25px;height:25px;color:var(--teal)}
.foot{display:flex;align-items:center;justify-content:space-between;padding-top:30px;border-top:1px solid rgba(255,255,255,.22)}
.foot img{height:48px}.foot .url{font-size:24px;font-weight:600;color:rgba(255,255,255,.88)}
.swipe{display:inline-flex;align-items:center;gap:14px;font-size:25px;font-weight:600;color:var(--teal)}.swipe svg{width:30px;height:30px}
.dots{display:flex;gap:11px;align-items:center}.dot{width:11px;height:11px;border-radius:50%;background:rgba(255,255,255,.32)}.dot.on{background:var(--teal);width:30px;border-radius:6px}
"""
ARROW='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
CHK='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7"/></svg>'
CROSS='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M6 6l12 12M18 6L6 18"/></svg>'
TICK='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M8.5 12.5l2.5 2.5 4.5-5"/></svg>'
SL=[]
def add(n,inner): SL.append((n,f'<div class="slide" id="{n}">{inner}</div>'))
def bg(img,pos="center",scrim="scrim"): return f'<div class="bg" style="background-image:url(../assets/{img});background-position:{pos}"></div><div class="scrim {scrim}"></div>'
def foot(n,i,right=None):
    r=right if right is not None else '<div class="dots">'+''.join(f'<span class="dot{" on" if k==i else ""}"></span>' for k in range(n))+'</div>'
    return f'<div class="foot"><img src="../assets/logo-white.png"><span class="url">conferencevenues.com</span>{r}</div>'
def swipe(): return f'<span class="swipe">Swipe {ARROW}</span>'

# ============ 01 BUDGET MISTAKES
A="a_budget_mistakes"; N=7
imgs=["vhero.jpg","vint.jpg","conf.jpg","crown.jpg","vint.jpg"]
poss=["center 40%","center 55%","center 45%","center 30%","center 60%"]
add(f"{A}_1", f"""
 {bg("vhero.jpg","center 40%","scrim")}
 <div class="chip">Conference planning &middot; since 1989</div>
 <div class="fill"></div>
 <div class="h1">5 mistakes that<br>quietly <span class="accent">inflate</span><br>your event budget</div>
 <div class="s16"></div>
 <div class="lead">The costliest line items rarely show up on the first quote. Here's where the money really goes.</div>
 <div class="s32"></div>
 {foot(N,0,swipe())}
""")
mistakes=[
 ("01","Booking the first venue that says yes","The fastest option is almost never the best value. One genuine comparison usually moves the price, the inclusions, or both."),
 ("02","Negotiating the rate on your own","Venues quote differently to a one-off client than to a buyer they deal with weekly. Relationships move rates more than haggling does."),
 ("03","Skimming the minimum spend clause","Food, beverage and room-hire minimums are where budgets quietly blow out. Read them before you fall for the room."),
 ("04","Leaving accommodation to the end","Group rates and room blocks get tighter the longer you wait. Lock delegate rooms when you lock the space."),
 ("05","Choosing on price, not total value","The cheapest room can cost the most once AV, parking and Wi-Fi are added. Compare the whole picture."),
]
for k,(num,t,b) in enumerate(mistakes):
    add(f"{A}_{k+2}", f"""
     {bg(imgs[k],poss[k],"scrim-deep")}
     <div class="fill"></div>
     <div class="glass pad">
       <div style="display:flex;align-items:center;gap:26px"><span class="mnum">{num}</span><span class="kick" style="letter-spacing:.2em">Mistake</span></div>
       <div class="s24"></div>
       <div class="h2">{t}</div>
       <div class="s16"></div>
       <div class="sub">{b}</div>
     </div>
     <div class="fill"></div>
     {foot(N,k+1)}
    """)
add(f"{A}_7", f"""
 {bg("crown.jpg","center 35%","scrim-deep")}
 <div class="fill"></div>
 <div class="chip plain" style="background:rgba(59,201,217,.18);border-color:rgba(59,201,217,.5)">Avoid all five</div>
 <div class="s24"></div>
 <div class="h1">We do this every<br>day, <span class="accent">on your side</span></div>
 <div class="s16"></div>
 <div class="lead">Send us the brief. We compare venues, read the fine print and negotiate the rate. Free to you.</div>
 <div class="s32"></div>
 <span class="pill">Start your brief {ARROW}</span>
 <div class="s24"></div>
 <div class="trust"><span class="t">{TICK} Free to you</span><span class="t">{TICK} Independent since 1989</span></div>
 <div class="fill"></div>
 {foot(N,6)}
""")

# ============ 02 SEARCHED VS SOURCED
B="b_searched_vs_sourced"; NB=6
add(f"{B}_1", f"""
 {bg("doltone.jpg","center 45%","scrim")}
 <div class="chip">How we work</div>
 <div class="fill"></div>
 <div class="h1">The right venue<br>isn't searched.<br>It's <span class="accent">sourced</span>.</div>
 <div class="s16"></div>
 <div class="lead">There's a difference between finding a room and being handed the right one.</div>
 <div class="s32"></div>
 {foot(NB,0,swipe())}
""")
add(f"{B}_2", f"""
 {bg("wsyd.jpg","center 40%","scrim-deep")}
 <div class="fill"></div>
 <div class="glass pad">
   <div class="kick bar">The difference</div>
   <div class="s24"></div>
   <div class="h2">Searching is what a<br>browser does. <span class="accent">Sourcing</span><br>is what we do.</div>
   <div class="s16"></div>
   <div class="sub">Anyone can pull up a list of venues. Knowing which one will actually hold your date, at the right rate, is a different job.</div>
 </div>
 <div class="fill"></div>
 {foot(NB,1)}
""")
pairs=[
 ("doltone.jpg","center 30%","You compare what's online","We know what's actually available, including rooms that never reach a public listing."),
 ("crown.jpg","center 40%","You chase quotes and wait","We negotiate rates directly, with people who deal with us every week."),
 ("wsyd.jpg","center 55%","You hope the price is fair","We benchmark every quote against the market and hold venues to account."),
]
for k,(im,po,bad,good) in enumerate(pairs):
    add(f"{B}_{k+3}", f"""
     {bg(im,po,"scrim-deep")}
     <div class="idx">0{k+1} / 03</div>
     <div class="fill"></div>
     <div class="glass-tint cpanel c-dim">
       <div class="clbl"><span class="cic">{CROSS}</span> Searching</div>
       <div class="ctxt">{bad}</div>
     </div>
     <div class="vs">vs</div>
     <div class="glass cpanel c-win">
       <div class="clbl"><span class="cic">{CHK}</span> Sourcing</div>
       <div class="ctxt">{good}</div>
     </div>
     <div class="fill"></div>
     {foot(NB,k+2)}
    """)
add(f"{B}_6", f"""
 {bg("crown.jpg","center 35%","scrim-deep")}
 <div class="fill"></div>
 <div class="chip plain" style="background:rgba(59,201,217,.18);border-color:rgba(59,201,217,.5)">Let us source it</div>
 <div class="s24"></div>
 <div class="h1">Get a <span class="accent">shortlist</span><br>in 48 hours.</div>
 <div class="s16"></div>
 <div class="lead">Independent, relationship-led, and free to you. We're paid by the venue, never by you.</div>
 <div class="s32"></div>
 <span class="pill">Start your brief {ARROW}</span>
 <div class="s24"></div>
 <div class="trust"><span class="t">{TICK} Free to you</span><span class="t">{TICK} Since 1989</span></div>
 <div class="fill"></div>
 {foot(NB,5)}
""")

# ============ 03 CLIENT RESULT
C="c_client_result"; NC=7
add(f"{C}_1", f"""
 {bg("star.jpg","center 45%","scrim")}
 <div class="chip">Client result</div>
 <div class="fill"></div>
 <div class="h1">140 delegates.<br>48 hours.<br><span class="accent">One</span> phone call.</div>
 <div class="s16"></div>
 <div class="lead">How a last-minute national conference came together without the panic.</div>
 <div class="s32"></div>
 {foot(NC,0,swipe())}
""")
add(f"{C}_2", f"""
 {bg("conf.jpg","center 45%","scrim-deep")}
 <div class="fill"></div>
 <div class="glass pad">
   <div class="kick bar">The brief</div>
   <div class="s24"></div>
   <div class="h2">A two-day conference<br>for <span class="accent">140 people</span>.</div>
   <div class="s16"></div>
   <div class="sub">Plenary plus three breakout rooms, full catering, and accommodation for interstate delegates. Dates locked. Budget tight.</div>
 </div>
 <div class="fill"></div>
 {foot(NC,1)}
""")
add(f"{C}_3", f"""
 {bg("vhero.jpg","center 55%","scrim-deep")}
 <div class="fill"></div>
 <div class="glass-tint pad">
   <div class="kick bar">The challenge</div>
   <div class="s24"></div>
   <div class="h2">Eight weeks out,<br>and <span class="accent">nothing held</span>.</div>
   <div class="s16"></div>
   <div class="sub">The original venue fell through. Peak season. Every day of delay meant fewer rooms and higher rates.</div>
 </div>
 <div class="fill"></div>
 {foot(NC,2)}
""")
add(f"{C}_4", f"""
 {bg("vint.jpg","center 45%","scrim-deep")}
 <div class="kick bar">What we did</div>
 <div class="s24"></div>
 <div class="glass pad">
   <div class="step"><div class="n">1</div><div><div class="st-t">Briefed once, not ten times</div><div class="st-b">One call captured the full requirement. No re-explaining to five sales teams.</div></div></div>
   <div class="step"><div class="n">2</div><div><div class="st-t">Shortlisted in 48 hours</div><div class="st-b">Three venues that genuinely fit, compared like-for-like on what matters.</div></div></div>
   <div class="step"><div class="n">3</div><div><div class="st-t">Negotiated the whole deal</div><div class="st-b">Room hire, catering minimums and delegate rooms, settled in one go.</div></div></div>
 </div>
 <div class="fill"></div>
 {foot(NC,3)}
""")
add(f"{C}_5", f"""
 {bg("star.jpg","center 35%","scrim-deep")}
 <div class="kick bar">The result</div>
 <div class="s24"></div>
 <div class="glass pad">
   <div class="srow"><span class="n">48 hrs</span><span class="l">From brief to a considered shortlist</span></div>
   <div class="srow"><span class="n">18%</span><span class="l">Under the original budget</span></div>
   <div class="srow"><span class="n">140</span><span class="l">Delegates, rooms and all, sorted</span></div>
 </div>
 <div class="fill"></div>
 {foot(NC,4)}
""")
add(f"{C}_6", f"""
 {bg("doltone.jpg","center 50%","scrim-deep")}
 <div class="fill"></div>
 <div class="glass pad">
   <div class="qm">&ldquo;</div>
   <div class="quote">They held the room I needed before I'd even finished explaining the brief. One call and it was handled.</div>
   <div class="s16"></div>
   <div class="attr">Events Manager, national association<span>Client since 2019</span></div>
 </div>
 <div class="fill"></div>
 {foot(NC,5)}
""")
add(f"{C}_7", f"""
 {bg("conf.jpg","center 40%","scrim-deep")}
 <div class="fill"></div>
 <div class="chip plain" style="background:rgba(59,201,217,.18);border-color:rgba(59,201,217,.5)">Your event next</div>
 <div class="s24"></div>
 <div class="h1">Planning something<br><span class="accent">like this?</span></div>
 <div class="s16"></div>
 <div class="lead">Send the brief. We'll come back with a shortlist worth your time.</div>
 <div class="s32"></div>
 <span class="pill">Start your brief {ARROW}</span>
 <div class="s24"></div>
 <div class="trust"><span class="t">{TICK} Free to you</span><span class="t">{TICK} Independent</span><span class="t">{TICK} Since 1989</span></div>
 <div class="fill"></div>
 {foot(NC,6)}
""")

doc=f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>"+"".join(s for _,s in SL)+"</body></html>"
open("index3.html","w").write(doc); open("slides3.txt","w").write("\n".join(n for n,_ in SL))
print("slides:",len(SL))
