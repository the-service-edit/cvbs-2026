/* CVBS — shared interactions. Vanilla, no dependencies. */
(function () {
  'use strict';
  var doc = document;

  /* Sticky header state */
  var header = doc.querySelector('.site-header');
  if (header) {
    var onScroll = function () {
      header.classList.toggle('scrolled', window.scrollY > 12);
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
      if (header) header.classList.toggle('nav-open', open);
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
