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
      var key = (form.querySelector('[name="access_key"]') || {}).value || '';
      var done = function () {
        form.querySelectorAll('.wiz-step,.wiz-nav,.wiz-progress').forEach(function (el) { el.style.display = 'none'; });
        if (ok) { ok.hidden = false; ok.scrollIntoView({ behavior: 'smooth', block: 'center' }); }
      };
      if (/^[0-9a-f-]{20,}$/i.test(key)) {
        fetch('https://api.web3forms.com/submit', { method: 'POST', body: new FormData(form) }).then(done).catch(done);
      } else { done(); }
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
      var key = (form.querySelector('[name="access_key"]') || {}).value || '';
      var done = function () {
        var row = form.querySelector('.sub-row'), fine = form.querySelector('.sub-fine');
        if (row) row.style.display = 'none';
        if (fine) fine.style.display = 'none';
        if (ok) ok.hidden = false;
      };
      if (/^[0-9a-f-]{20,}$/i.test(key)) {
        fetch('https://api.web3forms.com/submit', { method: 'POST', body: new FormData(form) }).then(done).catch(done);
      } else { done(); }
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
  var sortKey = 'cap';
  var sortDir = -1;

  var fmt = function (n) {
    return (n === null || n === undefined) ? null : n.toLocaleString('en-AU');
  };
  var cell = function (n) {
    var v = fmt(n);
    return v === null ? '<span class="vidx-none">Not published</span>' : v;
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
    var caps = VENUES.map(function (v) { return v.th; }).filter(function (n) { return n; });
    var big = Math.max.apply(null, caps);
    var precs = [];
    VENUES.forEach(function (v) { if (precs.indexOf(v.pr) === -1) precs.push(v.pr); });
    var over1000 = caps.filter(function (n) { return n >= 1000; }).length;
    var beds = VENUES.filter(function (v) { return v.gr; }).length;
    var rows = [
      [VENUES.length, '', 'Major ' + city + ' venues with published capacities'],
      [big.toLocaleString('en-AU'), 'seats', 'Largest single space in ' + city + ', theatre style'],
      [over1000, '', 'Venues that hold 1,000 or more in one room'],
      [beds, '', 'Venues where delegates sleep on the same site']
    ];
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
      else { x = a[sortKey]; y = b[sortKey]; }
      if (x === null || x === undefined) return 1;   /* nulls always last */
      if (y === null || y === undefined) return -1;
      if (typeof x === 'string') return x.localeCompare(y) * sortDir;
      return (x - y) * sortDir;
    });

    if (countEl) {
      if (rows.length) {
        countEl.innerHTML = '<span><b>' + rows.length + '</b> of ' + VENUES.length + ' ' +
          city + ' venues match, largest ' + setupLabel + ' capacity first.</span>' +
          (hiddenForNoData ? '<span class="vidx-hidden">' + hiddenForNoData +
            ' more ' + (hiddenForNoData === 1 ? 'venue does' : 'venues do') +
            ' not publish a ' + setupLabel + ' capacity. Ask us and we will confirm ' +
            (hiddenForNoData === 1 ? 'it' : 'them') + ' with the venue.</span>' : '');
      } else {
        countEl.innerHTML = '<span>No venues in the index match those filters.</span>';
      }
    }

    if (!rows.length) {
      tbody.innerHTML = '<tr><td colspan="7"><div class="vidx-empty">Nothing in the index matches that brief. ' +
        'That does not mean nothing in ' + city + ' does. ' +
        '<a href="submit-a-brief.html">Send us the brief</a> and we will go looking.</div></td></tr>';
      return;
    }

    tbody.innerHTML = rows.map(function (v) {
      var t = TYPE_LABEL[v.ty] || '';
      return '<tr>' +
        '<td class="vidx-c-name">' +
          '<div class="vidx-name">' + v.n + '</div>' +
          '<div class="vidx-space">' + v.sp + '</div>' +
          (t ? '<span class="vidx-tag vidx-tag--' + v.ty + '">' + t + '</span>' : '') +
        '</td>' +
        '<td data-l="Precinct">' + v.pr + '</td>' +
        '<td class="num" data-l="Largest space"><span class="vidx-cap">' + cell(capOf(v)) + '</span>' +
          '<div class="vidx-setup">' + setupLabel + '</div></td>' +
        '<td class="num" data-l="Banquet">' + cell(v.bq) + '</td>' +
        '<td class="num" data-l="Meeting rooms">' + cell(v.br) + '</td>' +
        '<td class="num" data-l="Guest rooms">' +
          (v.gr === 0 ? '<span class="vidx-none">None</span>' : cell(v.gr)) + '</td>' +
        '<td class="vidx-c-suit"><div class="vidx-suit">' + v.note + '</div></td>' +
        '<td class="vidx-c-enq"><a class="vidx-enq" href="submit-a-brief.html?dest=' +
          encodeURIComponent(city) + '&venue=' + encodeURIComponent(v.n) + '">Enquire' +
          '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></a></td>' +
      '</tr>';
    }).join('');
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
