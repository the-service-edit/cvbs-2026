/* CVBS — shared interactions. Vanilla, no dependencies. */
(function () {
  'use strict';
  var doc = document;

  /* Sticky header: shade on scroll (always visible) */
  var header = doc.querySelector('.site-header');
  if (header) {
    var onScroll = function () {
      header.classList.toggle('scrolled', (window.scrollY || 0) > 12);
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* Mobile menu */
  var toggle = doc.querySelector('.nav-toggle');
  var menu = doc.querySelector('.mobile-menu');
  if (toggle && menu) {
    var setMenu = function (open) {
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      menu.classList.toggle('open', open);
      doc.body.classList.toggle('menu-open', open);
      if (header) {
        header.classList.toggle('nav-open', open);
        if (open) header.classList.remove('nav-hide');
      }
    };
    toggle.addEventListener('click', function () {
      setMenu(toggle.getAttribute('aria-expanded') !== 'true');
    });
    menu.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () { setMenu(false); });
    });
    window.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') setMenu(false);
    });
  }

  /* Mobile nav accordions (Services / Destinations) */
  doc.querySelectorAll('.mobile-menu .m-top').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var item = btn.closest('.m-item');
      var open = item.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  });

  /* Scroll reveal */
  var reveals = doc.querySelectorAll('.reveal');
  if (reveals.length && 'IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { threshold: 0.08, rootMargin: '0px 0px 0px 0px' });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add('in'); });
  }

  /* 3D rolling destinations stage */
  (function () {
    var stage = doc.getElementById('destStage');
    if (!stage) return;
    var cards = [].slice.call(stage.querySelectorAll('.dcard'));
    if (!cards.length) return;
    var reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
    var mobile = window.matchMedia('(max-width:680px)');
    var offset = 0, S = 240, L = 0, paused = false, rafId = null, running = false;
    function measure() { var cw = cards[0].offsetWidth || 240; S = cw * 1.2; L = S * cards.length; }
    window.addEventListener('resize', function () { if (running) measure(); }, { passive: true });
    stage.addEventListener('mouseenter', function () { paused = true; });
    stage.addEventListener('mouseleave', function () { paused = false; });
    function clearInline() { cards.forEach(function (c) { c.style.transform = ''; c.style.zIndex = ''; c.style.opacity = ''; }); }
    function tick() {
      if (!paused) offset = (offset + 0.42) % L;
      var W = stage.clientWidth, radius = W * 0.5, half = L / 2;
      for (var i = 0; i < cards.length; i++) {
        var x = (((i * S - offset) % L) + L) % L - half;
        var t = Math.max(-1, Math.min(1, x / radius));
        var ry = -42 * t, tz = -260 * Math.abs(t), ty = 20 * Math.abs(t);
        cards[i].style.transform = 'translate(-50%,-50%) translateX(' + x + 'px) translateZ(' + tz + 'px) rotateY(' + ry + 'deg) translateY(' + ty + 'px)';
        cards[i].style.zIndex = String(1000 - Math.round(Math.abs(x)));
        cards[i].style.opacity = String(1 - 0.5 * Math.min(1, Math.abs(t)));
      }
      rafId = requestAnimationFrame(tick);
    }
    function update() {
      if (mobile.matches || reduce.matches) { if (running) { running = false; if (rafId) { cancelAnimationFrame(rafId); rafId = null; } } clearInline(); }
      else if (!running) { running = true; measure(); rafId = requestAnimationFrame(tick); }
    }
    if (mobile.addEventListener) { mobile.addEventListener('change', update); reduce.addEventListener('change', update); }
    else { mobile.addListener(update); reduce.addListener(update); }
    update();
  })();

  /* Shared form delivery helpers. Never report success unless Web3Forms confirms it. */
  function hasWeb3FormsKey(form) {
    var key = (form.querySelector('[name="access_key"]') || {}).value || '';
    return /^[0-9a-f-]{20,}$/i.test(key);
  }
  function showSubmissionError(form, message) {
    var error = form.querySelector('[data-form-error]');
    if (!error) {
      error = doc.createElement('p');
      error.className = 'form-error';
      error.setAttribute('data-form-error', '');
      error.setAttribute('role', 'alert');
      form.appendChild(error);
    }
    error.textContent = message + ' ';
    var link = doc.createElement('a');
    link.href = 'contact.html';
    link.textContent = 'Contact the CVBS team directly.';
    error.appendChild(link);
    error.hidden = false;
  }
  function clearSubmissionError(form) {
    var error = form.querySelector('[data-form-error]');
    if (error) error.hidden = true;
  }
  function submitToWeb3Forms(form) {
    return fetch('https://api.web3forms.com/submit', {
      method: 'POST',
      headers: { 'Accept': 'application/json' },
      body: new FormData(form)
    }).then(function (response) {
      return response.json().catch(function () { return {}; }).then(function (data) {
        if (!response.ok || !data.success) throw new Error(data.message || 'Submission failed');
        return data;
      });
    });
  }

  /* Multi-step brief wizard + Web3Forms submit */
  doc.querySelectorAll('[data-wizard]').forEach(function (form) {
    var steps = [].slice.call(form.querySelectorAll('.wiz-step'));
    var dots = [].slice.call(form.querySelectorAll('.wiz-progress .dot'));
    var i = 0;
    function show(n) {
      i = Math.max(0, Math.min(steps.length - 1, n));
      steps.forEach(function (s, k) { s.classList.toggle('active', k === i); });
      dots.forEach(function (d, k) { d.classList.toggle('active', k <= i); });
      form.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
    function valid(step) {
      var ok = true;
      step.querySelectorAll('[required]').forEach(function (el) {
        if (!el.value) { el.style.borderColor = '#c0532a'; ok = false; } else { el.style.borderColor = ''; }
      });
      var need = step.querySelector('[data-need-one]');
      if (need) {
        var any = need.querySelectorAll('input:checked').length > 0;
        var msg = need.querySelector('[data-need-msg]');
        if (msg) msg.hidden = any;
        if (!any) ok = false;
      }
      return ok;
    }
    form.querySelectorAll('[data-next]').forEach(function (b) {
      b.addEventListener('click', function () { if (valid(steps[i])) show(i + 1); });
    });
    form.querySelectorAll('[data-back]').forEach(function (b) {
      b.addEventListener('click', function () { show(i - 1); });
    });
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!valid(steps[i])) return;
      var ok = form.querySelector('[data-form-success]');
      var done = function () {
        form.querySelectorAll('.wiz-step,.wiz-nav,.wiz-progress').forEach(function (el) { el.style.display = 'none'; });
        if (ok) { ok.hidden = false; ok.scrollIntoView({ behavior: 'smooth', block: 'center' }); }
      };
      clearSubmissionError(form);
      if (!hasWeb3FormsKey(form)) {
        showSubmissionError(form, 'Online submission is temporarily unavailable. Your answers are still on this page.');
        return;
      }
      submitToWeb3Forms(form).then(done).catch(function () {
        showSubmissionError(form, 'We could not send your brief. Your answers are still on this page, so please try again.');
      });
    });
    show(0);
  });

  /* Newsletter / venue-offers signup */
  doc.querySelectorAll('[data-subscribe]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var email = form.querySelector('input[type="email"]');
      if (email && !email.checkValidity()) { email.reportValidity(); return; }
      var ok = form.querySelector('[data-form-success]');
      var done = function () {
        var row = form.querySelector('.sub-row'), fine = form.querySelector('.sub-fine');
        if (row) row.style.display = 'none';
        if (fine) fine.style.display = 'none';
        if (ok) ok.hidden = false;
      };
      var button = form.querySelector('button[type="submit"]');
      var buttonHtml = button ? button.innerHTML : '';
      clearSubmissionError(form);
      if (!hasWeb3FormsKey(form)) {
        showSubmissionError(form, 'Email signup is temporarily unavailable. We have not added your address.');
        return;
      }
      if (button) { button.disabled = true; button.textContent = 'Sending…'; }
      submitToWeb3Forms(form).then(done).catch(function () {
        showSubmissionError(form, 'We could not add your email. Please try again.');
      }).then(function () {
        if (button) { button.disabled = false; button.innerHTML = buttonHtml; }
      });
    });
  });

  /* Mobile bottom bar: reveal after the trust logos (or ~1 screen on interior pages) */
  (function () {
    var bar = doc.querySelector('.mbar');
    if (!bar) return;
    bar.classList.add('mbar--hidden');
    var reveal = function () { bar.classList.remove('mbar--hidden'); };
    var hide = function () { bar.classList.add('mbar--hidden'); };
    var trigger = doc.querySelector('.logos--trust') || doc.querySelector('.logo-marquee') || doc.querySelector('.trustline');
    if (trigger && 'IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (entries) {
        var en = entries[0];
        if (!en.isIntersecting && en.boundingClientRect.top < 0) reveal();
        else if (en.isIntersecting) hide();
      }, { threshold: 0 });
      io.observe(trigger);
    } else {
      var onS = function () {
        if ((window.scrollY || 0) > window.innerHeight * 0.8) reveal(); else hide();
      };
      onS();
      window.addEventListener('scroll', onS, { passive: true });
    }
  })();

  /* Lazy ambient background videos (load only when near viewport) */
  doc.querySelectorAll('video[data-lazy]').forEach(function (v) {
    var src = v.querySelector('source[data-src]');
    if (!src || !('IntersectionObserver' in window)) {
      if (src) { src.src = src.getAttribute('data-src'); v.load(); }
      return;
    }
    var vio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        src.src = src.getAttribute('data-src');
        v.load();
        var p = v.play(); if (p && p.catch) p.catch(function () {});
        vio.disconnect();
      });
    }, { rootMargin: '250px' });
    vio.observe(v);
  });

  /* Count-up stats */
  (function () {
    var nums = doc.querySelectorAll('[data-count]');
    if (!nums.length) return;
    if (!('IntersectionObserver' in window)) {
      nums.forEach(function (el) { el.textContent = el.getAttribute('data-count'); });
      return;
    }
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target, end = parseInt(el.getAttribute('data-count'), 10) || 0, t0 = null, dur = 1200;
        function step(ts) {
          if (!t0) t0 = ts;
          var p = Math.min((ts - t0) / dur, 1);
          el.textContent = Math.round(end * (0.5 - Math.cos(Math.PI * p) / 2));
          if (p < 1) requestAnimationFrame(step);
        }
        requestAnimationFrame(step); cio.unobserve(el);
      });
    }, { threshold: 0.4 });
    nums.forEach(function (el) { cio.observe(el); });
  })();

  /* Simple single-form fallback */
  doc.querySelectorAll('[data-brief-form]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var ok = form.querySelector('[data-form-success]');
      form.querySelectorAll('input,select,textarea,button').forEach(function (el) { el.disabled = true; });
      if (ok) { ok.hidden = false; ok.scrollIntoView({ behavior: 'smooth', block: 'center' }); }
    });
  });
})();

