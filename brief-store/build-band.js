/* Builds the navy header band used by BriefPdf.html.

   WHY THIS EXISTS: Apps Script's HTML to PDF converter throws away every
   background colour. CSS background, bgcolor attribute, both. Text colour,
   borders and images survive. So the navy band is not a coloured table cell,
   it is a PNG with the colour, the logo and the title already baked in.

   HOW TO RUN IT: open https://conferencevenues.com.au (or the GitHub Pages
   origin) in Chrome, open the console, paste this whole file, press enter.
   It prints the base64. Paste that over __BAND__ in BriefPdf.html.

   Run it in a BROWSER, not Node. It needs canvas and the real Helvetica.
*/
(async () => {
  const W = 1400, H = 170;
  const c = document.createElement('canvas'); c.width = W; c.height = H;
  const x = c.getContext('2d');
  x.fillStyle = '#0A2C52'; x.fillRect(0, 0, W, H);

  const img = new Image();
  img.crossOrigin = 'anonymous';
  img.src = 'https://the-service-edit.github.io/cvbs-2026/assets/img/logo-white.png';
  await new Promise((res, rej) => { img.onload = res; img.onerror = rej; });

  const lh = 92, lw = Math.round(lh * img.width / img.height);
  x.drawImage(img, 44, (H - lh) / 2, lw, lh);

  const tx = 44 + lw + 40;
  x.fillStyle = '#3BC9D9';
  x.font = '600 19px Helvetica, Arial, sans-serif';
  let cx = tx;
  for (const ch of 'CONFERENCE VENUES') { x.fillText(ch, cx, H / 2 - 22); cx += x.measureText(ch).width + 4.6; }

  x.fillStyle = '#ffffff';
  x.font = 'bold 44px Helvetica, Arial, sans-serif';
  x.fillText('Venue brief', tx - 1, H / 2 + 30);

  console.log(c.toDataURL('image/png').split(',')[1]);
})();
