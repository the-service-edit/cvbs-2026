const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  WidthType, BorderStyle, AlignmentType, HeadingLevel, PageBreak,
  ShadingType, Footer, PageNumber, LevelFormat, convertInchesToTwip
} = require('docx');

// ---------------------------------------------------------------- palette
const NAVY = '0A2C52';
const TEAL = '1F818C';
const INK = '0D1F2D';
const MUTED = '5C636B';
const TINT = 'E8F5F6';
const STONE = 'F4F3F0';
const LINE = 'DFE3E6';
const WHITE = 'FFFFFF';

const W = 10106;             // content width in dxa (0.625in margins)
const FONT = 'Inter';

// ---------------------------------------------------------------- helpers
const NONE = { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' };
const noBorders = { top: NONE, bottom: NONE, left: NONE, right: NONE };

function run(text, opt = {}) {
  return new TextRun({
    text,
    font: FONT,
    size: opt.size || 19,
    bold: !!opt.bold,
    color: opt.color || INK,
    allCaps: !!opt.caps,
    characterSpacing: opt.spacing || 0,
  });
}

function p(text, opt = {}) {
  return new Paragraph({
    spacing: { before: opt.before === undefined ? 0 : opt.before, after: opt.after === undefined ? 110 : opt.after, line: opt.line || 262 },
    alignment: opt.align || AlignmentType.LEFT,
    indent: opt.indent,
    children: Array.isArray(text) ? text : [run(text, opt)],
  });
}

function sectionLabel(num, title) {
  return [
    new Paragraph({
      keepNext: true,
      spacing: { before: 0, after: 50 },
      children: [
        run(num + '.', { bold: true, size: 17, color: TEAL, spacing: 26 }),
        run('   ' + title, { bold: true, size: 17, color: TEAL, caps: true, spacing: 26 }),
      ],
    }),
    new Paragraph({
      keepNext: true,
      spacing: { before: 0, after: 110 },
      border: { bottom: { style: BorderStyle.SINGLE, size: 10, color: TEAL, space: 1 } },
      children: [run('', { size: 2 })],
    }),
  ];
}

function h(text) {
  return new Paragraph({
    keepNext: true,
    spacing: { before: 200, after: 70 },
    children: [run(text, { bold: true, size: 20, color: NAVY })],
  });
}

function bullet(text, opt = {}) {
  return new Paragraph({
    numbering: { reference: 'bul', level: 0 },
    spacing: { before: 0, after: 60, line: 256 },
    children: Array.isArray(text) ? text : [run(text, opt)],
  });
}

function cell(children, opt = {}) {
  return new TableCell({
    width: { size: opt.w, type: WidthType.DXA },
    shading: opt.fill ? { type: ShadingType.CLEAR, fill: opt.fill, color: 'auto' } : undefined,
    margins: { top: 70, bottom: 70, left: 120, right: 120 },
    borders: {
      top: { style: BorderStyle.SINGLE, size: 2, color: LINE },
      bottom: { style: BorderStyle.SINGLE, size: 2, color: LINE },
      left: { style: BorderStyle.SINGLE, size: 2, color: LINE },
      right: { style: BorderStyle.SINGLE, size: 2, color: LINE },
    },
    verticalAlign: 'top',
    children: Array.isArray(children) ? children : [children],
  });
}

function th(text, w, opt = {}) {
  return new TableCell({
    width: { size: w, type: WidthType.DXA },
    shading: { type: ShadingType.CLEAR, fill: NAVY, color: 'auto' },
    margins: { top: 80, bottom: 80, left: 120, right: 120 },
    borders: {
      top: { style: BorderStyle.SINGLE, size: 2, color: NAVY },
      bottom: { style: BorderStyle.SINGLE, size: 2, color: NAVY },
      left: { style: BorderStyle.SINGLE, size: 2, color: NAVY },
      right: { style: BorderStyle.SINGLE, size: 2, color: NAVY },
    },
    children: [new Paragraph({
      alignment: opt.right ? AlignmentType.RIGHT : AlignmentType.LEFT,
      spacing: { after: 0 },
      children: [run(text, { bold: true, size: 14, color: WHITE, caps: true, spacing: 22 })],
    })],
  });
}

// rows: array of arrays of {t, bold, color, size, right, fill, w}
function table(widths, headers, rows, opt = {}) {
  const trs = [];
  if (headers) {
    trs.push(new TableRow({
      cantSplit: true,
      tableHeader: true,
      children: headers.map((hd, i) =>
        th(typeof hd === 'string' ? hd : hd.t, widths[i], { right: hd.right })),
    }));
  }
  rows.forEach((r) => {
    trs.push(new TableRow({
      cantSplit: true,
      children: r.map((c, i) => {
        const fill = c.fill || (r.hi ? TINT : undefined);
        return cell(
          (Array.isArray(c.t) ? c.t : String(c.t).split('\n')).map((line, li) =>
            typeof line === 'string'
              ? new Paragraph({
                  alignment: c.right ? AlignmentType.RIGHT : AlignmentType.LEFT,
                  spacing: { after: li === (Array.isArray(c.t) ? c.t.length : String(c.t).split('\n').length) - 1 ? 0 : 50, line: 250 },
                  children: [run(line, { bold: c.bold, size: c.size || 18, color: c.color || INK })],
                })
              : line
          ),
          { w: widths[i], fill }
        );
      }),
    }));
  });
  return new Table({
    columnWidths: widths,
    width: { size: W, type: WidthType.DXA },
    rows: trs,
    margins: { top: 0, bottom: 0, left: 0, right: 0 },
  });
}

function tintRow(cells) { const r = cells; r.hi = true; return r; }

// a shaded callout box drawn as a one cell table
function box(paras, fill) {
  return new Table({
    columnWidths: [W],
    width: { size: W, type: WidthType.DXA },
    rows: [new TableRow({
      cantSplit: true,
      children: [new TableCell({
        width: { size: W, type: WidthType.DXA },
        shading: { type: ShadingType.CLEAR, fill: fill || TINT, color: 'auto' },
        margins: { top: 150, bottom: 150, left: 200, right: 200 },
        borders: {
          top: { style: BorderStyle.SINGLE, size: 2, color: fill || TINT },
          bottom: { style: BorderStyle.SINGLE, size: 2, color: fill || TINT },
          left: { style: BorderStyle.SINGLE, size: 18, color: TEAL },
          right: { style: BorderStyle.SINGLE, size: 2, color: fill || TINT },
        },
        children: paras,
      })],
    })],
  });
}

const gap = (n) => new Paragraph({ spacing: { after: n || 200 }, children: [run('', { size: 2 })] });
const pageBreak = () => new Paragraph({ children: [new PageBreak()] });


// ---------------------------------------------------------------- content
const body = [];

// ---- HEADER ---------------------------------------------------------
body.push(new Paragraph({
  spacing: { before: 0, after: 50 },
  children: [run('SCOPE OF ENGAGEMENT', { bold: true, size: 16, color: TEAL, spacing: 52 })],
}));
body.push(new Paragraph({
  spacing: { before: 50, after: 70, line: 420, lineRule: 'exact' },
  children: [run('The new website, and the digital role around it', { bold: true, size: 32, color: NAVY })],
}));
body.push(new Paragraph({
  spacing: { after: 150 },
  children: [run('What I would build, what I would look after once it is live, and what each of them costs.', { size: 19, color: MUTED })],
}));

body.push(table([2526, 2526, 2527, 2527], null, [
  [
    { t: [
      new Paragraph({ spacing: { after: 30 }, children: [run('PREPARED FOR', { bold: true, size: 13, color: TEAL, spacing: 24 })] }),
      new Paragraph({ spacing: { after: 0 }, children: [run('Conference Venue Booking Service', { size: 17 })] }),
    ] },
    { t: [
      new Paragraph({ spacing: { after: 30 }, children: [run('PREPARED BY', { bold: true, size: 13, color: TEAL, spacing: 24 })] }),
      new Paragraph({ spacing: { after: 0 }, children: [run('Mel, The Service Edit', { size: 17 })] }),
    ] },
    { t: [
      new Paragraph({ spacing: { after: 30 }, children: [run('DATE', { bold: true, size: 13, color: TEAL, spacing: 24 })] }),
      new Paragraph({ spacing: { after: 0 }, children: [run('3 September 2026', { size: 17 })] }),
    ] },
    { t: [
      new Paragraph({ spacing: { after: 30 }, children: [run('VALID UNTIL', { bold: true, size: 13, color: TEAL, spacing: 24 })] }),
      new Paragraph({ spacing: { after: 0 }, children: [run('3 October 2026', { size: 17 })] }),
    ] },
  ],
]));
body.push(gap(180));

// ---- 1. WHERE THIS STARTED -------------------------------------------
body.push(...sectionLabel('1', 'Where this started'));
body.push(p('You brought me in to look after the social. Over the past year the same thing kept surfacing. The posts were landing, and then sending people to a website built in 2012 that did not say clearly what CVBS does. So I built the alternative and showed it to you, and you have decided to go ahead with it.'));
body.push(p('There are two pieces of work in that and I have priced them separately, because they are separate purchases. The website is a project with a start and a finish. What happens afterwards is ongoing, because offers change, venues get added, campaigns need pages to point at, and somebody has to watch whether any of it produces enquiries. Email gives you a direct line to a database you have no regular way of speaking to, social keeps you visible, and with one person on all three a campaign can be live everywhere in a couple of days.'));

// ---- 2. PHASE ONE -----------------------------------------------------
body.push(gap(160));
body.push(...sectionLabel('2', 'Phase one, the new website'));
body.push(p('The design and direction are done and you have approved them. The fee covers everything needed to take that to a finished website, live on your own domain, tested, measured and owned by CVBS.'));

body.push(table([2900, 7206], null, [
  [{ t: '52 published pages', bold: true }, { t: 'Twelve custom templates, including sixteen destination pages, each written for what matters in that place' }],
  [{ t: 'The Sydney venue index', bold: true }, { t: 'Capacity, ceiling height, floor area and setups, every figure read off the venue’s own capacity chart. Built so another city can be added by updating the data' }],
  [{ t: 'One brief form', bold: true }, { t: 'Reached from every page, and it fills itself in from whichever offer, venue or destination the person came from' }],
  [{ t: 'Guides, FAQ and a calculator', bold: true }, { t: 'The questions organisers ask before they are ready to enquire, answered on your site' }],
  [{ t: 'Nothing to renew', bold: true }, { t: 'No content management system, no plugins, no subscriptions behind it' }],
]));

body.push(p('Also in the fee: every template corrected from phone to desktop, the titles, descriptions and structured data behind every page, analytics set up so enquiries are what gets counted, testing across browsers, forms, links and load speed, the switch from your current site with redirects so no existing link breaks, a month of monitoring afterwards and a handover, and the meetings, revisions and project management along the way.', { before: 90 }));

body.push(gap(110));
body.push(table([W], null, [
  [{ t: [
    new Paragraph({ spacing: { after: 40 }, children: [run('WEBSITE INVESTMENT', { bold: true, size: 15, color: TEAL, spacing: 34 })] }),
    new Paragraph({ spacing: { before: 30, after: 60, line: 600, lineRule: 'exact' }, children: [run('$48,000', { bold: true, size: 48, color: NAVY }), run('   plus GST, one off', { size: 19, color: MUTED })] }),
    new Paragraph({ spacing: { after: 0 }, children: [run('Strategy, structure, design, build, content, search foundations, measurement, testing and launch.', { size: 18, color: MUTED })] }),
  ], fill: TINT }],
]));

body.push(gap(200));

body.push(table([3300, 1500, 5306], ['Stage', { t: 'Amount', right: true }, 'What it covers'], [
  [{ t: 'On acceptance' }, { t: '$19,200', right: true, bold: true }, { t: 'Strategy, structure, conversion planning and design, delivered and approved here.' }],
  [{ t: 'Build and content complete' }, { t: '$14,400', right: true, bold: true }, { t: 'Every page built and filled, on a private address for you to sign off.' }],
  [{ t: 'Launch' }, { t: '$14,400', right: true, bold: true }, { t: 'Live on conferencevenues.com.au, redirects in place, forms and analytics tested.' }],
]));

// ---- 3. PHASE TWO -----------------------------------------------------
body.push(gap(150));
body.push(...sectionLabel('3', 'Phase two, the ongoing role'));
body.push(p('Once the site is live it needs running. I would hold two and a half days a week for CVBS, spread over four days so there is something happening on the channels most days. Instagram and Facebook carry on much as they are, and the other five would be new.', { after: 90 }));

body.push(table([2400, 7706], null, [
  [{ t: 'Position', bold: true }, { t: 'Head of Digital, fractional. Contractor, The Service Edit, own ABN, accountable to Karen and Anthony.' }],
  [{ t: 'Authority', bold: true }, { t: 'I would carry out the digital work without clearing each item with you first. Four things I would always bring to you: spending money on CVBS’s behalf, commission or pricing, anything published under Karen’s or Anthony’s name, and brand changes.' }],
  [{ t: 'Digital strategy', bold: true, color: NAVY }, { t: 'Where the enquiries come from over the next twelve months and what we build to get them. The annual plan and the quarterly enquiry review.' }],
  [{ t: 'The website', bold: true, color: NAVY }, { t: 'A weekly publishing and maintenance pass: offers, venue and destination pages, the index, campaign and landing pages, performance and technical health.' }],
  [{ t: 'Social, three channels', bold: true, color: NAVY }, { t: 'Instagram and Facebook carry on as they are. Karen’s LinkedIn written from what she already knows and published under her name. The company page carrying clients, results, the team and each new index city.' }],
  [{ t: 'Email', bold: true, color: NAVY }, { t: 'Two planned sends a month: the program, templates, copy, build, proofing, list growth and hygiene, Mailchimp delivery, with Act! kept as the source database.' }],
  [{ t: 'Content', bold: true, color: NAVY }, { t: 'One venue or destination feature a month, offer write ups, blog and resource pages, carousels, directing the photography and the image library.' }],
  [{ t: 'Measurement', bold: true, color: NAVY }, { t: 'Analytics and Search Console, a one page monthly report, and a monthly check on whether the AI assistants name CVBS when asked who can source a venue.' }],
]));
body.push(gap(110));

body.push(table([W], null, [
  [{ t: [
    new Paragraph({ spacing: { after: 40 }, children: [run('ONGOING INVESTMENT', { bold: true, size: 15, color: TEAL, spacing: 34 })] }),
    new Paragraph({ spacing: { before: 30, after: 60, line: 600, lineRule: 'exact' }, children: [run('$8,650', { bold: true, size: 48, color: NAVY }), run('   per month, plus GST', { size: 19, color: MUTED })] }),
    new Paragraph({ spacing: { after: 0 }, children: [run('$6,900 a month from the start, while the site is being built, when social, email and strategy begin. It moves to $8,650 on the day the site goes live, as the full website and the weekly update cycle come in.', { size: 18, color: MUTED })] }),
  ], fill: TINT }],
]));

body.push(gap(200));

// the fee ladder is held together as one block so it never splits across a page
body.push(new Table({
  columnWidths: [W],
  width: { size: W, type: WidthType.DXA },
  rows: [new TableRow({
    cantSplit: true,
    children: [new TableCell({
      width: { size: W, type: WidthType.DXA },
      margins: { top: 0, bottom: 0, left: 0, right: 0 },
      borders: noBorders,
      children: [
        new Paragraph({ spacing: { before: 40, after: 110, line: 262 }, children: [run('The recommended level is the role CVBS has asked me to take on. The other two show what changes either side of it.')] }),
        table([2600, 6006, 1500], ['Level', 'What separates it', { t: 'Monthly', right: true }], [
          [{ t: 'Digital Management' }, { t: 'One email a month, with the direction set by you' }, { t: '$6,900', right: true, bold: true }],
          tintRow([{ t: 'Head of Digital, recommended', bold: true, color: NAVY }, { t: 'Strategy owned, two emails a month, four index cities a year', bold: true }, { t: '$8,650', right: true, bold: true, color: NAVY }]),
          [{ t: 'Head of Digital, full' }, { t: 'A new channel or market each year, two index cities a quarter' }, { t: '$10,400', right: true, bold: true }],
        ]),
        new Paragraph({ spacing: { after: 0 }, children: [run('', { size: 2 })] }),
      ],
    })],
  })],
}));

// ---- 4. WHERE THE WORK STOPS ------------------------------------------
body.push(gap(180));
body.push(...sectionLabel('4', 'Where the work stops'));
body.push(p('Ordinary publishing, optimisation and maintenance are covered by the monthly fee. Work that gives the site a capability it did not have before is priced before it starts.', { after: 90 }));
body.push(table([5053, 5053], ['Covered by the monthly fee', 'Quoted as its own job'], [
  [{ t: 'Creating, editing and maintaining pages' }, { t: 'A future redesign, rebuild or replacement site' }],
  [{ t: 'Offers, venue and destination content, the index' }, { t: 'New custom functionality of any kind' }],
  [{ t: 'Blog, resource, campaign and landing pages' }, { t: 'Third party integrations and APIs' }],
  [{ t: 'Copy, images, internal links, metadata' }, { t: 'Booking, payment or e-commerce systems' }],
  [{ t: 'Search, assistant and conversion improvements' }, { t: 'Member logins, portals or gated areas' }],
  [{ t: 'Technical health, uptime, broken links, speed' }, { t: 'Moving to a different platform or host' }],
]));
body.push(table([2400, 7706], null, [
  [{ t: 'Outside both fees', bold: true }, { t: 'Paid advertising, large automation builds, a significant event specific digital project, opening a new channel or market, brand identity work, and video or professional photography including the photographer’s fee. Each priced before it starts. Ad spend, Mailchimp, hosting, domains, software, stock images and travel are passed on at cost with your approval first.' }],
  [{ t: 'Not mine to do', bold: true }, { t: 'Answering venue enquiries, quoting, negotiating with venues, handling bookings. I bring you the enquiry and you take it from there.' }],
]));

// ---- 5. WHAT I WOULD NEED FROM YOU ------------------------------------
body.push(gap(180));
body.push(...sectionLabel('5', 'What I would need from you'));
body.push(p('Retainers like this usually stall for the same reason. I am waiting on something from the client and neither of us wrote it down anywhere. So here is my list.'));
body.push(bullet([run('Half an hour of Karen a month, ', { bold: true }), run('on the phone or as a voice note. What a room was really like, what worked, what she would not do again. I cannot write the LinkedIn posts, the city notes or the venue features without it.')]));
body.push(bullet([run('Photographs you own. ', { bold: true }), run('Venue and event images CVBS has the rights to use. Stock will not carry a venue finding business.')]));
body.push(bullet([run('Approvals inside three business days. ', { bold: true }), run('Routine work I have not heard back on after three days I will treat as approved and publish. The four matters under Authority always need a yes.')]));
body.push(bullet([run('Enquiry outcomes each quarter. ', { bold: true }), run('Which ones you quoted, which converted, what they were worth. Without it the quarterly review is a traffic report.')]));
body.push(bullet([run('A few facts confirmed once. ', { bold: true }), run('The commission rate as you charge it, the right titles for Chantelle and Rychelle, and how much venue pricing I can publish. All three end up on public pages.')]));
body.push(bullet([run('Access held in your name. ', { bold: true }), run('Owner level on the domain, hosting, analytics, Search Console, Mailchimp, Act! and the social accounts.')]));
body.push(p('If one of these does not arrive, the piece of work it affects will move, and I will say so in that month’s report.', { before: 70 }));

body.push(gap(200));

// ---- 6. TERMS ---------------------------------------------------------
body.push(...sectionLabel('6', 'Terms'));
body.push(table([2400, 7706], null, [
  [{ t: 'Invoicing', bold: true }, { t: 'The website against the three stages above. The monthly fee monthly in advance, fourteen days to pay. All fees exclude GST.' }],
  [{ t: 'Revisions and changes', bold: true }, { t: 'On the build, two rounds on each template at design stage and one round on each page once the content is in. New content in an existing page is part of the build. A new kind of page, or something the site was not built to do, is priced first.' }],
  [{ t: 'Capacity', bold: true }, { t: 'Two and a half days a week held for CVBS. I do not count or invoice hours. A quiet week is not credited and a heavy one is not surcharged. Some weeks will be mostly social, some mostly website, some built around a campaign, and that is how it is meant to work.' }],
  [{ t: 'Anything outside this', bold: true }, { t: 'I will quote a fixed price before I start. Nothing gets invoiced that you have not agreed to. What changes the arrangement is a permanent addition to what I am responsible for.' }],
  [{ t: 'Term and review', bold: true }, { t: 'The build closes thirty days after launch. The monthly arrangement runs six months, then month to month with sixty days notice either side. A short look at the scope after three months, then a review at the end of the initial term and each July, with CPI as a minimum.' }],
  [{ t: 'Ownership', bold: true }, { t: 'The site, copy, images and pages I produce become yours once the invoice covering them is paid, and the site stays on my hosting until then. The design system and the tools behind it stay mine, with a permanent licence to CVBS for its own site. If we part ways you get the site files, calendar, image library, email templates and reporting workbook within fourteen days.' }],
  [{ t: 'Confidentiality and basis', bold: true }, { t: 'Venue rates, client names, commission arrangements and enquiry data stay with CVBS. This is a contract for services: The Service Edit invoices under its own ABN, works with other clients and controls how the work is performed, and each party remains responsible for any tax, superannuation or employment obligations that apply by law.' }],
]));

// ---- 7. ACCEPTANCE ----------------------------------------------------
body.push(gap(150));
body.push(...sectionLabel('7', 'Acceptance'));
body.push(p('Signing here adopts this document as Schedule 1 to our services agreement and confirms the level selected. Either of us can suggest a change at any time, and it takes effect once we have both agreed it in writing.', { after: 110 }));

body.push(table([5053, 5053], null, [
  [
    { t: [
      new Paragraph({ spacing: { after: 30 }, children: [run('PHASE ONE, THE WEBSITE', { bold: true, size: 13, color: TEAL, spacing: 24 })] }),
      new Paragraph({ spacing: { after: 0 }, children: [run('$48,000 plus GST, one off', { bold: true, size: 20, color: NAVY })] }),
    ], fill: TINT },
    { t: [
      new Paragraph({ spacing: { after: 30 }, children: [run('PHASE TWO, THE ONGOING ROLE', { bold: true, size: 13, color: TEAL, spacing: 24 })] }),
      new Paragraph({ spacing: { after: 0 }, children: [run('$8,650 per month plus GST', { bold: true, size: 20, color: NAVY }), run('  ($6,900 until the site is live)', { size: 16, color: MUTED })] }),
    ], fill: TINT },
  ],
]));
body.push(gap(150));

function sigBlock(who) {
  return [
    new Paragraph({ spacing: { after: 90 }, children: [run(who, { bold: true, size: 18, color: NAVY })] }),
    new Paragraph({ spacing: { after: 40 }, border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: MUTED, space: 5 } }, children: [run('', { size: 18 })] }),
    new Paragraph({ spacing: { after: 130 }, children: [run('Name and signature', { size: 16, color: MUTED })] }),
    new Paragraph({ spacing: { after: 40 }, border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: MUTED, space: 5 } }, children: [run('', { size: 18 })] }),
    new Paragraph({ spacing: { after: 0 }, children: [run('Date and level selected', { size: 16, color: MUTED })] }),
  ];
}

