/* ==========================================================================
   CVBS brief store
   Receives a submitted brief from submit-a-brief.html, records it in the
   bound Google Sheet, renders it as a CVBS branded PDF and emails that PDF
   to the CVBS team.

   Order matters. The sheet write happens FIRST and the email second, so a
   mail failure can never lose a lead. Setup steps are in README.md.
   ========================================================================== */

var SHEET_NAME  = "briefs";
var SHARED_KEY  = "cvbs-2026-brief";              // must match BRIEF_ENDPOINT_KEY in submit-a-brief.html
var TZ          = "Australia/Sydney";
var NL          = String.fromCharCode(10);

/* Who receives the internal brief.
   HANDED OVER 8 Sep 2026. Address confirmed by Mel: aj@conferencevenues.com.au.
   Everything CVBS is on conferencevenues.com.AU, not .com. Karen is not on this
   list; add her to CC if that changes. */
var LIVE        = true;
var TO          = LIVE ? ["aj@conferencevenues.com.au"]
                       : ["hello@theserviceedit.com"];
var CC          = [];
var FAIL_ALERT  = "hello@theserviceedit.com";   // told when a send fails but the brief was saved

/* The enquirer also gets their own brief back as a PDF.
   ON since 8 Sep 2026, but it is GATED: the copy is refused unless a Resend key
   is present, because a client who enquired at conferencevenues.com.au must
   never receive mail from theserviceedit.com. Until RESEND_API_KEY is set in
   Script Properties, every brief sends Mel a failure notice plus a
   [CLIENT PREVIEW] copy, and the enquirer receives nothing. The moment the key
   lands, client copies start sending with no further code change and no
   redeploy. See sendClientCopy_ and README.md. */
var CLIENT_LIVE = true;

/* Where the email images and links point. Flip to https://conferencevenues.com.au
   at cutover. Matches the EDMs, including the ?v=3 cache stamp, which is
   deliberate: Apple Mail and Gmail cache image URLs permanently, so a URL that
   failed once stays broken. Reuse proven URLs, never invent a version. */
var ASSET_BASE  = "https://the-service-edit.github.io/cvbs-2026";

/* 11 Sep 2026: the cutover flip is a Script Property now, so it needs no code
   release. Project Settings > Script Properties > ASSET_BASE =
   https://www.conferencevenues.com.au once the new site is live there. Until
   the property exists, the constant above is used. */
function assetBase_() {
  try {
    var v = PropertiesService.getScriptProperties().getProperty("ASSET_BASE");
    if (v && /^https:\/\/[a-z0-9.-]+(\/[A-Za-z0-9._~\/-]*)?$/.test(v)) return v.replace(/\/+$/, "");
  } catch (ignore) {}
  return ASSET_BASE;
}

/* Two sender names on purpose. The internal one is a work queue and wants to be
   scannable in an inbox. The client one follows the CVBS rule that the inbox row
   is the business, the same as every Mailchimp send. */
var FROM_NAME_CLIENT = "Conference Venues";

/* From address. Only used when a Resend API key is present in Script
   Properties. Without one the script falls back to MailApp, which sends from
   the Google account that owns this script. See README.md. */
var FROM_NAME   = "CVBS Website Enquiry";
var FROM_EMAIL  = "briefs@mail.conferencevenues.com.au";

/* Ceiling on sends per rolling hour. The endpoint is public, so this is the
   difference between a bad afternoon and a mail bomb. Briefs over the ceiling
   are still saved to the sheet, they just do not trigger an email. */
var MAX_PER_HOUR = 30;

/* Field order for the sheet. Adding a field means adding it here AND to the
   PDF sections below, or it lands in the sheet and never reaches the paper. */
var COLS = [
  "ref","received","first","last","email","phone","company","role",
  "services","location","locationDetail","radius","delegates",
  "startDate","endDate","flexibleDates","duration","accommodation",
  "venueType","requirements","setup","budgetPp","budgetTotal","notes",
  "offer","venue","referral","source","status","sent"
];

