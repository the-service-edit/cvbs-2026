# Hotel group marks for the venue visits band

Used by the "Hotel groups represented across our venue network" band at the
bottom of /venue-visits/. Nothing else on the site reads this folder.

## The rule

A group only appears in the band when CVBS has walked a room inside it, and the
band lists those rooms. Never add a mark for a group with no walked record.

## Current state, 10 Sep 2026

| File            | Group                        | Status                          |
|-----------------|------------------------------|---------------------------------|
| accor.png       | Accor                        | live, background knocked out    |
| capella.png     | Capella Hotel Group          | live, background knocked out    |
| crown.png       | Crown Resorts                | live, checkerboard knocked out  |
| evt.png         | EVT Hotels & Resorts         | live, background knocked out    |
| ihg.png         | IHG Hotels & Resorts         | live                            |
| marriott.png    | Marriott International       | live, background knocked out    |
| tfe-hotels.png  | TFE Hotels                   | live, background knocked out    |
| the-star.png    | The Star Entertainment Group | live                            |
| hilton.png      | Hilton                       | live, background knocked out    |

All nine marks are live. The first Hilton file supplied was the reversed lockup,
white type on a navy box, which is unusable on a white ground; it was replaced
on 10 Sep with the standard black wordmark in its rule, knocked out and trimmed.

`accor.jpeg`, `hilton.jpeg` and `tfe-hotels.jpeg` are the original sources.
Nothing references them. They can go whenever the folder is next tidied.

## How the band fails safe

The band shows the group NAME as text by default. The image replaces the text
only after it loads successfully, via `onload`, never `onerror`. A missing or
broken file therefore degrades to a legible wordmark rather than a blank space,
which is what went wrong on the client logo wall in September.

**Never put `loading="lazy"` on these images.** They start at `display:none`, so
a lazy image is never considered in-viewport, never loads, and its `onload`
never fires. Every logo silently stays as text and the band looks unfinished.
This was caught on 10 Sep by rendering the page rather than trusting the markup.

## What a usable file looks like

- Transparent PNG or SVG. A fully opaque file renders as a solid block.
- 250px tall or more, artwork trimmed hard to its own bounding box with no
  baked-in padding, or the optical sizing will be wrong.
- The positive version of the mark, dark artwork for a white ground. Not the
  reversed or boxed version.
- No lockups with taglines.

## Sizing

Per-mark height is set inline on each row in venue-visits/index.html as `--mh`.
Set it per file, never one height for all of them. A stacked mark with a
wordmark under it reads far smaller than a single-line horizontal lockup at the
same pixel height, which is why the stacked marks run 62 to 66px, Hilton's boxed
wordmark runs 38px because the filled rule carries its own weight, and EVT, a
wide one-line lockup, runs 26px.

## Before publishing any of these

These are third party trademarks. The band deliberately ends with "We are
independent of every group listed here. CVBS is not a partner, agent or
preferred supplier of any hotel group." Do not remove that line, and do not move
these marks under any heading using the words partner, preferred, accredited or
official. Never use the Marriott Bonvoy mark: Bonvoy is a loyalty programme and
displaying it asserts a corporate relationship that does not exist.