body.push(table([5053, 5053], null, [
  [
    { t: sigBlock('For Conference Venue Booking Service') },
    { t: sigBlock('For The Service Edit') },
  ],
]));

// ---------------------------------------------------------------- doc
const doc = new Document({
  creator: 'The Service Edit',
  title: 'CVBS Scope of Engagement, September 2026',
  description: 'The new CVBS website and the ongoing digital role',
  numbering: {
    config: [{
      reference: 'bul',
      levels: [{
        level: 0,
        format: LevelFormat.BULLET,
        text: '•',
        alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 280, hanging: 190 } }, run: { color: TEAL, font: FONT } },
      }],
    }],
  },
  styles: {
    default: {
      document: { run: { font: FONT, size: 19, color: INK }, paragraph: { spacing: { line: 262 } } },
    },
  },
  sections: [{
    properties: {
      page: { margin: { top: 850, right: 900, bottom: 780, left: 900 } },
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          spacing: { before: 120 },
          border: { top: { style: BorderStyle.SINGLE, size: 2, color: LINE, space: 6 } },
          children: [
            run('Commercial in confidence', { size: 14, color: MUTED }),
            new TextRun({ text: '\t\t', font: FONT }),
            run('Page ', { size: 14, color: MUTED }),
            new TextRun({ children: [PageNumber.CURRENT], size: 14, color: MUTED, font: FONT }),
            run(' of ', { size: 14, color: MUTED }),
            new TextRun({ children: [PageNumber.TOTAL_PAGES], size: 14, color: MUTED, font: FONT }),
          ],
          tabStops: [
            { type: 'center', position: W / 2 },
            { type: 'right', position: W },
          ],
        })],
      }),
    },
    children: body,
  }],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync('CVBS-Scope-of-Engagement-Sep-2026.docx', buf);
  console.log('written', buf.length, 'bytes');
});