/* ---------------------------------------------------------------- plumbing */

/* The project is standalone, not bound to a sheet, so it holds the sheet id in
   Script Properties. First run creates the sheet and remembers it. */
function spreadsheet_() {
  var props = PropertiesService.getScriptProperties();
  var id = props.getProperty("SHEET_ID");
  if (id) {
    try { return SpreadsheetApp.openById(id); } catch (err) { /* fall through and remake */ }
  }
  var ss = SpreadsheetApp.create("CVBS Briefs");
  props.setProperty("SHEET_ID", ss.getId());
  return ss;
}

function sheet_() {
  var ss = spreadsheet_();
  var sh = ss.getSheetByName(SHEET_NAME);
  if (!sh) { sh = ss.insertSheet(SHEET_NAME); }
  if (sh.getLastRow() === 0) { sh.appendRow(COLS); sh.setFrozenRows(1); }
  return sh;
}

/* Google Sheets treats a leading = + - or @ as the start of a formula, so
   "+61 400 000 000" lands in the phone column as #ERROR! and the number is
   gone. Found on the first live test, 8 Sep 2026. A leading apostrophe forces
   text; Sheets does not store it, so the value reads back clean. */
function cell_(v) {
  var t = (v === null || v === undefined) ? "" : String(v);
  return /^[=+\-@\t\r]/.test(t) ? "'" + t : t;
}

function out_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

function str_(v) {
  if (v === null || v === undefined) return "";
  if (Object.prototype.toString.call(v) === "[object Array]") {
    return v.filter(function (x) { return x !== null && x !== undefined && String(x) !== ""; })
            .map(function (x) { return String(x).trim(); }).join(", ");
  }
  return String(v).trim();
}

/* Everything that reaches the PDF goes through this. The brief is typed by a
   stranger and rendered as HTML. */
