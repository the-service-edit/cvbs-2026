"""Expands ClientEmail.html with a sample brief so the layout can be checked in a
browser without deploying. Not used in production."""
import re, html
rec = dict(ref="CVB-260908-007", first="Jane", delegates="30",
           location="Sydney, NSW", dates="17 to 19 Nov 2026")
base = "https://the-service-edit.github.io/cvbs-2026"
facts = [("Delegates", rec["delegates"]), ("Location", rec["location"]), ("Dates", rec["dates"])]

s = open("ClientEmail.html").read()
s = s.replace("<?!= base ?>", base)
s = s.replace("<?!= rec.ref ?>", rec["ref"])
s = s.replace("<?!= firstName ?>", rec["first"])
s = s.replace("<?!= replyTo ?>", "aj@conferencevenues.com.au")

TD = ('<td class="fact" valign="top" width="33%" style="padding-right:14px; '
      'font-family:Inter,Helvetica,Arial,sans-serif;">'
      '<p style="margin:0 0 3px 0; font-size:10px; letter-spacing:1.6px; '
      'text-transform:uppercase; color:#6E747B; font-weight:600;">{k}</p>'
      '<p style="margin:0; font-size:16px; line-height:23px; color:#0A2C52; '
      'font-weight:700;">{v}</p></td>')
cells = "".join(TD.format(k=k, v=v) for k, v in facts)
s = re.sub(r"<\? for \(var i = 0.*?<\? \} \?>", cells, s, flags=re.S)
open("_client-preview.html", "w").write(s)
print("wrote _client-preview.html")
