# -*- coding: utf-8 -*-
"""Build privacy.html and terms.html.

Chrome, nav, mobile menu, footer and the newsletter band are lifted out of
how-we-are-paid.html at build time, exactly as build_venue.py does, so these
two pages cannot drift from the rest of the site when the nav changes.

Nothing on these pages is invented. Every statement describes something the
build actually does: the brief posts to the CVBS brief store (Google Apps
Script and a Google Sheet, with emails sent by Resend), the offers signup
goes to Mailchimp, the fonts come from Google,
the shortlist sits in the visitor's own browser, and there is no analytics or
advertising code anywhere in the site. Where a fact is genuinely not known
(the registered entity name, the ABN, who the data controller is on paper),
the page does not guess and does not carry a placeholder. Those sit on the
client decision sheet instead.

Usage: python3 _legal-source/build_legal.py
"""
import io, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'how-we-are-paid.html')
sys.path.insert(0, os.path.join(ROOT, '_entity-source'))
import entity as E                                              # noqa: E402

BASE = E.SERVE.rstrip('/')
UPDATED = '6 September 2026'          # terms
PRIVACY_UPDATED = '11 September 2026'  # privacy: processors corrected, Web3Forms retired

ARROW = ('<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" '
         'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
         '<path d="M5 12h14M13 6l6 6-6 6"/></svg>')

src = io.open(SRC, encoding='utf-8').read()


def between(a, b, s=None):
    s = src if s is None else s
    i = s.index(a)
    j = s.index(b, i)
    return s[i:j]


HEAD_OPEN = between('<!DOCTYPE html>', '<title>')
HEAD_TAIL = between('<meta name="theme-color"', '<script type="application/ld+json"')
CHROME = between('<header class="site-header">', '<main id="main">') if '<main id="main">' in src \
    else between('<header class="site-header">', '<section class="page-hero">')
TAIL = src[src.index('</main>'):]


def head(title, desc, slug):
    return (HEAD_OPEN
            + '<title>%s</title>\n' % title
            + '<meta name="description" content="%s">\n' % desc
            + '<link rel="canonical" href="%s/%s">\n' % (BASE, slug)
            + re.sub(r'(og:title" content=")[^"]*', r'\g<1>' + title,
              re.sub(r'(og:description" content=")[^"]*', r'\g<1>' + desc,
              re.sub(r'(og:url" content=")[^"]*', r'\g<1>%s/%s' % (BASE, slug), HEAD_TAIL))))


def hero(crumb, eyebrow, h1, lead):
    return ('<section class="page-hero">\n  <div class="wrap">\n'
            '    <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a>'
            '<span>/</span><b style="color:inherit;font-weight:500">%s</b></nav>\n'
            '    <span class="eyebrow" style="margin-top:1.2rem">%s</span>\n'
            '    <h1>%s</h1>\n    <p class="lead">%s</p>\n'
            '  </div>\n</section>\n' % (crumb, eyebrow, h1, lead))


def prose(blocks):
    out = []
    for band, body in blocks:
        out.append('<section class="s-%s pad"><div class="wrap wrap--narrow prose">\n%s\n</div></section>\n'
                   % (band, body))
    return ''.join(out)


def page(slug, title, desc, crumb, eyebrow, h1, lead, blocks, ld):
    return (head(title, desc, slug)
            + '<script type="application/ld+json">%s</script>\n' % json.dumps(ld, ensure_ascii=False)
            + '</head>\n<body>\n'
            + CHROME
            + '<main id="main">\n'
            + hero(crumb, eyebrow, h1, lead)
            + prose(blocks)
            + TAIL)


def webpage_ld(slug, title, desc):
    url = '%s/%s' % (BASE, slug)
    return {"@context": "https://schema.org", "@type": "WebPage",
            "@id": url + "#webpage", "url": url, "name": title,
            "description": desc, "inLanguage": "en-AU",
            "dateModified": "2026-09-06",
            "isPartOf": {"@id": E.WEBSITE_ID},
            "publisher": {"@id": E.ORG_ID}}


