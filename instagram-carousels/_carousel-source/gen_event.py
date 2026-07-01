#!/usr/bin/env python3
# IHG event-recap carousel (glass style)
CSS=open("/sessions/peaceful-eager-allen/mnt/outputs/build/_glasscss.txt").read()
CSS+="""
#ihg_1{background:#0A2C52}
.cover-img{margin:-80px -74px 0;height:858px;background-size:cover;background-repeat:no-repeat;position:relative}
.cover-img::after{content:"";position:absolute;left:0;right:0;bottom:0;height:300px;background:linear-gradient(180deg,rgba(10,44,82,0) 0%,rgba(10,44,82,.6) 55%,#0A2C52 100%)}
.cover-body{margin-top:34px}
"""
ARROW='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
TICK='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M8.5 12.5l2.5 2.5 4.5-5"/></svg>'
SL=[]
def add(n,inner): SL.append((n,f'<div class="slide" id="{n}">{inner}</div>'))
def bg(img,pos="center",scrim="scrim"): return f'<div class="bg" style="background-image:url(../assets/{img});background-position:{pos}"></div><div class="scrim {scrim}"></div>'
def foot(n,i,right=None):
    r=right if right is not None else '<div class="dots">'+''.join(f'<span class="dot{" on" if k==i else ""}"></span>' for k in range(n))+'</div>'
    return f'<div class="foot"><img src="../assets/logo-white.png"><span class="url">conferencevenues.com</span>{r}</div>'
def swipe(): return f'<span class="swipe">Swipe {ARROW}</span>'
N=5
add("ihg_1", f"""
 {bg("ev_group.jpg","center 36%","scrim-deep")}
 <div class="fill"></div>
 <div class="glass pad">
   <div class="chip">Industry event &middot; Sydney</div>
   <div class="s24"></div>
   <div class="h1">An afternoon<br>with <span class="accent">IHG</span>.</div>
   <div class="s16"></div>
   <div class="sub">The CVBS team at the IHG Hotels &amp; Resorts showcase and market update.</div>
 </div>
 <div class="s32"></div>
 {foot(N,0,swipe())}
""")
add("ihg_2", f"""
 {bg("ev_update.jpg","center 38%","scrim-deep")}
 <div class="fill"></div>
 <div class="glass pad">
   <div class="kick bar">What it was</div>
   <div class="s24"></div>
   <div class="h2">A showcase across<br>the whole <span class="accent">portfolio</span>.</div>
   <div class="s16"></div>
   <div class="sub">An interactive afternoon and market update on where the IHG brands, and the wider hospitality landscape, are heading.</div>
 </div>
 <div class="fill"></div>
 {foot(N,1)}
""")
add("ihg_3", f"""
 {bg("ev_holidayinn.jpg","center 45%","scrim-deep")}
 <div class="fill"></div>
 <div class="glass pad">
   <div class="kick bar">On show</div>
   <div class="s24"></div>
   <div class="h2">From Holiday Inn<br>to <span class="accent">Kimpton</span>.</div>
   <div class="s16"></div>
   <div class="sub">A look right across the IHG family, from trusted classics to design-led stays, and what each can do for your next event.</div>
 </div>
 <div class="fill"></div>
 {foot(N,2)}
""")
add("ihg_4", f"""
 {bg("ev_networking.jpg","center 40%","scrim-deep")}
 <div class="fill"></div>
 <div class="glass pad">
   <div class="kick bar">What we took away</div>
   <div class="s24"></div>
   <div class="h2">Hospitality runs on<br><span class="accent">relationships</span>.</div>
   <div class="s16"></div>
   <div class="sub">Real insight into where the industry is going, and a good reminder that strong partnerships are what make great events happen.</div>
 </div>
 <div class="fill"></div>
 {foot(N,3)}
""")
add("ihg_5", f"""
 {bg("ev_kimpton.jpg","center 50%","scrim-deep")}
 <div class="fill"></div>
 <div class="chip plain" style="background:rgba(59,201,217,.18);border-color:rgba(59,201,217,.5)">CVBS &times; IHG</div>
 <div class="s24"></div>
 <div class="h1">Thank you for the<br><span class="accent">hospitality</span>.</div>
 <div class="s16"></div>
 <div class="lead">Always good to connect, learn and keep building on a strong relationship. Looking forward to what's ahead.</div>
 <div class="s32"></div>
 <div class="trust"><span class="t">{TICK} Independent venue finding</span><span class="t">{TICK} Since 1989</span></div>
 <div class="fill"></div>
 {foot(N,4)}
""")
doc=f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>"+"".join(s for _,s in SL)+"</body></html>"
open("index_event.html","w").write(doc); open("slides_event.txt","w").write("\n".join(n for n,_ in SL))
print("slides",len(SL))
