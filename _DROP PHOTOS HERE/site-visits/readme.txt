SITE VISIT PHOTOS GO HERE.

One folder per venue, named after the venue. "ICC Sydney", "icc-sydney" and
"icc sydney" all work. Drop the photographs straight in. Phone photos are fine.
HEIC off an iPhone is fine.

Then run, from the project folder:

    python3 scripts/site-visit-intake.py

The first run reads the visit date off the photographs themselves and writes a
notes.txt into the folder, with the shots already listed in the order they were
taken. Write one line per photograph in that file. A thirty second voice note
transcribed is fine.

Run it again and the record goes live on the venue index.

A photograph with no line against it is not published, because the line is the
part that no venue website and no competitor can publish. The photograph on its
own is just a worse version of the venue's own photography.

THE ONE RULE FOR THE NOTES: write fit, not fault. Venues pay our commission.
  Yes: "Comfortable at 200 theatre. 400 is a squeeze and the back row loses the screen."
  No:  "The room is too small and the sightlines are poor."

Also: no identifiable delegates without a release, and no other client's branded
event in frame. Location data is stripped from every published file automatically.
