# Getting the CVBS data out of Act!

Notes for the segmentation project. Written 27 Aug 2026.

Purpose: see what is actually in the Act! database before deciding anything about
email segmentation. Not a migration. Not a sync. Just a look at the data.

---

## 0. Before anything

**You cannot do this on a Mac if CVBS is on Act! Premium Desktop.** That product
is Windows only and there is no Mac version. The export has to be run by whoever
sits at the machine that holds the database, or by you over a remote desktop or
in a Windows VM.

**If CVBS is on Act! Advantage Cloud**, it runs in Chrome and you can do it from
the Mac. Confirm which one before booking anyone's time.

**Permissions.** The export tools need Manager or Administrator rights on the Act!
database, or a Standard user with export permission switched on. If the export
button is greyed out, that is usually the reason. The other cause is a missing or
incompatible Excel install on that machine.

**Ask Karen first.** This is CVBS's client list, their most valuable asset. Get an
explicit yes before a copy leaves their machine, agree where it will live, and
delete it when the diagnostic is done. Do not email it around.

---

## 1. What you are actually collecting

Act! is a relational database, not a spreadsheet. There is no single file that
holds everything. You are collecting three or four separate exports and they are
linked by contact name, not by a clean ID, which is the first thing that will
annoy you.

| Export | Where it comes from | Why you need it |
|---|---|---|
| Contacts | Contact List view | The email list itself, plus every custom field |
| Opportunities | Opportunity List view | Event value, stage, close dates |
| History | History list view | Evidence of what actually happened and when |
| Notes | Cannot be exported natively | See section 5 |

Do all of them. The contact export on its own will look thin and mislead you into
thinking there is nothing there.

---

## 2. The method you will actually use: Export Current List to Excel

This works from the Contact List, Company List, Group List, Opportunity List,
History and Task List views.

1. **Create the lookup.** Decide which records. For the first pass use every
   contact: Lookup > All Contacts. To narrow later, right-click a group or
   company and choose Create Lookup.

2. **Switch to List View.** The export only works from list views, not the
   detail view of a single record.

3. **Set up the columns before you export.** This is the step people skip and
   then repeat the whole job. Act! exports exactly the columns you can see, in
   exactly the order they appear on screen. Right-click the list and choose
   Customize Columns, then add every field you might care about. Add too many
   rather than too few. Drag the headers to reorder.

   For this project make sure you have included, if they exist at all: city or
   state, contact type or category, ID/Status, any user-defined fields, Create
   Date, Edit Date, Last Reach or Last Attempt, and the email address field.

4. **Click Export Current List to Excel.** It is an icon in the toolbar at the
   top of the view. Save it somewhere sensible, dated.

5. **Repeat for the Opportunity List and the History list.** Same pattern, same
   column customisation step.

---

## 3. The older wizard: File > Export

Menu paths move between Act! versions, so check what is actually on screen. It is
either **File > Export** or **File > Data Exchange > Export**.

The wizard produces a text or comma delimited file and lets you pick record type
(Contacts, Companies or Groups) and choose fields one by one. It is more precise
than the Excel button and better if you want a repeatable field list.

It still does not export notes or activities.

---

## 4. The full database backup

**File > Back Up > Database.** This produces a single .zip containing the .adf
and .alf database files.

Understand what this is and is not. It is a restore file for Act!, not something
you can open and read. Excel will not touch it. It is the right thing to hand a
migration specialist, and the right thing to have sitting safely before anyone
changes fields in the database. It is the wrong thing if what you want is to look
at the data.

Take one anyway before any field restructuring work starts.

**On Act! Premium Cloud** you generally cannot pull the backup yourself. You have
to request the database backup from Act! support. Allow days, not hours, and
start that request early if it turns out to be the path.

---

## 5. The notes problem

Act! has no native export for Notes. This is well documented and it is the single
biggest gap in any Act! extraction.

It matters here because in a database that has been running for years, the
information worth segmenting on is usually sitting in free text notes. "Ran their
national conference at Doltone, about 90 people, October." That sentence is the
segmentation gold and Act! will not give it to you in a column.

Options, in the order I would try them:

1. **Check first whether it is even there.** Open twenty contact records at
   random and read the Notes and History tabs. If they are empty or thin, the
   whole notes question disappears and you have a much simpler project.
2. **History list view export.** History is exportable even though Notes is not,
   and in many databases the useful record lives in History rather than Notes.
   Try this before paying anyone.
3. **Third party extraction.** Tools and consultants exist that read the Act!
   tables directly and produce a CSV per table. Only worth it if step 1 shows
   the notes are rich and step 2 does not reach them.

---

## 6. What to do with the exports

Do not start building segments. Answer four questions first.

1. **How many contacts are there really**, after removing duplicates and records
   with no email address?
2. **What percentage have a usable email address?** Expect worse than you hope.
3. **Which fields are actually populated?** Sort each column and count the blanks.
   A field that is 20% filled cannot drive a segment.
4. **How recent is the activity?** Use Create Date and Edit Date. Contacts
   untouched since 2019 are a reengagement problem, not a segment.

The honest outcome of this exercise might be that the Act! data cannot support
segmentation yet. That is a useful answer. It redirects effort to Mailchimp click
behaviour and the submit-a-brief form, which are clean, current and already
structured, while the Act! field discipline gets fixed over months.

---

## 7. Before importing anything into Mailchimp

Do not bulk load the export. A decade of cold records hitting Mailchimp at once
will damage the sending reputation of conferencevenues.com.au, which is the same
domain Karen's client correspondence relies on, and consent under the Spam Act
has to be defensible for every address.

Import in waves. Warmest and most recent first. Treat anything untouched for over
two years as a separate reengagement campaign and expect it to perform badly.

---

## Version note

Act! menu paths and toolbar icons differ across versions and between Desktop and
Cloud. The list view export and the backup exist in every recent version, but
confirm the exact wording on screen rather than assuming these paths are literal.
