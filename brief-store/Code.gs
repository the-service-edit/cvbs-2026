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
   Set LIVE to true and redeploy to hand this over to CVBS. That is the only
   change needed. Everything CVBS is on conferencevenues.com.AU. */
var LIVE        = false;
var TO          = LIVE ? ["aj@conferencevenues.com.au"]
                       : ["hello@theserviceedit.com"];
var CC          = [];
var FAIL_ALERT  = "hello@theserviceedit.com";   // told when a send fails but the brief was saved

/* The enquirer also gets their own brief back as a PDF.
   While CLIENT_LIVE is false that copy goes to FAIL_ALERT instead, so Mel sees
   exactly what a client would receive before a client ever receives it.
   Setting it true is NOT enough on its own: the copy is refused unless a Resend
   key is present, because a client who enquired at conferencevenues.com.au must
   never receive mail from theserviceedit.com. See sendClientCopy_. */
var CLIENT_LIVE = false;

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
  return /^[=+\-@]/.test(t) ? "'" + t : t;
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

/* ------------------------------------------------------------------ intake */

function doPost(e) {
  var saved = false, ref = "";
  try {
    var raw = (e && e.postData && e.postData.contents) || "";
    if (raw.length > 20000) return out_({ ok: false, error: "too large" });

    var p = JSON.parse(raw || "{}");
    if (p.key !== SHARED_KEY) return out_({ ok: false, error: "bad key" });

    /* Honeypot. A real visitor never fills this. Answer ok so the bot learns
       nothing and moves on. */
    if (str_(p.botcheck)) return out_({ ok: true, ref: "" });

    var f = p.fields || {};
    if (!str_(f.email) || !str_(f.first)) return out_({ ok: false, error: "incomplete" });

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
      source: str_(p.page), status: "new", sent: ""
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
      try {
        MailApp.sendEmail(FAIL_ALERT, "CVBS brief endpoint failed",
          "A brief was submitted and NOT saved." + NL + NL + String(err) + NL + NL +
          ((e && e.postData && e.postData.contents) || ""));
      } catch (ignore) {}
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
        from: FROM_NAME + " <" + FROM_EMAIL + ">",
        to: m.to,
        reply_to: m.replyTo,
        subject: m.subject,
        text: m.body
      };
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
    MailApp.sendEmail({
      to: m.to.join(","),
      cc: (m.cc || []).join(","),
      replyTo: m.replyTo,
      subject: m.subject,
      body: m.body,
      name: FROM_NAME,
      attachments: m.pdf ? [m.pdf] : []
    });
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
    subject: (toClient ? "" : "[CLIENT PREVIEW] ") + "Your venue brief, " + rec.ref,
    body: L.join(NL),
    pdf: pdf
  }) + (toClient ? "" : "-preview");
}

function notifyFailure_(ref, detail) {
  try {
    MailApp.sendEmail(FAIL_ALERT, "CVBS brief " + ref + " needs a look",
      detail + NL + NL + "The brief is " + ref + " in the briefs sheet. Nothing is lost.");
  } catch (ignore) {}
}

/* ------------------------------------------------------------------ render */

function renderBriefHtml_(rec) {
  var t = HtmlService.createTemplateFromFile("BriefPdf");

  var dates = rec.flexibleDates
    ? (rec.startDate ? "Flexible, around " + niceDate_(rec.startDate) : "Flexible, not yet set")
    : (niceDate_(rec.startDate) + (rec.endDate && rec.endDate !== rec.startDate ? " to " + niceDate_(rec.endDate) : ""));
  if (!str_(dates)) dates = "Not stated";
  var lead = leadTime_(rec.startDate);
  if (lead) dates = dates + '<br><span style="font-weight:normal;font-size:9pt;color:#197683">' + lead + "</span>";

  var budget = [rec.budgetPp ? rec.budgetPp + " per delegate per day" : "", rec.budgetTotal ? rec.budgetTotal + " total" : ""]
    .filter(String).join("<br>");

  t.rec       = rec;
  t.esc       = esc_;
  t.escLines  = escLines_;
  t.headline  = [
    { label: "Delegates",  value: esc_(rec.delegates) || "Not stated" },
    { label: "Location",   value: esc_(rec.locationDetail || rec.location) || "Not stated" },
    { label: "Dates",      value: esc_(dates) || "Not stated" },
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