CONTACT = ('<p>Ask us anything about this page. Email '
           '<a href="mailto:%s">%s</a>, call <a href="tel:%s">0414 784 999</a>, '
           'or write to %s, %s %s %s.</p>'
           % (E.EMAIL, E.EMAIL, E.TELEPHONE,
              E.ADDRESS['street'], E.ADDRESS['locality'],
              E.ADDRESS['region'], E.ADDRESS['postcode']))

# ---------------------------------------------------------------- privacy
PRIVACY = [
 ('white', """<h2>The short version</h2>
<p>We collect what you tell us in a brief or an email, we use it to find you a venue, and we pass the relevant parts to the venues we approach on your behalf. We do not sell your information to anybody, and there is no advertising or analytics tracking on this website.</p>

<h2>What we collect, and when</h2>
<p>When you send us a brief we ask for your name, your work email, your organisation and optionally your phone number and role, along with the details of your event: location, dates, delegate numbers, room setup, accommodation needs and anything you write in the notes. Nothing beyond the contact fields and a location is required.</p>
<p>When you subscribe to venue offers we collect your email address, and nothing else.</p>
<p>When you email or call us we keep that correspondence so we can pick the conversation up where it left off.</p>
<p>We do not ask for payment details at any point, because our service is free to you.</p>

<h2>What we do with it</h2>
<p>We use your brief to approach venues on your behalf, to compare what comes back, and to make a recommendation. That means the venues we approach are told the parts of your brief they need in order to quote: your event dates, your numbers, your setup and your requirements. We give a venue your contact details when you have asked us to put you in touch, or when a booking is going ahead and the venue needs to contract with you directly.</p>
<p>We keep a record of the briefs we have handled and the venues we sourced for them, because knowing what a venue actually did for a client two years ago is the reason our advice is worth anything.</p>

<h2>What this website does</h2>
<p>The site has no advertising code, no tracking pixels, no session recording and no analytics account attached to it.</p>
<p>These are the only ways your details leave this page:</p>
<ul>
<li><b>Your brief.</b> When you send a brief it goes to a Google Apps Script service run for us, which records it in a Google Sheet held in a Google account and emails our team a copy as a PDF. The confirmation copy we send back to you is delivered by Resend, an email delivery service. Your brief is stored and processed on Google's and Resend's servers.</li>
<li><b>Venue offers.</b> The offers signup sends your email address to Mailchimp, the service we send offers through. To do that your browser loads a small script from Mailchimp. Mailchimp holds your address until you unsubscribe.</li>
<li><b>Fonts.</b> The site loads its typeface from Google Fonts, which means your browser requests a file from Google and Google sees the request.</li>
<li><b>Your shortlist.</b> When you save a venue, that list is stored in your own browser on your own device. It is not sent to us and we cannot see it. Clearing your browser data clears the list. Your part-finished brief is held the same way, and only until you submit it or close the tab.</li>
</ul>

<h2>How long we keep it</h2>
<p>We keep enquiry and booking records for as long as we have a working relationship with you, and afterwards for as long as we may need them for tax, contractual or dispute purposes. Newsletter subscriptions are kept until you unsubscribe, which you can do from the bottom of any email we send.</p>

<h2>Your rights</h2>
<p>You can ask us what we hold about you, ask us to correct it, or ask us to delete it. Write to the address below and we will come back to you. If we cannot do what you have asked, we will tell you why.</p>
<p>Under the Australian Privacy Principles you can also complain to the Office of the Australian Information Commissioner at <a href="https://www.oaic.gov.au/" rel="noopener">oaic.gov.au</a> if you are not satisfied with how we have handled your information.</p>

<h2>Changes to this page</h2>
<p>If we change how we handle your information we will change this page and update the date at the top of it.</p>
"""),
 ('stone', '<h2>Contact</h2>\n' + CONTACT),
]

