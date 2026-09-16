/* ==========================================================================
   CVBS Website Review - shared store
   Paste this whole file into a Google Apps Script project bound to a
   blank Google Sheet, then deploy it as a web app. Setup steps are in
   README.md in the review folder.
   ========================================================================== */

var SHEET_NAME = "feedback";
var SHARED_KEY = "cvbs-2026-review";   // must match key in config.js

/* The CVBS events calendar, read by the weekly hub.
   Karen or Anthony shares their calendar with hello@theserviceedit.com, then
   its id goes here AND in weekly/config.js as calendarId.
   A browser cannot fetch a Google Calendar feed directly because the feed
   sends no CORS headers. This script can, because it runs as the account the
   calendar is shared with. Leave it empty and the hub simply shows nothing. */
var CALENDAR_ID = "";

var COLS = ["id","project","kind","page","pageTitle","author","text","title",
            "askId","who","label","selector","relX","relY","absX","absY",
            "verdict","status","created","updated","deleted"];

function sheet_() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sh = ss.getSheetByName(SHEET_NAME);
  if (!sh) {
    sh = ss.insertSheet(SHEET_NAME);
    sh.appendRow(COLS);
    sh.setFrozenRows(1);
  }
  if (sh.getLastRow() === 0) { sh.appendRow(COLS); sh.setFrozenRows(1); }
  return sh;
}

function out_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

function rowToRec_(row) {
  var r = {};
  for (var i = 0; i < COLS.length; i++) {
    var v = row[i];
    if (COLS[i] === "deleted") v = (v === true || v === "TRUE" || v === "true");
    r[COLS[i]] = v;
  }
  return r;
}

function recToRow_(rec) {
  return COLS.map(function (c) { return rec[c] === undefined ? "" : rec[c]; });
}

function calendar_(days) {
  if (!CALENDAR_ID) return { ok: true, configured: false, events: [] };
  var cal = CalendarApp.getCalendarById(CALENDAR_ID);
  if (!cal) return { ok: false, error: "calendar not found or not shared with this account" };
  var from = new Date();
  var to = new Date(from.getTime() + (days || 60) * 864e5);
  var events = cal.getEvents(from, to).map(function (ev) {
    return {
      title: ev.getTitle(),
      start: ev.getStartTime().toISOString(),
      end: ev.getEndTime().toISOString(),
      allDay: ev.isAllDayEvent(),
      where: ev.getLocation() || "",
      notes: (ev.getDescription() || "").slice(0, 500)
    };
  });
  return { ok: true, configured: true, count: events.length, events: events };
}

function doGet(e) {
  try {
    var p = e.parameter || {};
    if (p.key !== SHARED_KEY) return out_({ ok: false, error: "bad key" });

    /* Added Sep 2026 for the weekly hub. Everything below this branch is
       exactly as it was, so the review tool is unaffected. */
    if (p.action === "calendar") {
      return out_(calendar_(parseInt(p.days, 10) || 60));
    }

    var sh = sheet_();
    var last = sh.getLastRow();
    var recs = [];
    if (last > 1) {
      var values = sh.getRange(2, 1, last - 1, COLS.length).getValues();
      for (var i = 0; i < values.length; i++) {
        if (!values[i][0]) continue;
        var rec = rowToRec_(values[i]);
        if (p.project && rec.project && rec.project !== p.project) continue;
        recs.push(rec);
      }
    }
    return out_({ ok: true, count: recs.length, records: recs });
  } catch (err) {
    return out_({ ok: false, error: String(err) });
  }
}

function doPost(e) {
  var lock = LockService.getScriptLock();
  lock.waitLock(20000);
  try {
    var body = JSON.parse(e.postData.contents);
    if (body.key !== SHARED_KEY) return out_({ ok: false, error: "bad key" });

    var sh = sheet_();
    var last = sh.getLastRow();
    var ids = {};
    if (last > 1) {
      var col = sh.getRange(2, 1, last - 1, 1).getValues();
      for (var i = 0; i < col.length; i++) { if (col[i][0]) ids[col[i][0]] = i + 2; }
    }

    var incoming = body.records || (body.record ? [body.record] : []);
    var appended = [];
    incoming.forEach(function (rec) {
      if (!rec || !rec.id) return;
      var row = recToRow_(rec);
      if (ids[rec.id]) {
        sh.getRange(ids[rec.id], 1, 1, COLS.length).setValues([row]);
      } else {
        appended.push(row);
      }
    });
    if (appended.length) {
      sh.getRange(sh.getLastRow() + 1, 1, appended.length, COLS.length).setValues(appended);
    }
    return out_({ ok: true, saved: incoming.length });
  } catch (err) {
    return out_({ ok: false, error: String(err) });
  } finally {
    lock.releaseLock();
  }
}
