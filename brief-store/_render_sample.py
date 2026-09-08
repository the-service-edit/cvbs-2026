"""Expands BriefPdf.html with a sample brief so the layout can be eyeballed
without deploying. Not used in production. Regenerate with:
    python3 brief-store/_render_sample.py"""
import re, html

rec = dict(
    ref="CVB-260908-001", received="8 Sep 2026 10:14",
    first="Jane", last="Smith", email="jane.smith@acme.com.au",
    phone="+61 400 000 000", company="Acme Corporation", role="Executive assistant / PA",
    services="Conference venue finding, Group accommodation",
    location="Brisbane, QLD", locationDetail="", radius="Within 2 to 3 hours drive",
    delegates="120", startDate="2027-03-15", endDate="2027-03-17", flexibleDates="",
    duration="3 days", accommodation="Yes, all delegates", venueType="Resort",
    requirements="Catering, AV / technology, Breakout rooms, Team activities",
    setup="Cabaret", budgetPp="$180", budgetTotal="$95,000",
    notes="We ran this in the city last year and it felt flat. Somewhere with space to "
          "walk between sessions. Two of the group use a wheelchair so step free access "
          "to every room is not negotiable.",
    offer="", venue="", referral="Word of mouth / referral", source="submit-a-brief.html")

e = lambda v: html.escape(str(v or ""), quote=True)
headline = [("Delegates", e(rec["delegates"])), ("Location", e(rec["location"])),
            ("Dates", "Sun 15 Mar 2027 to Wed 17 Mar 2027<br><span style='font-weight:normal;font-size:9pt;color:#197683'>27 weeks away</span>"),
            ("Budget", "$180 per delegate per day<br>$95,000 total")]
brief = [("What they need", e(rec["services"])), ("Venue type", e(rec["venueType"])),
         ("Travel radius", e(rec["radius"])), ("Duration", e(rec["duration"])),
         ("Accommodation", e(rec["accommodation"])), ("On site", e(rec["requirements"])),
         ("Room setup", e(rec["setup"]))]
contact = [("Name", "Jane Smith"), ("Company", e(rec["company"])), ("Role", e(rec["role"])),
           ("Email", e(rec["email"])), ("Phone", e(rec["phone"])),
           ("Heard about us", e(rec["referral"]))]

src = open("BriefPdf.html").read()
head, rest = src.split('<table class="facts"', 1)
head = head.replace("<?!= rec.ref ?>", rec["ref"]).replace("<?!= rec.received ?>", rec["received"])

cells = "".join(
    '<td class="%s"><div class="k">%s</div><div class="v">%s</div></td>'
    % ("last" if i == len(headline) - 1 else "", k, v) for i, (k, v) in enumerate(headline))
rows = lambda pairs: "".join(
    '<tr><td class="k">%s</td><td class="v">%s</td></tr>' % (k, v) for k, v in pairs)

body = ('<table class="facts" style="margin-top:3px"><tr>' + cells + "</tr></table>"
    + "<h2>In their words</h2><div class=\"quote\"><p>" + e(rec["notes"]) + "</p></div>"
    + '<h2>The brief</h2><table class="rows">' + rows(brief) + "</table>"
    + '<h2>Who sent it</h2><table class="rows">' + rows(contact) + "</table>"
    + '<p class="foot">Submitted through conferencevenues.com.au, submit-a-brief.html. '
      'Quote CVB-260908-001 when you reply. The full record is in the briefs sheet.</p>'
    + "</body></html>")

open("_sample.html", "w").write(head + body)
print("wrote _sample.html")