# ---------------------------------------------------------------- terms
TERMS = [
 ('white', """<h2>What we do</h2>
<p>We find, compare and negotiate venues and group accommodation on your behalf. We are a sourcing service, not a venue operator and not a travel agent. We do not own, run or control any of the venues on this website.</p>

<h2>What using this site means</h2>
<p>Sending us a brief is a request for us to go and look. It does not book anything, hold anything or commit you to anything. Nothing on this website is an offer capable of acceptance, and no availability shown here is live.</p>

<h2>Who you contract with</h2>
<p>When you decide to proceed, you contract directly with the venue. The venue's own terms govern your booking: its deposit schedule, its cancellation and attrition terms, its minimum spend and its rules about what you can and cannot do on site. We will explain those terms and negotiate them where we can, but we are not a party to them and we cannot waive them on the venue's behalf.</p>

<h2>What we charge you</h2>
<p>Nothing. The venue pays us a commission out of its existing budget, at the same rate whether the booking comes through us or you approach the venue yourself. That is set out in full on our <a href="how-we-are-paid.html">how we are paid</a> page.</p>

<h2>The information on this website</h2>
<p>Capacity figures, room dimensions, accommodation counts and facility details are read from each venue's own published material, and we show you the source and the date we last checked it. Venues change rooms, refurbish, rename spaces and publish figures that contradict their own other pages. We check what we publish, and we tell you when sources disagree, but we cannot guarantee that a figure is current at the moment you read it. Confirm anything that your decision turns on with us, and we will confirm it with the venue.</p>
<p>Where we describe a venue as suitable or unsuitable for a particular event, that is our opinion based on what we have seen and read. It is advice to help you choose, not a warranty.</p>

<h2>Where we have been</h2>
<p>Photographs published under our venue visits are our own, taken by whoever from our team was there on the day, and the date of the visit is shown. A visit records what that room was like on that day. It is not a statement about the venue's current condition.</p>

<h2>Limits</h2>
<p>We take care with the advice we give and the information we publish. To the extent the law allows, we are not liable for loss arising from a venue's own acts, omissions, pricing, availability or performance, or from a decision made on information published here without confirming it with us first. Nothing in these terms excludes any right you have under the Australian Consumer Law that cannot lawfully be excluded.</p>

<h2>The material on this site</h2>
<p>The text, photographs, research and page designs on this website are ours. Venue names and logos belong to their owners. You are welcome to read, print and share our pages for your own event planning. Republishing our venue research as your own is not on.</p>

<h2>Governing law</h2>
<p>These terms are governed by the law of New South Wales, Australia.</p>

<h2>Changes to these terms</h2>
<p>We may update this page. The date at the top tells you when it last changed, and the version in force is the one published when you sent us your brief.</p>
"""),
 ('stone', '<h2>Contact</h2>\n' + CONTACT),
]

PAGES = [
 dict(slug='privacy.html',
      title='Privacy Policy | CVBS',
      desc=('What Conference Venues and Booking Services collects when you send a brief, '
            'what we pass to venues, and everything on this website that sends data anywhere.'),
      crumb='Privacy', eyebrow='Privacy',
      h1='What we do with your information.',
      lead=('You are handing us the details of your event, so you are entitled to know exactly where '
            'they go. Last updated %s.' % PRIVACY_UPDATED),
      blocks=PRIVACY),
 dict(slug='terms.html',
      title='Terms of Service | CVBS',
      desc=('The terms for using Conference Venues and Booking Services: what we do, who you contract '
            'with, what our published venue information is and is not, and what it costs you.'),
      crumb='Terms', eyebrow='Terms',
      h1='The terms, in plain words.',
      lead=('We are a sourcing service. You contract with the venue, not with us, and our service is '
            'free to you. Last updated %s.' % UPDATED),
      blocks=TERMS),
]

for p in PAGES:
    html = page(p['slug'], p['title'], p['desc'], p['crumb'], p['eyebrow'],
                p['h1'], p['lead'], p['blocks'],
                webpage_ld(p['slug'], p['title'], p['desc']))
    io.open(os.path.join(ROOT, p['slug']), 'w', encoding='utf-8').write(html)
    print('wrote %-14s %6d bytes' % (p['slug'], len(html)))

print()
print('NOT stated on either page, because they are not known:')
print('  registered entity name  (entity.py LEGAL_NAME is None)')
print('  ABN                     (entity.py ABN is None)')
print('  the named privacy contact, if it is not Karen')
print('These are on the client decision sheet. Do not invent them.')