function esc_(v) {
  return str_(v).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
                .replace(/"/g, "&quot;");
}

function escLines_(v) {
  return esc_(v).replace(/\r\n|\r|\n/g, "<br>");
}

/* Lead time is arithmetic, not a guess, and it is the first thing that decides
   how a brief is triaged. Under six weeks on a 100 plus delegate event is a
   different conversation from eighteen months out. */
function leadTime_(startDate) {
  var m = str_(startDate).match(/^(\d{4})-(\d{2})-(\d{2})$/);
  if (!m) return "";
  var start = new Date(Number(m[1]), Number(m[2]) - 1, Number(m[3]));
  var days = Math.round((start - new Date()) / 86400000);
  if (days < 0)  return "Date has passed, check with them";
  if (days < 43) return Math.max(days, 0) + " days away, tight";
  var weeks = Math.round(days / 7);
  if (weeks < 53) return weeks + " weeks away";
  return Math.round(days / 30.44) + " months away";
}

/* Compact dates for the email fact row. "Tue 17 Nov 2026 to Thu 19 Nov 2026"
   wraps to three lines in a 600px column and makes the row ragged.
   "17 to 19 Nov 2026" says the same thing in one. */
function shortDates_(rec) {
  var a = str_(rec.startDate).match(/^(\d{4})-(\d{2})-(\d{2})$/);
  if (!a) return rec.flexibleDates ? "Flexible" : "";
  var d1 = new Date(Number(a[1]), Number(a[2]) - 1, Number(a[3]));
  var b = str_(rec.endDate).match(/^(\d{4})-(\d{2})-(\d{2})$/);
  var pre = rec.flexibleDates ? "Flexible, around " : "";
  if (!b || rec.endDate === rec.startDate) {
    return pre + Utilities.formatDate(d1, TZ, "d MMM yyyy");
  }
  var d2 = new Date(Number(b[1]), Number(b[2]) - 1, Number(b[3]));
  if (a[1] === b[1] && a[2] === b[2]) {
    return pre + Utilities.formatDate(d1, TZ, "d") + " to " + Utilities.formatDate(d2, TZ, "d MMM yyyy");
  }
  if (a[1] === b[1]) {
    return pre + Utilities.formatDate(d1, TZ, "d MMM") + " to " + Utilities.formatDate(d2, TZ, "d MMM yyyy");
  }
  return pre + Utilities.formatDate(d1, TZ, "d MMM yyyy") + " to " + Utilities.formatDate(d2, TZ, "d MMM yyyy");
}

function niceDate_(v) {
  var s = str_(v);
  if (!s) return "";
  var m = s.match(/^(\d{4})-(\d{2})-(\d{2})$/);
  if (!m) return s;
  var d = new Date(Number(m[1]), Number(m[2]) - 1, Number(m[3]));
  return Utilities.formatDate(d, TZ, "EEE d MMM yyyy");
}

function underHourlyCap_() {
  try {
    var cache = CacheService.getScriptCache();
    var k = "cvbs-brief-count-" + Utilities.formatDate(new Date(), TZ, "yyyyMMddHH");
    var n = Number(cache.get(k) || 0) + 1;
    cache.put(k, String(n), 3900);
    return n <= MAX_PER_HOUR;
  } catch (err) { return true; }
}

/* -------------------------------------------------------------- validation */

/* 11 Sep 2026. Everything the browser sends is checked here, because the page,
   its key and this endpoint are all public. Unknown fields are dropped, every
   field is cut to a length ceiling, and the fields that are echoed back to the
   enquirer in the client copy cannot carry links, so the form cannot be used
   to send CVBS-branded mail with someone else's content in it. */
var LIMITS = {
  first: 60, last: 60, email: 120, phone: 40, company: 120, role: 80,
  location: 80, locationDetail: 120, radius: 60, delegates: 12,
  startDate: 10, endDate: 10, flexibleDates: 10, duration: 60, accommodation: 60,
  venueType: 120, setup: 60, budgetPp: 40, budgetTotal: 40, notes: 6000,
  offer: 120, venue: 160, referral: 120, services: 400, requirements: 600
};
var ECHOED = ["first", "locationDetail", "delegates"];

function clean_(f) {
  var out = {}, bad = [];
  Object.keys(LIMITS).forEach(function (k) {
    var v = str_(f[k]).replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F\u007F]/g, "");
    out[k] = v.slice(0, LIMITS[k]);
  });
  if (!/^[^@\s<>"']{1,64}@[^@\s<>"']+\.[A-Za-z]{2,}$/.test(out.email)) bad.push("email");
  if (!out.first) bad.push("first");
  if (out.delegates && !/\d/.test(out.delegates)) bad.push("delegates");
  ["startDate", "endDate"].forEach(function (k) {
    if (out[k] && !/^\d{4}-\d{2}-\d{2}$/.test(out[k])) bad.push(k);
  });
  ECHOED.forEach(function (k) {
    if (/(https?:|www\.|<|>|\/\/)/i.test(out[k])) bad.push(k);
  });
  return { rec: out, bad: bad };
}

/* One alert per 15 minutes at most, and never the raw request body. Before
   this, every unparseable POST emailed its whole body to the alert address, so
   a bot could fill an inbox with its own content. A real failure still alerts,
   with the validated fields, because that alert may be the only copy of a lead. */
function alertOnce_(subject, body) {
  try {
    var cache = CacheService.getScriptCache();
    if (cache.get("cvbs-alert-lock")) {
      console.error("Alert suppressed (throttled): " + subject + NL + body);
      return;
    }
    cache.put("cvbs-alert-lock", "1", 900);
  } catch (ignore) {}
  try { MailApp.sendEmail(FAIL_ALERT, subject, body); } catch (ignore) {}
}

/* ------------------------------------------------------------------ intake */

function doPost(e) {
  var saved = false, ref = "", f = {};
  var raw = (e && e.postData && e.postData.contents) || "";
  if (raw.length > 20000) return out_({ ok: false, error: "too large" });

  /* Malformed or unkeyed requests are answered and forgotten. No alert: they
     are not briefs, and alerting on them is how the inbox got flooded. */
  var p;
  try { p = JSON.parse(raw || "{}"); } catch (err) { return out_({ ok: false, error: "bad request" }); }
  if (!p || typeof p !== "object" || p.key !== SHARED_KEY) return out_({ ok: false, error: "bad key" });

  /* Honeypot. A real visitor never fills this. Answer ok so the bot learns
     nothing and moves on. */
  if (str_(p.botcheck)) return out_({ ok: true, ref: "" });

  var checked = clean_(p.fields || {});
  if (checked.bad.length) {
    console.warn("Brief refused, invalid fields: " + checked.bad.join(", "));
    return out_({ ok: false, error: "invalid", fields: checked.bad });
  }
  f = checked.rec;

  try {

    var now = new Date();
    var sh  = sheet_();
    ref = "CVB-" + Utilities.formatDate(now, TZ, "yyMMdd") + "-" +
          ("00" + (sh.getLastRow())).slice(-3);

    var rec = {
      ref: ref,
      received: Utilities.formatDate(now, TZ, "yyyy-MM-dd HH:mm"),
      first: str_(f.first), last: str_(f.last), email: str_(f.email),
      phone: str_(f.phone), company: str_(f.company), role: str_(f.role),
      services: str_(f.services), location: str_(f.location),
      locationDetail: str_(f.locationDetail), radius: str_(f.radius),
      delegates: str_(f.delegates), startDate: str_(f.startDate),
      endDate: str_(f.endDate), flexibleDates: str_(f.flexibleDates),
      duration: str_(f.duration), accommodation: str_(f.accommodation),
      venueType: str_(f.venueType), requirements: str_(f.requirements),
      setup: str_(f.setup), budgetPp: str_(f.budgetPp),
      budgetTotal: str_(f.budgetTotal), notes: str_(f.notes),
      offer: str_(f.offer), venue: str_(f.venue), referral: str_(f.referral),
      source: str_(p.page).slice(0, 80), status: "new", sent: ""
    };

    sh.appendRow(COLS.map(function (c) { return cell_(rec[c]); }));
    saved = true;

    if (!underHourlyCap_()) return out_({ ok: true, ref: ref });

    var result = sendBrief_(rec);
    try {
      sh.getRange(sh.getLastRow(), COLS.indexOf("sent") + 1).setValue(result);
    } catch (ignore) {}

    return out_({ ok: true, ref: ref });

  } catch (err) {
    /* The visitor is told the truth: if the brief is in the sheet it is safe,
       and the team can be prompted by hand. If it is not, the page shows its
       fallback and the visitor is sent to the contact page. */
    if (!saved) {
      alertOnce_("CVBS brief endpoint failed",
        "A valid brief was submitted and NOT saved. Its fields are below so the lead is not lost." +
        NL + NL + String(err) + NL + NL +
        Object.keys(f).filter(function (k) { return f[k]; })
          .map(function (k) { return k + ": " + f[k]; }).join(NL));
      return out_({ ok: false, error: "server" });
    }
    return out_({ ok: true, ref: ref });
  }
}

function doGet() {
  return out_({ ok: true, service: "cvbs-brief-store" });
}

/* -------------------------------------------------------------------- send */

function renderPdf_(rec) {
  try {
    return Utilities.newBlob(renderBriefHtml_(rec), "text/html", "x")
      .getAs("application/pdf")
      .setName("CVBS-brief-" + rec.ref + "-" +
               (rec.company || rec.last).replace(/[^A-Za-z0-9]+/g, "-") + ".pdf");
  } catch (err) {
    return null;
  }
}

/* One way out for every email. Resend when the domain is configured, the
   owning Google account otherwise. */
function deliver_(m) {
  var apiKey = PropertiesService.getScriptProperties().getProperty("RESEND_API_KEY");
  if (apiKey) {
    try {
      var payload = {
        from: (m.fromName || FROM_NAME) + " <" + FROM_EMAIL + ">",
        to: m.to,
        reply_to: m.replyTo,
        subject: m.subject,
        text: m.body
      };
      if (m.html) payload.html = m.html;
      if (m.cc && m.cc.length) payload.cc = m.cc;
      if (m.pdf) {
        payload.attachments = [{
          filename: m.pdf.getName(),
          content: Utilities.base64Encode(m.pdf.getBytes())
        }];
      }
      var res = UrlFetchApp.fetch("https://api.resend.com/emails", {
        method: "post",
        contentType: "application/json",
        headers: { Authorization: "Bearer " + apiKey },
        payload: JSON.stringify(payload),
        muteHttpExceptions: true
      });
      if (res.getResponseCode() < 300) return "resend";
      notifyFailure_(m.ref, "Resend returned " + res.getResponseCode() + ": " + res.getContentText());
    } catch (err) {
      notifyFailure_(m.ref, "Resend threw: " + String(err));
    }
  }

  try {
    var opts = {
      to: m.to.join(","),
      cc: (m.cc || []).join(","),
      replyTo: m.replyTo,
      subject: m.subject,
      body: m.body,
      name: m.fromName || FROM_NAME,
      attachments: m.pdf ? [m.pdf] : []
    };
    if (m.html) opts.htmlBody = m.html;
    MailApp.sendEmail(opts);
    return apiKey ? "mailapp-fallback" : "mailapp";
  } catch (err) {
    notifyFailure_(m.ref, "MailApp threw: " + String(err));
    return "FAILED";
  }
}

function sendBrief_(rec) {
  var pdf = renderPdf_(rec);
  var internal = deliver_(internalMail_(rec, pdf));
  var client = sendClientCopy_(rec, pdf);
  return internal + " / client:" + client;
}

/* The internal copy. Reply-to is the enquirer, so a reply answers the client
   directly instead of bouncing around. */
function internalMail_(rec, pdf) {
  var L = [
    "A new brief came in through the website. The full brief is attached as a PDF.",
    "",
    "Reference   " + rec.ref,
    "Received    " + rec.received + " AEST",
    "From        " + rec.first + " " + rec.last + ", " + rec.company,
    "Email       " + rec.email
  ];
  if (rec.phone) L.push("Phone       " + rec.phone);
  L.push("Delegates   " + rec.delegates);
  L.push("Location    " + rec.location + (rec.locationDetail ? " (" + rec.locationDetail + ")" : ""));
  L.push("Dates       " + (rec.flexibleDates ? "Flexible. " : "") + niceDate_(rec.startDate) +
         (rec.endDate ? " to " + niceDate_(rec.endDate) : ""));
  L.push("");
  if (rec.notes) { L.push("In their words:"); L.push(rec.notes); L.push(""); }
  L.push("Reply to this email and it goes straight to " + rec.email + ".");
  if (!pdf) L.push("", "The PDF could not be rendered this time. Every field is in the sheet.");

  return {
    ref: rec.ref,
    to: TO,
    cc: CC,
    replyTo: rec.email,
    subject: "New brief " + rec.ref + ": " + (rec.company || (rec.first + " " + rec.last)) +
             ", " + (rec.delegates || "?") + " delegates, " + (rec.location || "location TBC"),
    body: L.join(NL),
    pdf: pdf
  };
}

/* The enquirer's own copy. Deliberately harder to send than the internal one.
   A client who enquired at conferencevenues.com.au receiving mail from
   theserviceedit.com is a trust break and reads like phishing, so this refuses
   to reach a real client until the CVBS domain is configured in Resend. Until
   then it lands with Mel, clearly marked, so the wording can be approved. */
function sendClientCopy_(rec, pdf) {
  var hasDomain = !!PropertiesService.getScriptProperties().getProperty("RESEND_API_KEY");
  var toClient  = CLIENT_LIVE && hasDomain;

  if (CLIENT_LIVE && !hasDomain) {
    notifyFailure_(rec.ref, "CLIENT_LIVE is on but no RESEND_API_KEY is set, so the client copy " +
      "was NOT sent to the enquirer. It would have come from the wrong domain. " +
      "Finish the Resend setup in brief-store/README.md.");
  }

  var L = [
    "Hi " + (rec.first || "there") + ",",
    "",
    "Thank you, we have your brief.",
    "",
    "One of the team will be in touch, and you will have a costed shortlist " +
      "within 48 hours. It costs you nothing.",
    "",
    "Your brief is attached as a PDF, so you have a copy to keep or to forward.",
    "",
    "Reference   " + rec.ref,
    "",
    "If anything changes, reply to this email and we will update it before we " +
      "go looking.",
    "",
    "Conference Venues and Booking Services",
    "Sourcing conference venues and group accommodation since 1989"
  ];

  if (!toClient) {
    L = ["[PREVIEW ONLY. Not sent to the client.",
         " This is what " + rec.email + " would have received.]",
         ""].concat(L);
  }

  return deliver_({
    ref: rec.ref,
    to: toClient ? [rec.email] : [FAIL_ALERT],
    cc: [],
    replyTo: TO[0],
    fromName: FROM_NAME_CLIENT,
    subject: (toClient ? "" : "[CLIENT PREVIEW] ") + "Your venue brief, " + rec.ref,
    body: L.join(NL),
    html: clientHtml_(rec),
    pdf: pdf
  }) + (toClient ? "" : "-preview");
}

function notifyFailure_(ref, detail) {
  try {
    MailApp.sendEmail(FAIL_ALERT, "CVBS brief " + ref + " needs a look",
      detail + NL + NL + "The brief is " + ref + " in the briefs sheet. Nothing is lost.");
  } catch (ignore) {}
}

/* The branded HTML body for the client copy, built on the wave EDM system.
   The plain text version above is still sent alongside it, and is what a text
   only client sees. */
function clientHtml_(rec) {
  var t = HtmlService.createTemplateFromFile("ClientEmail");
  var dates = shortDates_(rec) || (rec.flexibleDates ? "Flexible" : "");

  t.rec       = rec;
  t.base      = assetBase_();
  t.replyTo   = TO[0];
  t.firstName = esc_(rec.first) || "there";
  t.facts     = [
    { label: "Delegates", value: esc_(rec.delegates) || "To confirm" },
    { label: "Location",  value: esc_(rec.locationDetail || rec.location) || "To confirm" },
    { label: "Dates",     value: esc_(dates) || "To confirm" }
  ];
  return t.evaluate().getContent();
}

/* ------------------------------------------------------------------ render */

function renderBriefHtml_(rec) {
  var t = HtmlService.createTemplateFromFile("BriefPdf");

  var dates = rec.flexibleDates
    ? (rec.startDate ? "Flexible, around " + niceDate_(rec.startDate) : "Flexible, not yet set")
    : (niceDate_(rec.startDate) + (rec.endDate && rec.endDate !== rec.startDate ? " to " + niceDate_(rec.endDate) : ""));
  if (!str_(dates)) dates = "Not stated";
  /* 11 Sep 2026: escape each typed value first, then add markup. The budget
     used to go into the PDF unescaped, and the dates line escaped the markup
     this function had just built, so the lead time printed as raw tags. */
  var lead = leadTime_(rec.startDate);
  var datesHtml = esc_(dates) +
    (lead ? '<br><span style="font-weight:normal;font-size:9pt;color:#197683">' + esc_(lead) + "</span>" : "");

  var budget = [rec.budgetPp ? esc_(rec.budgetPp) + " per delegate per day" : "",
                rec.budgetTotal ? esc_(rec.budgetTotal) + " total" : ""]
    .filter(String).join("<br>");

  t.rec       = rec;
  t.esc       = esc_;
  t.escLines  = escLines_;
  t.headline  = [
    { label: "Delegates",  value: esc_(rec.delegates) || "Not stated" },
    { label: "Location",   value: esc_(rec.locationDetail || rec.location) || "Not stated" },
    { label: "Dates",      value: datesHtml },
    { label: "Budget",     value: budget || "Not stated" }
  ];
  t.brief = [
    ["What they need",      esc_(rec.services)],
    ["Venue type",          esc_(rec.venueType)],
    ["Travel radius",       esc_(rec.radius)],
    ["Duration",            esc_(rec.duration)],
    ["Accommodation",       esc_(rec.accommodation)],
    ["On site",             esc_(rec.requirements)],
    ["Room setup",          esc_(rec.setup)],
    ["Enquiring about",     esc_([rec.venue, rec.offer].filter(String).join(" / "))]
  ].filter(function (r) { return r[1]; });
  t.contact = [
    ["Name",            esc_((rec.first + " " + rec.last).trim())],
    ["Company",         esc_(rec.company)],
    ["Role",            esc_(rec.role)],
    ["Email",           esc_(rec.email)],
    ["Phone",           esc_(rec.phone)],
    ["Heard about us",  esc_(rec.referral)]
  ].filter(function (r) { return r[1]; });

  return t.evaluate().getContent();
}

/* RUN THIS FIRST, once, from the editor.
   It authorises the project, creates the CVBS Briefs sheet, writes a sample PDF
   to Drive and emails it to you, so every moving part is proven before the form
   is wired. Look in the execution log for the two links. */
function setup() {
  var ss = spreadsheet_();
  sheet_();
  var pdf = sampleBlob_();
  DriveApp.createFile(pdf);
  MailApp.sendEmail({
    to: TO.join(","),
    subject: "CVBS brief store is working",
    body: ["This is the sample brief. The real ones will look the same.",
           "", "Sheet: " + ss.getUrl()].join(NL),
    attachments: [pdf]
  });
  Logger.log("Sheet:  " + ss.getUrl());
  Logger.log("Sample PDF is in the root of your Drive, and emailed to " + TO.join(", "));
}

function sampleBlob_() {
  return Utilities.newBlob(renderBriefHtml_(sampleRec_()), "text/html", "x")
    .getAs("application/pdf").setName("CVBS-brief-sample.pdf");
}

/* Renders the sample PDF to Drive without emailing. Use it while adjusting the
   layout in BriefPdf.html. */
function testRender() {
  var f = DriveApp.createFile(sampleBlob_());
  Logger.log("PREVIEW " + f.getUrl());
}

function sampleRec_() {
  return {
    ref: "CVB-260908-001", received: "8 Sep 2026 10:14",
    first: "Jane", last: "Smith", email: "jane.smith@acme.com.au",
    phone: "+61 400 000 000", company: "Acme Corporation", role: "Executive assistant / PA",
    services: "Conference venue finding, Group accommodation",
    location: "Brisbane, QLD", locationDetail: "", radius: "Within 2 to 3 hours drive",
    delegates: "120", startDate: "2027-03-15", endDate: "2027-03-17", flexibleDates: "",
    duration: "3 days", accommodation: "Yes, all delegates", venueType: "Resort",
    requirements: "Catering, AV / technology, Breakout rooms, Team activities",
    setup: "Cabaret", budgetPp: "$180", budgetTotal: "$95,000",
    notes: "We ran this in the city last year and it felt flat. Somewhere with space to walk between sessions. Two of the group use a wheelchair so step free access to every room is not negotiable.",
    offer: "", venue: "", referral: "Word of mouth / referral", source: "submit-a-brief.html"
  };
}
