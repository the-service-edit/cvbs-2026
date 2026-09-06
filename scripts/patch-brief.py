#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Teach submit-a-brief.html to accept a shortlist.

    python3 scripts/patch-brief.py

WHAT IT ADDS
    A ?venues= parameter carrying a comma separated list of venue names, sent
    by the finder's shortlist tray and by the comparison. The form fills the
    hidden Venue field, writes the list into the notes, and shows the organiser
    what it has carried through so nothing feels lost between pages.

WHY IT MATTERS MORE THAN IT LOOKS
    The single ?venue= parameter already existed, for one venue at a time. A
    shortlist is the whole point of saving four of them, and retyping four
    venue names into a text box is exactly the friction that makes somebody
    close the tab and email a hotel instead.

Idempotent.
"""
import io, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, 'submit-a-brief.html')

MARK = 'cvbs-shortlist-intake'

BLOCK = '''<script id="cvbs-shortlist-intake">
/* Carry a saved shortlist through from the venue finder.
   ?venues=Name one, Name two, Name three
   The names are already CVBS's own, so they are trusted as data but still
   stripped of angle brackets and length capped before they reach the DOM. */
(function(){
  var p=new URLSearchParams(location.search);
  var raw=p.get('venues'); if(!raw) return;
  var clean=function(v,n){return v?v.replace(/[<>]/g,'').slice(0,n||600):'';};
  var list=clean(raw).split(',').map(function(s){return s.trim();}).filter(Boolean).slice(0,12);
  if(!list.length) return;
  var el=function(id){return document.getElementById(id);};
  var dest=clean(p.get('dest'),80), guests=clean(p.get('guests'),8);

  var vf=el('venueField'); if(vf) vf.value=list.join(', ');
  var subj=document.querySelector('input[name="subject"]');
  if(subj) subj.value='Shortlist enquiry: '+list.length+' venue'+(list.length===1?'':'s');

  var n=el('notes');
  if(n&&!n.value){
    n.value='These are the venues we have shortlisted'+(dest?' in '+dest:'')+
      (guests?' for about '+guests+' people':'')+':\\n\\n'+
      list.map(function(v){return '\\u2022 '+v;}).join('\\n')+
      '\\n\\nCould you come back with availability, day delegate rates and what is included at each one?';
    n.dispatchEvent(new Event('input',{bubbles:true}));
  }

  var b=el('offerBanner');
  if(b){
    var pre=el('offerPre'),nm=el('offerName'),post=el('offerPost');
    if(pre) pre.textContent='You have shortlisted ';
    if(nm) nm.textContent=list.length+' venue'+(list.length===1?'':'s');
    if(post) post.textContent=': '+list.join(', ')+'. We will take your brief to each of them.';
    b.hidden=false; b.style.display='flex';
  }
}());
</script>
'''


def main():
    s = io.open(PAGE, encoding='utf-8').read()
    if MARK in s:
        print('submit-a-brief.html already carries the shortlist intake')
        return

    # The hero starter writes a default note. It must stand aside for a
    # shortlist exactly as it already stands aside for a single venue.
    old = "if(n&&!n.value&&!p.get('venue')&&!p.get('filters')){"
    new = "if(n&&!n.value&&!p.get('venue')&&!p.get('venues')&&!p.get('filters')){"
    if old in s:
        s = s.replace(old, new, 1)
    else:
        print('WARNING: could not find the hero note guard. Check by hand.')

    anchor = "<script>\n/* Carry a named venue through from a featured card or a venue index row */"
    if anchor not in s:
        anchor = "/* Carry a named venue through from a featured card or a venue index row */"
        if anchor not in s:
            sys.exit('Could not find the single-venue intake block to insert before.')
        s = s.replace(anchor, BLOCK + '<script>\n' + anchor, 1)
    else:
        s = s.replace(anchor, BLOCK + anchor, 1)

    io.open(PAGE, 'w', encoding='utf-8').write(s)
    print('submit-a-brief.html now accepts ?venues=')


if __name__ == '__main__':
    main()
