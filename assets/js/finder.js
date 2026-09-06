/* CVBS venue finder, shortlist and comparison. Vanilla, no dependencies.
   ==========================================================================
   Loaded on venue-results.html and the venue pages.

   THE RULE THIS FILE IS BUILT AROUND
   It never invents a number. Every figure printed here comes out of the data
   island, which comes out of assets/data/venues.json, which comes out of the
   venue's own published material. Where a venue publishes nothing the page
   says so in words rather than leaving a blank or guessing a range.

   The shortlist lives in localStorage, not in an account, because asking an
   organiser to register before they can save three venues is the fastest way
   to lose them. It carries venue ids only, so it survives a data rebuild.
   ========================================================================== */
(function () {
  'use strict';

  var LSKEY = 'cvbs.shortlist.v1';
  var MAXCMP = 4;

  /* ---------------------------------------------------------- shortlist */
  function readList() {
    try {
      var raw = window.localStorage.getItem(LSKEY);
      var a = raw ? JSON.parse(raw) : [];
      return Object.prototype.toString.call(a) === '[object Array]' ? a : [];
    } catch (e) { return []; }
  }
  function writeList(a) {
    try { window.localStorage.setItem(LSKEY, JSON.stringify(a.slice(0, 24))); }
    catch (e) { /* private mode, or storage off. The page still works. */ }
  }
  var SL = readList();
  function saved(id) { return SL.indexOf(id) !== -1; }
  function toggleSaved(id) {
    var i = SL.indexOf(id);
    if (i === -1) { SL.push(id); } else { SL.splice(i, 1); }
    writeList(SL);
    paintPips();
    return i === -1;
  }

  function paintPips() {
    var pips = document.querySelectorAll('[data-vf-pip]');
    for (var i = 0; i < pips.length; i++) {
      var p = pips[i];
      if (SL.length > 0) { p.className = p.className.replace(/\s*\bon\b/, '') + ' on'; }
      else { p.className = p.className.replace(/\s*\bon\b/, ''); }
      var b = p.querySelector('b');
      if (b) b.textContent = SL.length;
      var href = p.getAttribute('data-vf-pip');
      if (href && p.tagName === 'A') p.setAttribute('href', href);
    }
  }

  /* ------------------------------------------------------------ helpers */
  function num(n) {
    return n === null || n === undefined ? null
      : String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
  }
  function esc(s) {
    return String(s === null || s === undefined ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;')
      .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }
  function el(tag, cls, html) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (html !== undefined) n.innerHTML = html;
    return n;
  }
  function qs(name, d) {
    var m = new RegExp('[?&]' + name + '=([^&]*)').exec(window.location.search);
    return m ? decodeURIComponent(m[1].replace(/\+/g, ' ')) : (d === undefined ? '' : d);
  }

  /* What the organiser is planning, mapped to the room layout that decides
     whether the venue works. A gala dinner is a banquet number, not a theatre
     number, and getting that wrong is the most common way a shortlist wastes
     somebody's week. "Not sure yet" deliberately uses the venue's largest
     published capacity in any layout, and the card says so. */
  var TYPE_SETUP = {
    'Conference or seminar': 'th',
    'Meeting or board session': 'bd',
    'Gala dinner or awards night': 'bq',
    'Cocktail function or launch': 'ck',
    'Training or workshop': 'cl',
    'Not sure yet': 'max'
  };
  var SETUP_WORD = {
    th: 'theatre', bq: 'banquet', cl: 'classroom', ck: 'cocktail',
    cab: 'cabaret', ush: 'u-shape', bd: 'boardroom',
    max: 'its largest published layout'
  };
  var TYPE_LABEL = {
    conv: 'Convention centre', hotel: 'Hotel',
    event: 'Event venue', resort: 'Resort'
  };

  function capOf(v, setup) {
    if (setup === 'max' || !setup) {
      return v.maxcap === undefined ? null : v.maxcap;
    }
    return v[setup] === undefined ? null : v[setup];
  }

  var HEART = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20.8 6.6a5 5 0 0 0-7.1 0L12 8.3l-1.7-1.7a5 5 0 1 0-7.1 7.1l8.8 8.8 8.8-8.8a5 5 0 0 0 0-7.1z"/></svg>';

  /* ================================================================ main */
  var island = document.getElementById('vf-data');
  var root = document.getElementById('vf-results');

  /* The pip and the on-page save buttons work on every page that loads this
     file, including the venue pages, which carry no dataset and no results
     list. Everything below therefore has to survive both of those being
     absent: an early return here would have registered no click handler, and
     the save button on a venue page would have looked live and done nothing. */
  paintPips();
  bindOnPageSaves();

  var DATA = null, VENUES = [], BY = {};
  if (island) {
    try { DATA = JSON.parse(island.textContent); } catch (e) { DATA = null; }
  }
  if (DATA && DATA.venues && DATA.venues.length) {
    VENUES = DATA.venues;
    for (var bi = 0; bi < VENUES.length; bi++) { BY[VENUES[bi].id] = VENUES[bi]; }
  }
  var LIVE = !!(root && VENUES.length);

  /* Pages that carry a shortlist tray or a save button but no results list,
     the venue pages and the accommodation page, still need venue names to put
     in the tray and in the handover link. Rather than repeat a 37KB island on
     every one of them, they fetch the dataset once. The path is derived from
     this script's own src so it works from the site root and from a venue page
     two directories down. If the fetch fails, the tray still shows the count
     and the handover still works, it just carries no names. */
  function dataUrl() {
    var ss = document.getElementsByTagName('script');
    for (var i = 0; i < ss.length; i++) {
      var s = ss[i].getAttribute('src') || '';
      var k = s.indexOf('assets/js/finder.js');
      if (k !== -1) { return s.slice(0, k) + 'assets/data/venues.json'; }
    }
    return 'assets/data/venues.json';
  }

  var CMP = [];

  /* Forty two cards is not a shortlist, it is a directory. The closest fit
     sort puts the right sized rooms first, so the first dozen is almost always
     the useful part. The rest stays one click away rather than gone. */
  var PAGE = 12;
  var showAll = false;

  var f = {
    dest: document.getElementById('vf-dest'),
    guests: document.getElementById('vf-guests'),
    type: document.getElementById('vf-type'),
    accom: document.getElementById('vf-accom'),
    prec: document.getElementById('vf-prec'),
    vt: document.getElementById('vf-vt'),
    seen: document.getElementById('vf-seen'),
    sort: document.getElementById('vf-sort')
  };
  var countEl = document.getElementById('vf-count');
  var chipsEl = document.getElementById('vf-chips');
  var refineBtn = document.getElementById('vf-refine-toggle');
  var refinePanel = document.getElementById('vf-refine-panel');

  /* --------------------------------------------------- populate selects */
  (function fillDest() {
    if (!f.dest || !VENUES.length) { return; }
    var cities = {};
    for (var i = 0; i < VENUES.length; i++) {
      cities[VENUES[i].city] = (cities[VENUES[i].city] || 0) + 1;
    }
    var names = Object.keys(cities).sort();
    for (var j = 0; j < names.length; j++) {
      var o = document.createElement('option');
      o.value = names[j];
      o.textContent = names[j] + ' (' + cities[names[j]] + ')';
      f.dest.appendChild(o);
    }
  }());

  function fillPrecincts() {
    if (!f.prec) { return; }
    var city = f.dest ? f.dest.value : '';
    var keep = f.prec.value;
    var seen = {}, out = [];
    for (var i = 0; i < VENUES.length; i++) {
      var v = VENUES[i];
      if (city && v.city !== city) { continue; }
      if (!seen[v.pr]) { seen[v.pr] = 1; out.push(v.pr); }
    }
    out.sort();
    f.prec.innerHTML = '<option value="">Anywhere in the destination</option>';
    for (var k = 0; k < out.length; k++) {
      var op = document.createElement('option');
      op.value = out[k];
      op.textContent = out[k];
      f.prec.appendChild(op);
    }
    if (out.indexOf(keep) !== -1) { f.prec.value = keep; }
  }

  /* venue-results.html?view=saved shows only what the visitor has kept. It is
     the shortlist review screen, and it exists because a venue page and the
     accommodation page can add to a shortlist with nowhere to go and look at
     it. Deliberately a mode of the results page rather than a page of its own:
     an empty extra URL in the sitemap helps nobody. */
  var VIEW = qs('view');

  /* ------------------------------------------------ state from the URL */
  function preset() {
    if (f.dest && qs('dest')) { f.dest.value = qs('dest'); }
    fillPrecincts();
    if (f.guests && qs('guests')) { f.guests.value = qs('guests'); }
    if (f.type && qs('type')) { f.type.value = qs('type'); }
    if (f.accom && qs('accom')) { f.accom.value = qs('accom'); }
    if (f.prec && qs('prec')) { f.prec.value = qs('prec'); }
    if (f.vt && qs('vt')) { f.vt.value = qs('vt'); }
    if (f.seen && qs('seen')) { f.seen.value = qs('seen'); }
    if (f.sort && qs('sort')) { f.sort.value = qs('sort'); }
  }

  function stateUrl() {
    var p = [];
    function add(k, v) { if (v) { p.push(k + '=' + encodeURIComponent(v)); } }
    add('dest', f.dest && f.dest.value);
    add('guests', f.guests && f.guests.value);
    add('type', f.type && f.type.value);
    add('accom', f.accom && f.accom.value);
    add('prec', f.prec && f.prec.value);
    add('vt', f.vt && f.vt.value);
    add('seen', f.seen && f.seen.value);
    add('sort', f.sort && f.sort.value);
    return window.location.pathname + (p.length ? '?' + p.join('&') : '');
  }

  /* ------------------------------------------------------------ the fit */
  function fitLine(v, n, setup) {
    var word = SETUP_WORD[setup] || 'theatre';
    var c = capOf(v, setup);
    if (c === null) {
      return ['none', 'The venue doesn’t publish a ' + word +
        ' figure. We can ask them for it.'];
    }
    var head = setup === 'max'
      ? 'Holds <b>' + num(c) + '</b> at its largest published layout'
      : 'Seats <b>' + num(c) + '</b> ' + word;
    if (setup === 'ck') {
      head = 'Takes <b>' + num(c) + '</b> for a cocktail reception';
    }
    if (!n) { return ['ok', head + '.']; }
    if (c < n) { return ['no', '']; }
    if (c >= n * 1.2) {
      return ['ok', head + ', so ' + num(n) + ' sits comfortably in the one room.'];
    }
    if (c >= n * 1.05) {
      return ['ok', head + ', so ' + num(n) + ' fits with a little room to move.'];
    }
    return ['tight', head + ', so ' + num(n) +
      ' fits, but only just. Worth looking at the floor plan before you commit.'];
  }

  /* ------------------------------------------------------------ render */
  function render(push) {
    var city = f.dest ? f.dest.value : '';
    var n = f.guests && f.guests.value ? parseInt(f.guests.value, 10) : 0;
    if (isNaN(n) || n < 0) { n = 0; }
    var typeVal = f.type ? f.type.value : '';
    var setup = TYPE_SETUP[typeVal] || 'max';
    var accom = f.accom ? f.accom.value : '';
    var prec = f.prec ? f.prec.value : '';
    var vt = f.vt ? f.vt.value : '';
    var seenF = f.seen ? f.seen.value : '';
    var sort = f.sort ? f.sort.value : 'fit';

    var matched = [], unpublished = [], tooSmall = 0;

    if (VIEW === 'saved') {
      for (var si = 0; si < SL.length; si++) {
        if (BY[SL[si]]) { matched.push(BY[SL[si]]); }
      }
      renderSaved(matched, n, setup);
      return;
    }

    for (var i = 0; i < VENUES.length; i++) {
      var v = VENUES[i];
      if (city && v.city !== city) { continue; }
      if (prec && v.pr !== prec) { continue; }
      if (vt && v.ty !== vt) { continue; }
      if (accom === 'yes' && !v.gr) { continue; }
      if (accom === 'no' && v.gr) { continue; }
      if (seenF === 'seen' && !v.visit) { continue; }
      if (seenF === 'worked' && !v.worked) { continue; }
      var c = capOf(v, setup);
      if (c === null) { unpublished.push(v); continue; }
      if (n && c < n) { tooSmall++; continue; }
      matched.push(v);
    }

    /* Default order puts the smallest room that still works at the top. A
       planner for 250 does not want a 7,000 seat hall first, and sorting on
       size alone is exactly what the marketplaces get wrong. */
    matched.sort(function (a, b) {
      var ca = capOf(a, setup), cb = capOf(b, setup);
      if (sort === 'largest') { return (cb || 0) - (ca || 0); }
      if (sort === 'rooms') { return (b.gr || 0) - (a.gr || 0); }
      if (sort === 'name') { return a.n.localeCompare(b.n); }
      if (n) {
        if (ca !== cb) { return ca - cb; }
      } else if (ca !== cb) {
        return cb - ca;
      }
      return a.n.localeCompare(b.n);
    });
    unpublished.sort(function (a, b) { return a.n.localeCompare(b.n); });

    var layoutWord = setup === 'max' ? 'in one room' : SETUP_WORD[setup];

    if (countEl) {
      var where = city ? ' in ' + esc(city) : ' across the venues we publish';
      if (!matched.length && !unpublished.length) {
        countEl.innerHTML = 'Nothing here matches that yet.';
      } else if (n) {
        countEl.innerHTML = '<b>' + matched.length + '</b> ' +
          (matched.length === 1 ? 'venue' : 'venues') + where +
          ' can take ' + num(n) + ' ' + layoutWord + '.';
      } else {
        countEl.innerHTML = '<b>' + matched.length + '</b> ' +
          (matched.length === 1 ? 'venue' : 'venues') + where + '.';
      }
    }

    if (chipsEl) {
      chipsEl.innerHTML = '';
      var chips = [];
      if (city) { chips.push(['dest', city]); }
      if (n) { chips.push(['guests', num(n) + ' people']); }
      if (typeVal) { chips.push(['type', typeVal]); }
      if (accom === 'yes') { chips.push(['accom', 'With accommodation']); }
      if (accom === 'no') { chips.push(['accom', 'No accommodation needed']); }
      if (prec) { chips.push(['prec', prec]); }
      if (vt) { chips.push(['vt', TYPE_LABEL[vt] || vt]); }
      if (seenF === 'seen') { chips.push(['seen', 'We have walked through it']); }
      if (seenF === 'worked') { chips.push(['seen', 'We have booked it before']); }
      for (var q = 0; q < chips.length; q++) {
        var cb2 = el('button', 'vf-chip',
          esc(chips[q][1]) + ' <span aria-hidden="true">&times;</span>');
        cb2.type = 'button';
        cb2.setAttribute('data-clear', chips[q][0]);
        cb2.setAttribute('aria-label', 'Remove filter, ' + chips[q][1]);
        chipsEl.appendChild(cb2);
      }
    }

    root.innerHTML = '';
    if (!matched.length) {
      var why = n
        ? 'Nothing we publish' + (city ? ' in ' + esc(city) : '') +
          ' has a room that takes ' + num(n) + ' ' + layoutWord + '.'
        : 'Nothing matches those filters yet.';
      var extra = tooSmall
        ? ' ' + tooSmall + ' ' + (tooSmall === 1 ? 'venue is' : 'venues are') +
          ' too small for that number.'
        : '';
      root.appendChild(el('div', 'vf-empty',
        '<h3>We haven’t published one that fits.</h3><p>' + why + extra +
        ' What we publish is a fraction of what we book, so this is a good moment ' +
        'to tell us what you’re planning and let us go looking.</p>' +
        '<a class="btn btn--teal" href="' + briefHref([]) +
        '">Tell us about your event</a>'));
    } else {
      var limited = !showAll && matched.length > PAGE;
      var shown = limited ? PAGE : matched.length;
      var ul = el('ul', 'vf-list');
      for (var m = 0; m < shown; m++) {
        ul.appendChild(card(matched[m], n, setup));
      }
      root.appendChild(ul);
      if (limited) {
        var rest = matched.length - PAGE;
        var more = el('button', 'btn btn--ghost vf-more',
          'Show the other ' + rest + ' ' + (rest === 1 ? 'venue' : 'venues'));
        more.type = 'button';
        more.setAttribute('data-showall', '1');
        root.appendChild(more);
        root.appendChild(el('p', 'vf-showing',
          'Showing the ' + PAGE + ' closest to ' +
          (n ? num(n) + ' ' + layoutWord : 'your brief') + ' first.'));
      }
    }

    if (unpublished.length) {
      var names = unpublished.map(function (v) {
        return '<li>' + esc(v.n) + '</li>';
      }).join('');
      var gapWord = setup === 'max' ? 'capacity' : SETUP_WORD[setup];
      root.appendChild(el('div', 'vf-nodata',
        '<h4>' + unpublished.length + ' more we hold, where the venue publishes no ' +
        esc(gapWord) + ' figure</h4><p>We would rather show you the gap than fill it ' +
        'in with a guess. If one of these is on your list, ask us and we’ll get ' +
        'the number from the venue.</p><ul>' + names + '</ul>'));
    }

    paintTray();
    if (push && window.history && window.history.replaceState) {
      window.history.replaceState(null, '', stateUrl());
    }
  }

  function renderSaved(list, n, setup) {
    if (chipsEl) { chipsEl.innerHTML = ''; }
    if (countEl) {
      countEl.innerHTML = list.length
        ? '<b>' + list.length + '</b> ' + (list.length === 1 ? 'venue' : 'venues') +
          ' on your shortlist. Send them to us together and we will come back on all of them at once.'
        : 'Nothing on your shortlist yet.';
    }
    root.innerHTML = '';
    if (!list.length) {
      root.appendChild(el('div', 'vf-empty',
        '<h3>Nothing saved yet.</h3><p>Save a venue anywhere on the site and it will be waiting ' +
        'here. Nothing is sent to us until you decide to send it, and there is no account to make.</p>' +
        '<a class="btn btn--teal" href="venue-results.html">Look at the venues we publish</a>'));
    } else {
      var ul = el('ul', 'vf-list');
      for (var i = 0; i < list.length; i++) { ul.appendChild(card(list[i], n, setup)); }
      root.appendChild(ul);
      root.appendChild(el('p', 'vf-showing',
        '<a href="venue-results.html">Back to everything we publish</a>'));
    }
    paintTray();
  }

  function card(v, n, setup) {
    var li = el('li');
    var hasImg = !!v.photo;
    var c = el('article', 'vf-card' + (hasImg ? '' : ' vf-card--noimg'));
    c.setAttribute('data-id', v.id);

    if (hasImg) {
      c.appendChild(el('div', 'vf-card__img',
        '<img src="' + esc(v.photo) + '" alt="' + esc(v.n) +
        ', photographed by CVBS" loading="lazy" decoding="async" width="420" height="280">'));
    }

    var fit = fitLine(v, n, setup);
    var facts = [];
    if (v.sp) { facts.push('<div>Largest space<b>' + esc(v.sp) + '</b></div>'); }
    if (v.br) { facts.push('<div>Event rooms<b>' + v.br + '</b></div>'); }
    if (v.gr) { facts.push('<div>Guest rooms<b>' + num(v.gr) + '</b></div>'); }
    if (v.area) { facts.push('<div>Floor area<b>' + num(v.area) + ' sqm</b></div>'); }
    if (v.ceil && !v.ceilq) { facts.push('<div>Ceiling<b>' + v.ceil + ' m</b></div>'); }

    var tags = [];
    if (v.visit) { tags.push('<span class="vf-tag vf-tag--seen">Inspected by CVBS</span>'); }
    if (v.worked) { tags.push('<span class="vf-tag vf-tag--worked">We have booked it</span>'); }
    if (v.offer) { tags.push('<span class="vf-tag vf-tag--offer">Current offer</span>'); }
    if (v.gr) { tags.push('<span class="vf-tag vf-tag--accom">Rooms on site</span>'); }

    var name = v.visit
      ? '<a href="venue-visits/' + esc(v.visit) + '/">' + esc(v.n) + '</a>'
      : esc(v.n);

    var fitCls = fit[0] === 'tight' ? ' vf-fit--tight'
      : (fit[0] === 'none' ? ' vf-fit--none' : '');

    c.appendChild(el('div', 'vf-card__body',
      '<h3 class="vf-card__n">' + name + '</h3>' +
      '<p class="vf-card__loc">' + esc(v.pr) + ', ' + esc(v.city) +
      ' &middot; ' + esc(TYPE_LABEL[v.ty] || '') + '</p>' +
      '<p class="vf-fit' + fitCls + '">' + fit[1] + '</p>' +
      (v.note ? '<p class="vf-card__note">' + esc(v.note) + '</p>' : '') +
      (facts.length ? '<div class="vf-facts">' + facts.join('') + '</div>' : '') +
      (tags.length ? '<div class="vf-tags">' + tags.join('') + '</div>' : '')));

    var acts = el('div', 'vf-card__acts');
    var sv = el('button', 'vf-save',
      HEART + '<span>' + (saved(v.id) ? 'Saved' : 'Save') + '</span>');
    sv.type = 'button';
    sv.setAttribute('data-save', v.id);
    sv.setAttribute('aria-pressed', saved(v.id) ? 'true' : 'false');
    sv.setAttribute('aria-label',
      (saved(v.id) ? 'Remove ' : 'Save ') + v.n + ' to your shortlist');
    acts.appendChild(sv);

    if (v.visit) {
      var a = el('a', 'btn btn--ghost');
      a.setAttribute('href', 'venue-visits/' + v.visit + '/');
      a.textContent = 'What it’s like';
      acts.appendChild(a);
    }

    var lbl = el('label', 'vf-cmp',
      '<input type="checkbox" data-cmp="' + esc(v.id) + '"' +
      (CMP.indexOf(v.id) !== -1 ? ' checked' : '') + '> Compare');
    acts.appendChild(lbl);

    if (v.src) {
      acts.appendChild(el('p', 'vf-src',
        'Figures from <a href="' + esc(v.src) +
        '" rel="nofollow noopener" target="_blank">the venue’s own material</a>'));
    }
    c.appendChild(acts);
    li.appendChild(c);
    return li;
  }

  /* -------------------------------------------------------------- tray */
  function briefHref(ids) {
    var p = [];
    if (f.dest && f.dest.value) { p.push('dest=' + encodeURIComponent(f.dest.value)); }
    if (f.guests && f.guests.value) { p.push('guests=' + encodeURIComponent(f.guests.value)); }
    if (f.type && f.type.value) { p.push('type=' + encodeURIComponent(f.type.value)); }
    var src = (ids && ids.length) ? ids : SL;
    var names = [];
    for (var i = 0; i < src.length; i++) {
      if (BY[src[i]]) { names.push(BY[src[i]].n); }
    }
    if (names.length) { p.push('venues=' + encodeURIComponent(names.join(', '))); }
    return 'submit-a-brief.html' + (p.length ? '?' + p.join('&') : '');
  }

  var tray = document.getElementById('vf-tray');
  function paintTray() {
    if (!tray) { return; }
    var on = SL.length > 0 || CMP.length > 1;
    tray.className = 'vf-tray' + (on ? ' on' : '');
    document.body.className = document.body.className.replace(/\s*\bhas-tray\b/, '') +
      (on ? ' has-tray' : '');
    var nEl = tray.querySelector('[data-tray-n]');
    var namesEl = tray.querySelector('[data-tray-names]');
    var send = tray.querySelector('[data-tray-send]');
    var cmpBtn = tray.querySelector('[data-tray-compare]');
    if (nEl) {
      nEl.innerHTML = SL.length
        ? '<b>' + SL.length + '</b> ' + (SL.length === 1 ? 'venue' : 'venues') +
          ' on your shortlist'
        : '<b>' + CMP.length + '</b> selected to compare';
    }
    if (namesEl) {
      var list = SL.length ? SL : CMP, out = [];
      for (var i = 0; i < list.length; i++) {
        if (BY[list[i]]) { out.push(BY[list[i]].n); }
      }
      namesEl.textContent = out.join(', ');
    }
    if (send) { send.setAttribute('href', briefHref([])); }
    if (cmpBtn) {
      cmpBtn.hidden = CMP.length < 2;
      cmpBtn.textContent = 'Compare these ' + CMP.length;
    }
  }

  /* ---------------------------------------------------------- compare */
  var modal = document.getElementById('vf-compare');
  var lastFocus = null;

  var CMP_ROWS = [
    ['Where', 'city'], ['Venue type', 'ty'], ['Largest space', 'sp'],
    ['Theatre', 'th'], ['Banquet', 'bq'], ['Cocktail', 'ck'],
    ['Classroom', 'cl'], ['Cabaret', 'cab'], ['Boardroom', 'bd'],
    ['Floor area', 'area'], ['Ceiling height', 'ceil'],
    ['Second space', 'second'], ['Event rooms', 'br'], ['Guest rooms', 'gr'],
    ['We have walked it', 'seen']
  ];
  /* "Not published" is the right words for a figure the venue has never put
     out. It is the wrong words for our own visits, which is why the seen row
     gets its own answer and only appears when at least one of the venues in
     the comparison has a page. */
  var CMP_ALWAYS = ['city', 'ty', 'sp', 'seen'];
  var CMP_NUMERIC = ['th', 'bq', 'ck', 'cl', 'cab', 'bd', 'area', 'br', 'gr'];

  function rowVal(v, key) {
    switch (key) {
    case 'city': return esc(v.pr) + ', ' + esc(v.city);
    case 'ty': return esc(TYPE_LABEL[v.ty] || '');
    case 'sp': return esc(v.sp || '');
    case 'area': return v.area ? num(v.area) + ' sqm' : null;
    case 'ceil': return v.ceil ? v.ceil + ' m' + (v.ceilq ? ' *' : '') : null;
    case 'br': return v.br ? String(v.br) : null;
    case 'gr': return v.gr ? num(v.gr) : null;
    case 'second': return v.s_name
      ? esc(v.s_name) + (v.s_th ? ', ' + num(v.s_th) + ' theatre' : '') : null;
    case 'seen': return v.visit
      ? '<a href="venue-visits/' + esc(v.visit) + '/">Yes, see the page</a>'
      : 'Not yet';
    default: return v[key] ? num(v[key]) : null;
    }
  }

  function openCompare() {
    if (!modal || CMP.length < 2) { return; }
    var vs = [];
    for (var z = 0; z < CMP.length; z++) { if (BY[CMP[z]]) { vs.push(BY[CMP[z]]); } }
    var body = modal.querySelector('[data-cmp-body]');
    var grid = el('div', 'vf-cmp-grid');

    /* Best-in-row is marked only on the numeric rows, and only where the
       venues actually differ. Marking a winner on every row would imply a
       ranking CVBS is not making. */
    var best = {};
    for (var r = 0; r < CMP_ROWS.length; r++) {
      var key = CMP_ROWS[r][1];
      if (CMP_NUMERIC.indexOf(key) === -1) { continue; }
      var mx = 0, same = 0;
      for (var s = 0; s < vs.length; s++) { mx = Math.max(mx, vs[s][key] || 0); }
      for (var s2 = 0; s2 < vs.length; s2++) {
        if ((vs[s2][key] || 0) === mx) { same++; }
      }
      if (mx > 0 && same < vs.length) { best[key] = mx; }
    }

    /* A row where none of the venues publishes anything tells the organiser
       nothing and makes the table longer. Drop it. */
    var liveRows = [];
    for (var rr = 0; rr < CMP_ROWS.length; rr++) {
      var kk = CMP_ROWS[rr][1];
      if (CMP_ALWAYS.indexOf(kk) !== -1) { liveRows.push(CMP_ROWS[rr]); continue; }
      for (var vv = 0; vv < vs.length; vv++) {
        if (rowVal(vs[vv], kk)) { liveRows.push(CMP_ROWS[rr]); break; }
      }
    }

    for (var i = 0; i < vs.length; i++) {
      var v = vs[i], rows = '';
      for (var j = 0; j < liveRows.length; j++) {
        var label = liveRows[j][0], k = liveRows[j][1];
        var val = rowVal(v, k);
        var isBest = best[k] && v[k] === best[k];
        rows += '<div class="r"><dt>' + label + '</dt><dd class="' +
          (val ? (isBest ? 'best' : '') : 'na') + '">' +
          (val || 'Not published') + '</dd></div>';
      }
      var foot = '<a class="btn btn--teal" href="' + briefHref([v.id]) +
        '">Ask us about this one</a>';
      if (v.visit) {
        foot += '<a class="btn btn--ghost" href="venue-visits/' + esc(v.visit) +
          '/">What it’s like</a>';
      }
      grid.appendChild(el('div', 'vf-cmp-col',
        '<h3>' + esc(v.n) + '</h3><p class="loc">' + esc(v.pr) + '</p><dl>' +
        rows + '</dl><div class="foot">' + foot + '</div>'));
    }
    body.innerHTML = '';
    body.appendChild(grid);
    body.appendChild(el('p', 'vf-cmp-note',
      'Every figure here is the one the venue publishes for that room, read from its ' +
      'own capacity chart or fact sheet. “Not published” means the venue has ' +
      'not put a number out, not that the room cannot do it. An asterisk on a ceiling ' +
      'height means the venue qualifies the number, usually because it is measured at a ' +
      'high point rather than across the room. What none of this tells you is how the day ' +
      'actually runs in each building, and that is the part worth a conversation.'));

    var send = modal.querySelector('[data-cmp-send]');
    if (send) { send.setAttribute('href', briefHref(CMP)); }

    lastFocus = document.activeElement;
    modal.className = 'vf-modal on';
    if (tray) { tray.setAttribute('aria-hidden', 'true'); tray.style.visibility = 'hidden'; }
    document.documentElement.style.overflow = 'hidden';
    var x = modal.querySelector('.vf-modal__x');
    if (x) { x.focus(); }
  }

  function closeCompare() {
    if (!modal) { return; }
    modal.className = 'vf-modal';
    if (tray) { tray.removeAttribute('aria-hidden'); tray.style.visibility = ''; }
    document.documentElement.style.overflow = '';
    if (lastFocus && lastFocus.focus) { lastFocus.focus(); }
  }

  /* ------------------------------------------------------------ events */
  document.addEventListener('click', function (e) {
    var t = e.target;
    if (!t || !t.closest) { return; }

    var sv = t.closest('[data-save]');
    if (sv) {
      var id = sv.getAttribute('data-save');
      var now = toggleSaved(id);
      sv.setAttribute('aria-pressed', now ? 'true' : 'false');
      var nm = BY[id] ? BY[id].n : (sv.getAttribute('data-name') || 'this venue');
      var sp = sv.querySelector('span');
      if (sp) {
        sp.textContent = sv.hasAttribute('data-name')
          ? (now ? 'Saved to your shortlist' : 'Save to your shortlist')
          : (now ? 'Saved' : 'Save');
      }
      sv.setAttribute('aria-label',
        (now ? 'Remove ' : 'Save ') + nm + ' to your shortlist');
      paintTray();
      return;
    }

    if (LIVE && t.closest('[data-showall]')) {
      showAll = true;
      render(false);
      return;
    }

    /* Clearing the shortlist is shortlist state, not results state, so it has
       to work on the accommodation page and the venue pages too. */
    if (t.closest('[data-tray-clear]')) {
      SL = [];
      writeList(SL);
      CMP = [];
      paintPips();
      if (LIVE) { render(false); } else { paintTray(); }
      var pressed = document.querySelectorAll('[data-save][aria-pressed="true"]');
      for (var pi = 0; pi < pressed.length; pi++) {
        pressed[pi].setAttribute('aria-pressed', 'false');
        var psp = pressed[pi].querySelector('span');
        if (psp) {
          psp.textContent = pressed[pi].hasAttribute('data-name')
            ? 'Save to your shortlist' : 'Save';
        }
      }
      return;
    }

    /* Everything past this point needs the dataset and the results list. On a
       venue page there is neither, and the click was not for us. */
    if (!LIVE) { return; }

    var chip = t.closest('[data-clear]');
    if (chip) {
      var key = chip.getAttribute('data-clear');
      if (f[key]) {
        f[key].value = '';
        if (key === 'dest') { fillPrecincts(); }
        render(true);
      }
      return;
    }

    if (t.closest('[data-tray-compare]')) { openCompare(); return; }
    if (t.closest('[data-cmp-close]')) { closeCompare(); return; }
    if (modal && t.className === 'vf-modal__bg') { closeCompare(); return; }
  });

  document.addEventListener('change', function (e) {
    if (!LIVE) { return; }
    var t = e.target;
    if (t.hasAttribute && t.hasAttribute('data-cmp')) {
      var id = t.getAttribute('data-cmp');
      var i = CMP.indexOf(id);
      if (t.checked) {
        if (CMP.length >= MAXCMP) {
          t.checked = false;
          var note = document.getElementById('vf-cmp-max');
          if (note) {
            note.hidden = false;
            window.setTimeout(function () { note.hidden = true; }, 4000);
          }
          return;
        }
        if (i === -1) { CMP.push(id); }
      } else if (i !== -1) {
        CMP.splice(i, 1);
      }
      paintTray();
      return;
    }
    for (var k in f) {
      if (f[k] && t === f[k]) {
        if (k === 'dest') { fillPrecincts(); }
        showAll = false;
        render(true);
        return;
      }
    }
  });

  if (f.guests && LIVE) {
    var tmr;
    f.guests.addEventListener('input', function () {
      window.clearTimeout(tmr);
      tmr = window.setTimeout(function () { showAll = false; render(true); }, 350);
    });
  }

  if (refineBtn && refinePanel) {
    refineBtn.addEventListener('click', function () {
      var open = refineBtn.getAttribute('aria-expanded') === 'true';
      refineBtn.setAttribute('aria-expanded', open ? 'false' : 'true');
      refinePanel.hidden = open;
    });
    if (window.matchMedia && window.matchMedia('(min-width: 900px)').matches) {
      refineBtn.setAttribute('aria-expanded', 'true');
      refinePanel.hidden = false;
    }
  }

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && modal && modal.className.indexOf('on') !== -1) {
      closeCompare();
    }
  });

  /* The ask form filters in place. Without JavaScript it still submits as a
     GET to this page, which the URL preset then reads, so the page works
     either way. */
  var askForm = document.getElementById('vf-ask');
  if (askForm && LIVE) {
    askForm.addEventListener('submit', function (e) {
      e.preventDefault();
      render(true);
      if (countEl && countEl.scrollIntoView) {
        countEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    });
  }

  /* -------------------------------------------- venue page save buttons */
  function bindOnPageSaves() {
    var btns = document.querySelectorAll('[data-save][data-name]');
    for (var i = 0; i < btns.length; i++) {
      var b = btns[i], id = b.getAttribute('data-save');
      b.setAttribute('aria-pressed', saved(id) ? 'true' : 'false');
      var sp = b.querySelector('span');
      if (sp) {
        sp.textContent = saved(id)
          ? 'Saved to your shortlist' : 'Save to your shortlist';
      }
    }
  }

  if (LIVE) {
    preset();
    render(false);
  } else {
    paintTray();
    if (!VENUES.length && SL.length && window.fetch &&
        (tray || document.querySelector('[data-save]'))) {
      window.fetch(dataUrl()).then(function (r) {
        return r.ok ? r.json() : null;
      }).then(function (d) {
        if (!d || !d.venues) { return; }
        VENUES = d.venues;
        for (var i = 0; i < VENUES.length; i++) { BY[VENUES[i].id] = VENUES[i]; }
        paintTray();
      })['catch'](function () { /* names stay absent, the tray still works */ });
    }
  }
}());
