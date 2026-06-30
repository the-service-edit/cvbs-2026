# Carousel source (for Claude, not for posting)

These Python files generate the CVBS Instagram carousels. They hold the full
design system (liquid glass over venue photos, brand colours, Inter) and the copy.

To re-render or make a new post, Claude:
1. Copies these scripts + the fonts + the venue images into a build dir
   (images come from ../assets/img in the main site folder).
2. Edits the copy / image / numbers in the script.
3. Renders to 1080x1350 PNG (and PDF) with headless chromium.

Pipeline notes: needs Inter TTFs (here in fonts/), and in the sandbox a
libXdamage.so.1 stub so headless chromium launches. Backgrounds use object-position
crops so one photo can vary across slides.

Five templates: 01 budget mistakes, 02 searched vs sourced, 03 client result,
04 offer/EDM, 05 site visit.
