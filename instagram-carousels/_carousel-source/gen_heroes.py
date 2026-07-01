#!/usr/bin/env python3
# An array of CVBS carousel hero/cover styles across post types.
CSS=open("/sessions/peaceful-eager-allen/mnt/outputs/build/_glasscss.txt").read()
CSS+="""
#h5{background:#0A2C52}
#h7{background:#EEF6F7}
.lightfoot{border-top:1px solid #D6E7E9 !important}
.lightfoot .url{color:#6E747B !important}
.price{display:flex;align-items:baseline;gap:16px}
.price .pre{font-size:27px;font-weight:500;color:rgba(255,255,255,.85)}
.price .big{font-size:70px;font-weight:800;letter-spacing:-.03em;color:var(--teal)}
.heronum{font-size:300px;font-weight:800;color:var(--teal);line-height:.74;letter-spacing:-.05em}
.loc{display:inline-flex;align-items:center;gap:14px;align-self:flex-start;padding:16px 26px;border-radius:999px;
 font-size:25px;font-weight:600;color:#fff;background:rgba(255,255,255,.14);
 backdrop-filter:blur(24px) saturate(150%);-webkit-backdrop-filter:blur(24px) saturate(150%);
 border:1.5px solid rgba(255,255,255,.32)}
.loc svg{width:26px;height:26px;color:var(--teal)}
.tagk{display:inline-flex;align-self:flex-start;padding:14px 24px;border-radius:999px;font-size:22px;font-weight:700;
 letter-spacing:.16em;text-transform:uppercase;background:rgba(40,168,182,.14);color:var(--teal-deep);
 border:1.5px solid rgba(40,168,182,.30)}
.eyebrow-d{display:inline-flex;align-items:center;gap:16px;font-size:23px;letter-spacing:.24em;text-transform:uppercase;font-weight:600;color:var(--teal-deep)}
.eyebrow-d::before{content:"";width:40px;height:3px;border-radius:2px;background:var(--teal)}
.navytype{color:#0D1F2D}
.tag2{position:relative;align-self:flex-start;background:var(--teal);color:#06262b;font-weight:700;padding:20px 32px 20px 58px;border-radius:16px;font-size:28px;letter-spacing:.06em;text-transform:uppercase;transform:rotate(-2.5deg);box-shadow:0 20px 40px -18px rgba(0,0,0,.6)}
.tag2::before{content:"";position:absolute;left:24px;top:50%;transform:translateY(-50%);width:18px;height:18px;border-radius:50%;background:#06262b}
"""
ARROW='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
PIN='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s7-5.5 7-11a7 7 0 0 0-14 0c0 5.5 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/></svg>'
def footw(): return '<div class="foot"><img src="../assets/logo-white.png"><span class="url">conferencevenues.com</span><span class="swipe">Swipe '+ARROW+'</span></div>'
def footd(): return '<div class="foot lightfoot"><img src="../assets/logo.png"><span class="url">conferencevenues.com</span><span class="swipe" style="color:var(--teal-deep)">Swipe '+ARROW+'</span></div>'
def bg(img,pos,scrim="scrim"): return f'<div class="bg" style="background-image:url(../assets/{img});background-position:{pos}"></div><div class="scrim {scrim}"></div>'
def lab(t): return f'<div class="label">{t}</div>'
SL=[]
def add(n,inner,cls=""): SL.append((n,f'<div class="slide {cls}" id="{n}">{inner}</div>'))

# H1 Offer — full bleed + price pill
add("h1", f"""{bg("kimpton.jpg","center 35%","scrim")}
 <div class="chip">Venue offer &middot; Sydney</div><div class="fill"></div>
 <div class="h1">Winter at<br>Kimpton <span class="accent">Margot</span>.</div><div class="s24"></div>
 <div class="glass" style="align-self:flex-start;padding:26px 36px;border-radius:22px"><div class="price"><span class="pre">Day delegate from</span><span class="big">$110pp</span></div></div>
 <div class="s32"></div>{footw()}""")

# H2 Site visit — full bleed + glass panel
add("h2", f"""{bg("hyatt.jpg","center 40%","scrim-deep")}
 <div class="fill"></div>
 <div class="glass pad"><div class="chip">Site visit &middot; Melbourne</div><div class="s24"></div>
   <div class="h1">Inside <span class="accent">Hyatt</span><br>Place.</div></div>
 <div class="s32"></div>{footw()}""")

# H3 Event recap — full bleed group + glass panel (chosen C style)
add("h3", f"""{bg("ev_group.jpg","center 36%","scrim-deep")}
 <div class="fill"></div>
 <div class="glass pad"><div class="chip">Industry event &middot; Sydney</div><div class="s24"></div>
   <div class="h1">An afternoon<br>with <span class="accent">IHG</span>.</div></div>
 <div class="s32"></div>{footw()}""")

# H4 Educational — number led
add("h4", f"""{bg("vint.jpg","center 45%","scrim-deep")}
 <div class="fill"></div><div class="chip">Conference planning</div><div class="s16"></div>
 <div class="heronum">5</div>
 <div class="h1" style="font-size:64px;margin-top:6px">mistakes that inflate<br>your event <span class="accent">budget</span></div>
 <div class="s32"></div>{footw()}""")

# H5 Positioning — navy, no photo
add("h5", f"""<div class="eyebrow" style="align-self:flex-start">How we work</div>
 <div class="fill"></div>
 <div class="h1" style="font-size:78px">The right venue<br>isn't searched.<br>It's <span class="accent">sourced</span>.</div>
 <div class="s16"></div><div class="lead">There's a difference between finding a room and being handed the right one.</div>
 <div class="fill"></div>{footw()}""")

# H6 Destination — location tag
add("h6", f"""{bg("syd.jpg","center 45%","scrim")}
 <div class="loc">{PIN} Sydney, NSW</div><div class="fill"></div>
 <div class="h1">Your conference,<br>sorted in <span class="accent">Sydney</span>.</div>
 <div class="s16"></div><div class="lead">From the harbour to the CBD, the right room at the right rate.</div>
 <div class="s32"></div>{footw()}""")

# H7 Offers roundup — light / stone cover
add("h7", f"""<div class="tagk">Monthly</div><div class="fill"></div>
 <div class="eyebrow-d">Offers roundup &middot; June</div><div class="s24"></div>
 <div class="h1 navytype">This month's<br>venue <span class="accent">offers</span>.</div>
 <div class="s16"></div><div class="lead" style="color:#37444f">Five rates worth booking, negotiated for CVBS clients.</div>
 <div class="fill"></div>{footd()}""")

# H8 Client result — stat led over photo
add("h8", f"""{bg("crown.jpg","center 35%","scrim-deep")}
 <div class="chip">Client result</div><div class="fill"></div>
 <div class="h1" style="font-size:96px">140 delegates.<br>48 hours.<br><span class="accent">One</span> call.</div>
 <div class="s32"></div>{footw()}""")

# H9 Destination — luggage-tag motif
add("h9", f"""{bg("syd.jpg","center 45%","scrim")}
 <div class="tag2">{PIN}&nbsp; Sydney</div><div class="fill"></div>
 <div class="h1">Conferences,<br>sorted in <span class="accent">Sydney</span>.</div>
 <div class="s16"></div><div class="lead">From the harbour to the CBD, the right room at the right rate.</div>
 <div class="s32"></div>{footw()}""")

doc=f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>"+"".join(s for _,s in SL)+"</body></html>"
open("index_heroes.html","w").write(doc); open("slides_heroes.txt","w").write("\n".join(n for n,_ in SL))
print("heroes",len(SL))
