# Competitor usability audit, 5 September 2026

Measured on a 375x812 phone, the way a client actually arrives.

## What the competition does

| Site | Type | H1 position | Words in first screen | First action | Content reached |
|---|---|---|---|---|---|
| VenueNow, home | marketplace | rotating | **24** | form field at 0px | n/a |
| VenueNow, listing | marketplace | none at all | **28** | filters at top | immediately |
| Tagvenue, Sydney | marketplace | 96px | **33** | search form in hero | 0.1 screens |
| The Venue Agency | agency | 0px | 18 | **2,473px** | n/a |
| **CVBS before** | agency | ~250px | **52** | 3,628px to venues | **4.3 screens** |

## The two findings that matter

**1. The marketplaces put a working form in the hero. The agencies put a statement.**
VenueNow's first screen is two dropdowns and a Search button. Tagvenue's is GUESTS,
LOCATION, Search. Neither wastes the first screen explaining itself. The agency
competitors do the opposite: The Venue Agency writes a headline and buries its first
form field 2,473 pixels down, which is three full screens of scrolling before a
visitor can do anything at all.

CVBS was behaving like the agencies. That is the gap.

**2. Nobody scrolls past prose to find what they came for.**
The Sydney page carried 358 words of reference copy between the hero and the first
venue. Good copy, wrong position.

## What was changed

**A brief starter in the hero of every commercial page.** Two fields and a button:
how many people, what kind of event, start your brief. On a city page the destination
is already filled in. It submits straight to `submit-a-brief.html` with `dest`,
`guests` and `type`, which prefills the delegate band, the service and the location,
and writes the notes line. 21 pages: 16 city pages, 4 service pages, the homepage.

This is the marketplace pattern applied to an agency model. The form does not search
a database. **It starts the brief that a person answers**, which is the event that
actually earns CVBS a commission.

**Heroes cut on mobile.** They were 711px of an 844px screen, tuned for desktop and
never capped. Now ~518px. Desktop untouched.

**Reference prose moved below the content.** Every word kept, for AEO. Just no longer
standing between the visitor and the venues.

## Result

| | Before | After |
|---|---|---|
| Sydney: first venue | 3,628px, 4.3 screens | 593px, 0.7 screens |
| Sydney: hero height | 711px | 518px |
| Words in first screen | 52 | 35 to 46 |
| First usable action | scroll required | in the hero, every page |

That lands CVBS between Tagvenue (33 words) and where it was (52), with an action
above the fold on every commercial page.

## What was deliberately NOT copied

**Filters, browse, ratings, prices.** That is the self-service marketplace model.
CVBS has five venue records against VenueNow's thousands; that is not a winnable
fight, and a browsable directory teaches the client to do the job CVBS is paid for.

**The AI assistant.** VenueNow floats an AI chat bubble bottom right. In the same
slot CVBS now puts Karen Jepson: photo, "Director. Finding venues since 1989.",
and a direct mobile number. A person, not a chatbot. It is the one thing on the
page a marketplace structurally cannot match, and it is the whole selling point.

## Next levers, in order

1. The homepage hero copy still leads with a statement rather than the visitor's
   problem. It came out of a nine-option process with the client, so it was left alone.
2. Only Sydney has the full page structure. The other fifteen city pages got the hero
   and the form, but their reference prose has not been reordered because they do not
   yet have venue sections to put above it.
3. Karen's own words on each venue record. The slot is built and empty. Two or three
   sentences per venue makes those pages uncopyable.