/* ==========================================================================
   Venue index. Shared across every destination page.
   Each city page carries a <script type="application/json" id="vidx-data">
   island and an empty .vidx shell. This renders, filters and sorts it.
   Adding a new city means adding data, not code.
   ========================================================================== */
(function () {
  'use strict';
  var doc = document;
  var island = doc.getElementById('vidx-data');
  var root = doc.getElementById('vidx');
  if (!island || !root) return;

  var VENUES;
  try { VENUES = JSON.parse(island.textContent); } catch (e) { return; }
  if (!VENUES || !VENUES.length) return;

  var city = root.getAttribute('data-city') || '';
  var tbody = doc.getElementById('vidx-body');
  var countEl = doc.getElementById('vidx-count');
  var fCap = doc.getElementById('vidx-cap');
  var fSetup = doc.getElementById('vidx-setup');
  var fPrec = doc.getElementById('vidx-prec');
  var fType = doc.getElementById('vidx-type');
  var fQ = doc.getElementById('vidx-q');
  var fAccom = doc.getElementById('vidx-accom');
  var fSeen = doc.getElementById('vidx-seen');
  var resetBtn = doc.getElementById('vidx-reset');
  /* The table and its filters are optional. Sydney publishes the answer block,
     the at a glance rail and the site visit records without them, and a page
     that carries only those must still work. Only the table code is gated. */
  var hasTable = !!(tbody && fCap && fSetup && fPrec && fType);

  /* The site visit option only exists once there is a site visit to show. An
     empty filter is worse than no filter, so it removes itself until Karen has
     filled in at least one 'seen' record in the data. */
  if (hasTable && fSeen && !VENUES.some(function (v) { return v.seen; })) {
    var so = fSeen.querySelector('option[value="seen"]');
    if (so) so.parentNode.removeChild(so);
  }

  var TYPE_LABEL = { conv: 'Convention centre', hotel: 'Hotel', event: 'Event venue' };
  var SETUPS = [['th','Theatre'],['bq','Banquet'],['cab','Cabaret'],['cl','Classroom'],
                ['ck','Cocktail'],['ush','U-shape'],['bd','Boardroom']];
  var DEFAULT_SHOWN = 6;
  var showAll = false;
  var sortKey = 'cap';
  var sortDir = -1;

  var fmt = function (n) {
    return (n === null || n === undefined) ? null : n.toLocaleString('en-AU');
  };
  var cell = function (n) {
    var v = fmt(n);
    return v === null ? '<span class="vidx-none">Not published</span>' : v;
  };
  var metres = function (v) {
    if (v.ceil === null || v.ceil === undefined) return '<span class="vidx-none">Not published</span>';
    var t = v.ceil + 'm';
    return v.ceilq ? t + '<span class="vidx-qual">' + v.ceilq + '</span>' : t;
  };
  var capOf = function (v) {
    var n = v[fSetup ? fSetup.value : 'th'];
    return (n === null || n === undefined) ? null : n;
  };

  /* Precinct options, built from the data so a new city needs no edits here.
     Only where the filter exists at all. */
  if (fPrec) {
    var precincts = [];
    VENUES.forEach(function (v) { if (precincts.indexOf(v.pr) === -1) precincts.push(v.pr); });
    precincts.sort().forEach(function (p) {
      var o = doc.createElement('option');
      o.value = p; o.textContent = p;
      fPrec.appendChild(o);
    });
  }

  /* At a glance rail, derived from the data so it can never contradict the table */
  (function stats() {
    var box = doc.getElementById('vidx-stats');
    if (!box) return;
    var used = {};
    var pick = function (pool, key) {
      var hit = pool.filter(function (v) { return v[key] && !used[v.n]; })
                    .sort(function (a, b) { return b[key] - a[key]; })[0];
      if (hit) used[hit.n] = true;
      return hit;
    };
    var hotels = VENUES.filter(function (v) { return v.ty === 'hotel'; });
    /* a qualified ceiling (a dome apex, say) is not a headline number */
    var plainCeil = VENUES.filter(function (v) { return v.ceil && !v.ceilq; });

    var big = pick(VENUES, 'th');
    var ballroom = pick(hotels, 'th');
    var tall = pick(plainCeil, 'ceil');
    var beds = pick(VENUES, 'gr');

    var rows = [];
    if (big) rows.push([big.th.toLocaleString('en-AU'), 'seats',
      'Largest single space in ' + city + ', ' + big.sp + ' at ' + big.n]);
    if (ballroom) rows.push([ballroom.th.toLocaleString('en-AU'), 'seats',
      'Largest hotel ballroom, ' + ballroom.sp + ' at ' + ballroom.n]);
    if (tall) rows.push([tall.ceil + 'm', '',
      'Highest ceiling on record, ' + tall.sp + ' at ' + tall.n]);
    if (beds) rows.push([beds.gr.toLocaleString('en-AU'), 'rooms',
      'Most delegate beds on one site, at ' + beds.n]);

    box.innerHTML = '<span class="vidx-stats__tag">' + city + ' at a glance</span>' +
      rows.map(function (r) {
        return '<div class="vidx-stat"><div class="vidx-stat__n">' + r[0] +
          (r[1] ? '<small>' + r[1] + '</small>' : '') + '</div>' +
          '<div class="vidx-stat__l">' + r[2] + '</div></div>';
      }).join('');
  })();


  /* --- site visit record --------------------------------------------------
     v.visit = {by, when, on, note, photos: [{s, l, c, w, h}]}
       by    who from CVBS was in the room
       when  human date, "March 2026"
       on    sortable date, "2026-03", used by the recently visited band
       note  what the floor plan does not tell you
       s/l   small and large image paths, c the caption, w/h the small size

     Renders only where a visit is logged. No visit, no markup, no claim.
     Never hand write a visit record. It comes from the site visit intake
     script, which reads the date off the photograph itself. See
     scripts/site-visit-intake.py. ---------------------------------------- */

  var esc = function (s) {
    return String(s === null || s === undefined ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
  };
  var pad2 = function (i) { return (i < 9 ? '0' : '') + (i + 1); };
  var hasPhotos = function (v) {
    return !!(v && v.visit && v.visit.photos && v.visit.photos.length);
  };
  var visitAttr = function (v) {
    var vis = v.visit || {};
    return (vis.by || 'CVBS') + (vis.when ? ', ' + vis.when : '');
  };
  var ICON_EYE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" ' +
    'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
    '<path d="M2 12s3.6-6 10-6 10 6 10 6-3.6 6-10 6-10-6-10-6z"/><circle cx="12" cy="12" r="2.6"/></svg>';
  var ICON_CAM = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" ' +
    'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
    '<path d="M3 8.5h3.2l1.4-2.2h7.8l1.4 2.2H21v10H3z"/><circle cx="12" cy="13" r="3.1"/></svg>';

  function visitCount(v) {
    if (!hasPhotos(v)) return '';
    var n = v.visit.photos.length;
    return '<span class="vidx-seen__n">' + ICON_CAM + n + (n === 1 ? ' photo' : ' photos') + '</span>';
  }

  function visitBlock(v) {
    if (!hasPhotos(v)) return '';
    var vis = v.visit;
    var who = esc(vis.by || 'CVBS');
    var when = vis.when ? esc(vis.when) : '';
    var attrib = esc(v.n + (v.sp ? ', ' + v.sp : '') + '. Photographed by ' + visitAttr(v) + '.');
    return '<div class="vidx-visit">' +
      '<div class="vidx-visit__head">' +
        '<span class="vidx-visit__tag">' + ICON_EYE + 'Site visit record</span>' +
        '<p class="vidx-visit__who"><b>Walked by ' + who + '</b>' + (when ? ', ' + when : '') + '</p>' +
        '<p class="vidx-visit__prov">Photographed by us on the day. Not supplied by the venue.</p>' +
      '</div>' +
      (vis.note ? '<p class="vidx-visit__note"><b>What the floor plan does not tell you.</b> ' +
        esc(vis.note) + '</p>' : '') +
      '<ul class="vidx-visit__strip">' +
        vis.photos.map(function (p, i) {
          var cap = p.c || '';
          var alt = cap || (v.n + ', ' + (v.sp || 'event space'));
          return '<li class="vidx-visit__item">' +
            '<button type="button" class="vidx-visit__btn" data-vlb="1"' +
              ' data-l="' + esc(p.l || p.s) + '"' +
              ' data-c="' + esc(cap) + '"' +
              ' data-a="' + attrib + '"' +
              ' aria-label="Enlarge photograph ' + pad2(i) + ' of ' + esc(v.n) + '">' +
              '<img src="' + esc(p.s) + '" alt="' + esc(alt) + '" loading="lazy" decoding="async"' +
                (p.w ? ' width="' + p.w + '"' : '') + (p.h ? ' height="' + p.h + '"' : '') + '>' +
            '</button>' +
            (cap ? '<p class="vidx-visit__cap"><span class="vidx-visit__num">' + pad2(i) + '</span>' +
              esc(cap) + '</p>' : '') +
          '</li>';
        }).join('') +
      '</ul>' +
    '</div>';
  }

  /* The recently visited band. Sits above the filters. A full venue record per
     visit: the photograph we took, a short summary of what the room suits, the
     complete published specification, and the date we were in it. This is the
     firsthand version of a venue listing, and it is deliberately slower to read
     than a table row, because a table row is what everybody else has.
     It hides itself entirely while there is nothing to show, so the page never
     advertises an empty promise. */
  (function recentBand() {
    var box = doc.getElementById('vidx-recent');
    if (!box) return;
    var withVisit = VENUES.filter(hasPhotos).sort(function (a, b) {
      return String(b.visit.on || '').localeCompare(String(a.visit.on || ''));
    }).slice(0, 6);
    if (!withVisit.length) {
      /* Nothing to show. Hide the band and, where the band is the whole point
         of its section, hide the section too, so the page never carries an
         empty heading promising rooms we have walked. */
      box.hidden = true;
      return;
    }

    function specRow(dt, dd) {
      return '<div class="vidx-spec__row"><dt>' + dt + '</dt><dd>' + dd + '</dd></div>';
    }

    box.innerHTML =
      '<div class="vidx-recent__head">' +
        '<span class="vidx-recent__tag">' + ICON_EYE + 'Recently visited</span>' +
        '<p class="vidx-recent__sub">The rooms we have most recently stood in, with the date we were ' +
          'there. Every photograph is one of ours, taken on the day.</p>' +
      '</div>' +
      '<ul class="vidx-recent__grid">' +
        withVisit.map(function (v) {
          var meta = [v.sp, v.pr, TYPE_LABEL[v.ty] || ''].filter(Boolean).join(' &middot; ');
          var setups = SETUPS.map(function (st) {
            return specRow(st[1], cell(v[st[0]]));
          }).join('');
          var room =
            specRow('Floor area', v.area ? fmt(v.area) + ' sqm' : '<span class="vidx-none">Not published</span>') +
            specRow('Ceiling height', metres(v)) +
            specRow('Meeting rooms', cell(v.br)) +
            specRow('Guest rooms', v.gr === 0 ? '<span class="vidx-none">None on site</span>' : cell(v.gr)) +
            (v.s_name ? specRow('Second space', esc(v.s_name) + (v.s_th ? ', ' + fmt(v.s_th) + ' theatre' : '')) : '');
          return '<li class="vrec">' +
            '<header class="vrec__head">' +
              '<p class="vrec__w">' + ICON_EYE + 'Walked by ' + esc(visitAttr(v)) + '</p>' +
              '<h3 class="vrec__n">' + esc(v.n) + '</h3>' +
              '<p class="vrec__meta">' + meta + '</p>' +
            '</header>' +
            '<div class="vrec__words">' +
              (v.note ? '<p class="vrec__sum">' + esc(v.note) + '</p>' : '') +
              (v.visit.note ? '<p class="vrec__note"><b>What the floor plan does not tell you.</b> ' +
                esc(v.visit.note) + '</p>' : '') +
              '<a class="vidx-enq vrec__enq" href="submit-a-brief.html?dest=' + encodeURIComponent(city) +
                '&venue=' + encodeURIComponent(v.n) + '">Ask us about this room' +
                '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" ' +
                'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></a>' +
            '</div>' +
            '<div class="vrec__specs">' +
              '<div class="vrec__speccol"><h4>' + esc(v.sp || 'Largest space') + '</h4><dl>' + setups + '</dl></div>' +
              '<div class="vrec__speccol"><h4>The room itself</h4><dl>' + room + '</dl></div>' +
            '</div>' +
            '<ul class="vrec__photos">' +
              v.visit.photos.map(function (q, i) {
                var qc = q.c || '';
                return '<li class="vidx-visit__item">' +
                  '<button type="button" class="vidx-visit__btn" data-vlb="1"' +
                    ' data-l="' + esc(q.l || q.s) + '" data-c="' + esc(qc) + '"' +
                    ' data-a="' + esc(v.n + (v.sp ? ', ' + v.sp : '') + '. Photographed by ' + visitAttr(v) + '.') + '"' +
                    ' aria-label="Enlarge photograph ' + pad2(i) + ' of ' + esc(v.n) + '">' +
                    '<img src="' + esc(q.s) + '" alt="' + esc(qc || v.n) + '" loading="lazy" decoding="async"' +
                      (q.w ? ' width="' + q.w + '"' : '') + (q.h ? ' height="' + q.h + '"' : '') + '>' +
                  '</button>' +
                  (qc ? '<p class="vidx-visit__cap"><span class="vidx-visit__num">' + pad2(i) + '</span>' +
                    esc(qc) + '</p>' : '') +
                '</li>';
              }).join('') +
            '</ul>' +
          '</li>';
        }).join('') +
      '</ul>' +
      '<p class="vidx-recent__foot">Every capacity above is the venue’s own published figure for the ' +
        'space named. The photograph and the note beside it are ours.</p>';
    box.hidden = false;

    /* The page is authored for its normal state, which is this section hidden,
       because most venues have no site visit logged. Revealing it inserts a
       band between two that already alternate, so every band after it flips to
       keep the stone and white rhythm. Doing it on reveal rather than on hide
       means the common case needs no JavaScript and cannot flash. */
    var sec = box.closest('section[data-visit-section]');
    if (sec && sec.hidden) {
      sec.hidden = false;
      var n = sec.nextElementSibling;
      while (n) {
        if (n.classList.contains('s-stone')) n.classList.replace('s-stone', 's-white');
        else if (n.classList.contains('s-white')) n.classList.replace('s-white', 's-stone');
        n = n.nextElementSibling;
      }
    }
  })();

  /* Lightbox. Built once, on first use, and shared by both blocks. */
  (function lightbox() {
    var el = null, imgEl, capEl, attrEl, prevBtn, nextBtn, closeBtn;
    var group = [], at = 0, lastFocus = null;

    function build() {
      el = doc.createElement('div');
      el.className = 'vlb';
      el.setAttribute('role', 'dialog');
      el.setAttribute('aria-modal', 'true');
      el.setAttribute('aria-label', 'Site visit photograph');
      el.innerHTML =
        '<button type="button" class="vlb__close" aria-label="Close">' +
          '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" ' +
          'stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg></button>' +
        '<button type="button" class="vlb__nav vlb__prev" aria-label="Previous photograph">' +
          '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" ' +
          'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 6l-6 6 6 6"/></svg></button>' +
        '<button type="button" class="vlb__nav vlb__next" aria-label="Next photograph">' +
          '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" ' +
          'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 6l6 6-6 6"/></svg></button>' +
        '<div class="vlb__box">' +
          '<img class="vlb__img" src="" alt="">' +
          '<div class="vlb__meta"><p class="vlb__cap"></p><p class="vlb__attr"></p></div>' +
        '</div>';
      doc.body.appendChild(el);
      imgEl = el.querySelector('.vlb__img');
      capEl = el.querySelector('.vlb__cap');
      attrEl = el.querySelector('.vlb__attr');
      prevBtn = el.querySelector('.vlb__prev');
      nextBtn = el.querySelector('.vlb__next');
      closeBtn = el.querySelector('.vlb__close');
      closeBtn.addEventListener('click', close);
      prevBtn.addEventListener('click', function () { go(-1); });
      nextBtn.addEventListener('click', function () { go(1); });
      el.addEventListener('click', function (e) { if (e.target === el) close(); });
      doc.addEventListener('keydown', function (e) {
        if (!el || !el.classList.contains('is-open')) return;
        if (e.key === 'Escape') close();
        else if (e.key === 'ArrowLeft') go(-1);
        else if (e.key === 'ArrowRight') go(1);
      });
    }

    function paint() {
      var b = group[at];
      if (!b) return;
      imgEl.src = b.getAttribute('data-l');
      imgEl.alt = b.getAttribute('data-c') || '';
      capEl.textContent = b.getAttribute('data-c') || '';
      attrEl.textContent = b.getAttribute('data-a') || '';
      var many = group.length > 1;
      prevBtn.hidden = !many;
      nextBtn.hidden = !many;
    }
    function go(d) {
      if (group.length < 2) return;
      at = (at + d + group.length) % group.length;
      paint();
    }
    function close() {
      el.classList.remove('is-open');
      doc.documentElement.style.overflow = '';
      if (lastFocus && lastFocus.focus) lastFocus.focus();
    }
    function open(btn) {
      if (!el) build();
      var strip = btn.closest('.vrec') || btn.closest('.vidx-visit__strip') || btn.closest('.vidx-recent__grid');
      group = strip ? Array.prototype.slice.call(strip.querySelectorAll('[data-vlb]')) : [btn];
      at = Math.max(0, group.indexOf(btn));
      lastFocus = btn;
      paint();
      el.classList.add('is-open');
      doc.documentElement.style.overflow = 'hidden';
      closeBtn.focus();
    }

    doc.addEventListener('click', function (e) {
      var btn = e.target.closest ? e.target.closest('[data-vlb]') : null;
      if (btn) { e.preventDefault(); open(btn); }
    });
  })();

  function render() {
    var minCap = +fCap.value;
    var prec = fPrec.value;
    var type = fType.value;
    var q = fQ ? fQ.value.trim().toLowerCase() : '';
    var accom = fAccom ? fAccom.value : '';
    var seenF = fSeen ? fSeen.value : '';
    var setupLabel = fSetup.options[fSetup.selectedIndex].text.toLowerCase();
    var hiddenForNoData = 0;

    var rows = VENUES.filter(function (v) {
      if (prec && v.pr !== prec) return false;
      if (type && v.ty !== type) return false;
      if (q && (v.n + ' ' + v.sp + ' ' + v.pr).toLowerCase().indexOf(q) === -1) return false;
      if (accom === 'yes' && !v.gr) return false;
      if (accom === 'no' && v.gr) return false;
      /* Firsthand filters. 'worked' is CVBS booking history, confirmed by Karen.
         'seen' is the site visit record and prints only where a visit is logged. */
      if (seenF === 'worked' && !v.worked) return false;
      if (seenF === 'seen' && !v.seen) return false;
      var c = capOf(v);
      if (c === null) {
        /* Venue does not publish this setup. Keep it visible at "any size",
           hide it only when the planner has set a capacity floor. */
        if (minCap > 0) { hiddenForNoData++; return false; }
        return true;
      }
      return c >= minCap;
    });

    rows.sort(function (a, b) {
      var x, y;
      if (sortKey === 'cap') { x = capOf(a); y = capOf(b); }
      else if (sortKey === 'ceil') { x = a.ceil; y = b.ceil; }
      else { x = a[sortKey]; y = b[sortKey]; }
      if (x === null || x === undefined) return 1;   /* nulls always last */
      if (y === null || y === undefined) return -1;
      if (typeof x === 'string') return x.localeCompare(y) * sortDir;
      return (x - y) * sortDir;
    });

    var filtered = (minCap > 0 || prec || type || q || accom || seenF);
    var limited = !filtered && !showAll && rows.length > DEFAULT_SHOWN;
    var shown = limited ? DEFAULT_SHOWN : rows.length;

    if (countEl) {
      if (!rows.length) {
        countEl.innerHTML = '<span>No venues match those filters.</span>';
      } else if (limited) {
        countEl.innerHTML = '<span>Showing the largest ' + city + ' venues by ' + setupLabel +
          ' capacity. Filter above, or <button type="button" class="vidx-showall" id="vidx-showall">see them all</button>.</span>';
      } else {
        countEl.innerHTML = '<span>' +
          (filtered
            ? '<b>' + rows.length + '</b> ' + (rows.length === 1 ? 'venue' : 'venues') +
              ' match, largest ' + setupLabel + ' capacity first.'
            : 'Every ' + city + ' venue we hold, largest ' + setupLabel + ' capacity first. ' +
              '<button type="button" class="vidx-showall" id="vidx-showall">Show fewer</button>') + '</span>' +
          (hiddenForNoData ? '<span class="vidx-hidden">' + hiddenForNoData +
            ' more ' + (hiddenForNoData === 1 ? 'venue does' : 'venues do') +
            ' not publish a ' + setupLabel + ' capacity. Ask us and we will confirm ' +
            (hiddenForNoData === 1 ? 'it' : 'them') + ' with the venue.</span>' : '');
      }
    }

    if (!rows.length) {
      tbody.innerHTML = '<tr><td colspan="8"><div class="vidx-empty">Nothing in the index matches that brief. ' +
        'That does not mean nothing in ' + city + ' does. ' +
        '<a href="submit-a-brief.html">Send us the brief</a> and we will go looking.</div></td></tr>';
      return;
    }

    tbody.innerHTML = rows.map(function (v, i) {
      var over = i >= shown;
      var t = TYPE_LABEL[v.ty] || '';
      var pid = 'vidx-spec-' + i;
      var setupRows = SETUPS.map(function (s) {
        return '<div class="vidx-spec__row"><dt>' + s[1] + '</dt><dd>' + cell(v[s[0]]) + '</dd></div>';
      }).join('');
      return '<tr class="vidx-row' + (over ? ' vidx-row--over" hidden' : '"') + '>' +
        '<td class="vidx-c-name">' +
          '<div class="vidx-name">' + v.n + '</div>' +
          '<div class="vidx-space">' + v.sp + '</div>' +
          (v.worked ? '<span class="vidx-tag vidx-tag--worked">' +
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 12.5l5 5L20 6.5"/></svg>Worked with</span> ' : '') +
          (v.seen ? '<div class="vidx-seen"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2 12s3.6-6 10-6 10 6 10 6-3.6 6-10 6-10-6-10-6z"/><circle cx="12" cy="12" r="2.6"/></svg>Walked by ' + v.seen + visitCount(v) + '</div>' : '') +
          (t ? '<span class="vidx-tag vidx-tag--' + v.ty + '">' + t + '</span>' : '') +
        '</td>' +
        '<td data-l="Precinct">' + v.pr + '</td>' +
        '<td class="num" data-l="Largest space"><span class="vidx-cap">' + cell(capOf(v)) + '</span>' +
          '<div class="vidx-setup">' + setupLabel + '</div></td>' +
        '<td class="num" data-l="Ceiling">' + metres(v) + '</td>' +
        '<td class="num" data-l="Meeting rooms">' + cell(v.br) + '</td>' +
        '<td class="num" data-l="Guest rooms">' +
          (v.gr === 0 ? '<span class="vidx-none">None</span>' : cell(v.gr)) + '</td>' +
        '<td class="vidx-c-suit"><div class="vidx-suit">' + v.note + '</div></td>' +
        '<td class="vidx-c-enq">' +
          '<button type="button" class="vidx-more" aria-expanded="false" aria-controls="' + pid + '">' +
            'Full specs<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg></button>' +
          '<a class="vidx-enq" href="submit-a-brief.html?dest=' + encodeURIComponent(city) +
            '&venue=' + encodeURIComponent(v.n) + '">Enquire' +
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></a>' +
        '</td>' +
      '</tr>' +
      '<tr class="vidx-specrow" id="' + pid + '" hidden><td colspan="8">' +
        '<div class="vidx-spec">' +
          '<div class="vidx-spec__col vidx-spec__col--wide"><p class="vidx-spec__full">' + v.note + '</p>' +
            /* Where there is a full visit record below, this line would say the
               same thing twice and answer its own invitation. Only shown where
               a visit is logged without photographs. */
            (v.seen && !hasPhotos(v) ? '<p class="vidx-spec__seen"><b>We have been in this room.</b> Walked by ' + v.seen +
              '. Ask us what the floor plan does not tell you.</p>' : '') + '</div>' +
          '<div class="vidx-spec__col"><h4>' + v.sp + '</h4><dl>' + setupRows + '</dl></div>' +
          '<div class="vidx-spec__col"><h4>The room itself</h4><dl>' +
            '<div class="vidx-spec__row"><dt>Floor area</dt><dd>' +
              (v.area ? fmt(v.area) + ' sqm' : '<span class="vidx-none">Not published</span>') + '</dd></div>' +
            '<div class="vidx-spec__row"><dt>Ceiling height</dt><dd>' + metres(v) + '</dd></div>' +
            '<div class="vidx-spec__row"><dt>Meeting rooms</dt><dd>' + cell(v.br) + '</dd></div>' +
            '<div class="vidx-spec__row"><dt>Guest rooms</dt><dd>' +
              (v.gr === 0 ? '<span class="vidx-none">None on site</span>' : cell(v.gr)) + '</dd></div>' +
          '</dl></div>' +
          '<div class="vidx-spec__col"><h4>Second largest space</h4>' +
            (v.s_name
              ? '<p class="vidx-spec__second"><b>' + v.s_name + '</b></p><dl><div class="vidx-spec__row">' +
                '<dt>Theatre</dt><dd>' + cell(v.s_th) + '</dd></div></dl>' +
                (v.s_th && v.th ? '<p class="vidx-spec__note">The two largest rooms seat <b>' +
                  fmt(v.s_th + v.th) + '</b> between them, which is the ceiling on a plenary plus one concurrent stream.</p>' : '')
              : '<p class="vidx-spec__note">This venue does not publish a second space.</p>') +
          '</div>' +
          visitBlock(v) +
        '</div>' +
      '</td></tr>';
    }).join('');

    var hand = doc.getElementById('vidx-handoff');
    if (hand) {
      if (filtered && rows.length) {
        var bits = [];
        if (minCap) bits.push(minCap + '+ delegates');
        bits.push(setupLabel);
        if (prec) bits.push(prec);
        if (type) bits.push(({conv:'convention centre', hotel:'hotel', event:'dedicated event venue'})[type]);
        if (accom === 'yes') bits.push('accommodation on site');
        if (accom === 'no') bits.push('venue only');
        if (seenF === 'worked') bits.push('venues we have worked with');
        if (seenF === 'seen') bits.push('venues we have been inside');
        if (q) bits.push('matching "' + fQ.value.trim() + '"');
        var href = 'submit-a-brief.html?dest=' + encodeURIComponent(city) +
          (minCap ? '&guests=' + encodeURIComponent(minCap) : '') +
          (accom === 'yes' ? '&accom=1' : '') +
          '&filters=' + encodeURIComponent(bits.join(', ')) +
          '&matched=' + encodeURIComponent(rows.slice(0, 8).map(function (v) { return v.n; }).join('; '));
        hand.innerHTML =
          '<p class="vidx-handoff__q"><b>' + rows.length + ' ' +
            (rows.length === 1 ? 'venue matches' : 'venues match') +
            '.</b> Want us to check availability on your dates and negotiate them?</p>' +
          '<p class="vidx-handoff__s">' + bits.join(' &middot; ') + '</p>' +
          '<a class="btn btn--teal" href="' + href + '">Check these venues for me' +
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></a>';
        hand.hidden = false;
      } else {
        hand.hidden = true;
        hand.innerHTML = '';
      }
    }

    var sa = doc.getElementById('vidx-showall');
    if (sa) sa.addEventListener('click', function () { showAll = !showAll; render(); });

    tbody.querySelectorAll('.vidx-more').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var panel = doc.getElementById(btn.getAttribute('aria-controls'));
        var open = btn.getAttribute('aria-expanded') === 'true';
        btn.setAttribute('aria-expanded', open ? 'false' : 'true');
        if (panel) panel.hidden = open;
      });
    });
  }

  doc.querySelectorAll('.vidx-table th.is-sortable').forEach(function (th) {
    var setState = function () {
      doc.querySelectorAll('.vidx-table th.is-sortable').forEach(function (o) {
        o.classList.remove('asc', 'desc');
        o.setAttribute('aria-sort', 'none');
        var a = o.querySelector('.vidx-arr'); if (a) a.textContent = '↕';
      });
      th.classList.add(sortDir === 1 ? 'asc' : 'desc');
      th.setAttribute('aria-sort', sortDir === 1 ? 'ascending' : 'descending');
      var arr = th.querySelector('.vidx-arr');
      if (arr) arr.textContent = sortDir === 1 ? '↑' : '↓';
    };
    th.addEventListener('click', function () {
      var k = th.getAttribute('data-k');
      if (sortKey === k) { sortDir *= -1; }
      else { sortKey = k; sortDir = (k === 'n' || k === 'pr') ? 1 : -1; }
      setState();
      render();
    });
    th.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); th.click(); }
    });
  });

  [fCap, fSetup, fPrec, fType, fAccom, fSeen].forEach(function (el) {
    if (el) el.addEventListener('change', render);
  });
  if (fQ) {
    var t;
    fQ.addEventListener('input', function () { clearTimeout(t); t = setTimeout(render, 160); });
  }

  if (resetBtn) {
    resetBtn.addEventListener('click', function () {
      fCap.value = '0'; fSetup.value = 'th'; fPrec.value = ''; fType.value = '';
      if (fQ) fQ.value = ''; if (fAccom) fAccom.value = ''; if (fSeen) fSeen.value = '';
      showAll = false;
      sortKey = 'cap'; sortDir = -1;
      doc.querySelectorAll('.vidx-table th.is-sortable').forEach(function (o) {
        o.classList.remove('asc', 'desc');
        o.setAttribute('aria-sort', 'none');
        var a = o.querySelector('.vidx-arr'); if (a) a.textContent = '↕';
      });
      render();
    });
  }

  if (hasTable) render();
})();
