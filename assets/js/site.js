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
  var resetBtn = doc.getElementById('vidx-reset');
  if (!tbody || !fCap || !fSetup || !fPrec || !fType) return;

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
    var n = v[fSetup.value];
    return (n === null || n === undefined) ? null : n;
  };

  /* Precinct options, built from the data so a new city needs no edits here */
  var precincts = [];
  VENUES.forEach(function (v) { if (precincts.indexOf(v.pr) === -1) precincts.push(v.pr); });
  precincts.sort().forEach(function (p) {
    var o = doc.createElement('option');
    o.value = p; o.textContent = p;
    fPrec.appendChild(o);
  });

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

  function render() {
    var minCap = +fCap.value;
    var prec = fPrec.value;
    var type = fType.value;
    var setupLabel = fSetup.options[fSetup.selectedIndex].text.toLowerCase();
    var hiddenForNoData = 0;

    var rows = VENUES.filter(function (v) {
      if (prec && v.pr !== prec) return false;
      if (type && v.ty !== type) return false;
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

    var filtered = (minCap > 0 || prec || type);
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
          '<div class="vidx-spec__col vidx-spec__col--wide"><p class="vidx-spec__full">' + v.note + '</p></div>' +
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
        '</div>' +
      '</td></tr>';
    }).join('');

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

  [fCap, fSetup, fPrec, fType].forEach(function (el) {
    el.addEventListener('change', render);
  });

  if (resetBtn) {
    resetBtn.addEventListener('click', function () {
      fCap.value = '0'; fSetup.value = 'th'; fPrec.value = ''; fType.value = '';
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

  render();
})();
