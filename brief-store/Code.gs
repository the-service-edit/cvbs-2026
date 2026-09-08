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

/* Who receives the brief. */
var TO          = ["karen@conferencevenues.com", "aj@conferencevenues.com"];
var CC          = [];
var FAIL_ALERT  = "hello@theserviceedit.com";     // told when the send fails but the brief was saved

/* From address. Only used when a Resend API key is present in Script
   Properties. Without one the script falls back to MailApp, which sends from
   the Google account that owns this script. See README.md. */
var FROM_NAME   = "Conference Venues website";
var FROM_EMAIL  = "briefs@mail.conferencevenues.com";

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

function sheet_() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sh = ss.getSheetByName(SHEET_NAME);
  if (!sh) { sh = ss.insertSheet(SHEET_NAME); }
  if (sh.getLastRow() === 0) { sh.appendRow(COLS); sh.setFrozenRows(1); }
  return sh;
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

    sh.appendRow(COLS.map(function (c) { return rec[c] === undefined ? "" : rec[c]; }));
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
          "A brief was submitted and NOT saved.\n\n" + String(err) + "\n\n" +
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

function sendBrief_(rec) {
  var pdf, subject, body;
  try {
    pdf = Utilities.newBlob(renderBriefHtml_(rec), "text/html", "x")
            .getAs("application/pdf")
            .setName("CVBS-brief-" + rec.ref + "-" + (rec.company || rec.last).replace(/[^A-Za-z0-9]+/g, "-") + ".pdf");
  } catch (err) {
    pdf = null;
  }

  subject = "New brief " + rec.ref + ": " + (rec.company || (rec.first + " " + rec.last)) +
            ", " + (rec.delegates || "?") + " delegates, " + (rec.location || "location TBC");

  body =
    "A new brief came in through the website. The full brief is attached as a PDF.\n\n" +
    "Reference   " + rec.ref + "\n" +
    "Received    " + rec.received + " AEST\n" +
    "From        " + rec.first + " " + rec.last + ", " + rec.company + "\n" +
    "Email       " + rec.email + "\n" +
    (rec.phone ? "Phone       " + rec.phone + "\n" : "") +
    "Delegates   " + rec.delegates + "\n" +
    "Location    " + rec.location + (rec.locationDetail ? " (" + rec.locationDetail + ")" : "") + "\n" +
    "Dates       " + (rec.flexibleDates ? "Flexible. " : "") + niceDate_(rec.startDate) +
      (rec.endDate ? " to " + niceDate_(rec.endDate) : "") + "\n\n" +
    (rec.notes ? "In their words:\n" + rec.notes + "\n\n" : "") +
    "Reply to this email and it goes straight to " + rec.email + ".\n" +
    (pdf ? "" : "\nThe PDF could not be rendered this time. Every field is in the sheet.\n");

  var attachments = pdf ? [pdf] : [];

  var apiKey = PropertiesService.getScriptProperties().getProperty("RESEND_API_KEY");
  if (apiKey) {
    try {
      var payload = {
        from: FROM_NAME + " <" + FROM_EMAIL + ">",
        to: TO,
        reply_to: rec.email,
        subject: subject,
        text: body
      };
      if (CC.length) payload.cc = CC;
      if (pdf) {
        payload.attachments = [{
          filename: pdf.getName(),
          content: Utilities.base64Encode(pdf.getBytes())
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
      notifyFailure_(rec, "Resend returned " + res.getResponseCode() + ": " + res.getContentText());
    } catch (err) {
      notifyFailure_(rec, "Resend threw: " + String(err));
    }
  }

  /* Fallback. Sends from the Google account that owns this script, which is
     the wrong from address but a delivered brief beats a tidy one. */
  try {
    MailApp.sendEmail({
      to: TO.join(","),
      cc: CC.join(","),
      replyTo: rec.email,
      subject: subject,
      body: body,
      name: FROM_NAME,
      attachments: attachments
    });
    return apiKey ? "mailapp-fallback" : "mailapp";
  } catch (err) {
    notifyFailure_(rec, "MailApp threw: " + String(err));
    return "FAILED";
  }
}

function notifyFailure_(rec, detail) {
  try {
    MailApp.sendEmail(FAIL_ALERT, "CVBS brief " + rec.ref + " saved but not emailed",
      detail + "\n\nThe brief is row " + rec.ref + " in the briefs sheet. Nothing is lost.");
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

/* Run this once from the editor to authorise the project and to see the PDF
   before the form is live. It saves nothing to the sheet. */
function testRender() {
  var rec = {
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
  var pdf = Utilities.newBlob(renderBriefHtml_(rec), "text/html", "x").getAs("application/pdf")
              .setName("CVBS-brief-sample.pdf");
  DriveApp.createFile(pdf);
  Logger.log("Sample written to the root of your Google Drive.");
}
